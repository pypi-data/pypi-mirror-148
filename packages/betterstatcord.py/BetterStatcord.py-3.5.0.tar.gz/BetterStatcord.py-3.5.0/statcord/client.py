import asyncio
import logging
import traceback
from collections import defaultdict
from typing import Callable, DefaultDict, Optional, Set, Union

import aiohttp
import psutil

HEADERS = {"Content-Type": "application/json"}
STAT_ENDPOINT = "https://api.statcord.com/v3/stats"


def _get_package_name(obj: object) -> str:
    try:
        import discord
    except ImportError:
        pass
    else:
        if discord.__title__.lower() == "pycord":
            return "pycord"

    return obj.__module__.split(".")[0]


class StatcordClient:
    """The base Statcord client class."""

    def __init__(
        self,
        bot,
        statcord_key: str,
        custom_1: Callable = None,
        custom_2: Callable = None,
        resource_stats: bool = True,
    ) -> None:
        self.bot = bot

        self.statcord_key = statcord_key

        self.custom_1 = custom_1
        self.custom_2 = custom_2

        # validate args
        if not isinstance(statcord_key, str):
            raise TypeError("The statcord_key argument must be a string.")

        if not (custom_1 is None or callable(custom_1)):
            raise TypeError("The custom_1 argument must be a callable.")

        if not (custom_2 is None or callable(custom_2)):
            raise TypeError("The custom_2 argument must be a callable.")

        # setup logging
        self.logger = logging.getLogger("statcord")
        self.logger.setLevel(logging.WARNING)

        # configuration
        self.resource_stats = resource_stats

        # create aiohttp clientsession instance
        self._aiohttp_ses = aiohttp.ClientSession(loop=bot.loop)

        # create counters
        self._prev_net_usage: Optional[int] = None
        if self.resource_stats:
            net_io_counter = psutil.net_io_counters()
            self._prev_net_usage = net_io_counter.bytes_sent + net_io_counter.bytes_recv

        self._popular_commands: DefaultDict[str, int] = defaultdict(int)
        self._command_count = 0
        self._active_users: Set[int] = set()

        # add on_command handler
        bot.add_listener(self._command_ran, name="on_command")

        pkg_name = _get_package_name(bot)

        if pkg_name == "disnake":
            bot.add_listener(self._disnake_slash_command_ran, name="on_slash_command")

        elif pkg_name == "pycord":
            bot.add_listener(self._pycord_slash_command_ran, name="on_application_command")

        # start stat posting loop
        self._post_loop_task = bot.loop.create_task(self._post_loop())

    def close(self) -> None:
        """Closes the Statcord client safely."""

        self._post_loop_task.cancel()
        self.bot.remove_listener(self._command_ran, name="on_command")

    @staticmethod
    def _format_traceback(e: Exception) -> str:
        """Formats exception traceback nicely."""

        return "".join(traceback.format_exception(type(e), e, e.__traceback__, 4))

    def _get_user_count(self) -> int:
        """Gets the user count of the bot as accurately as it can."""
        cache_size = len(self.bot.users)
        member_count = sum(
            [g.member_count for g in self.bot.guilds if hasattr(g, "member_count") and g.member_count is not None]
        )

        return max(cache_size, member_count)

    async def _command_ran(self, ctx) -> None:
        """Updates command-related statistics."""

        if ctx.command_failed:
            return

        self._command_count += 1
        self._active_users.add(ctx.author.id)
        self._popular_commands[ctx.command.name] += 1

    async def _disnake_slash_command_ran(self, inter: "disnake.ApplicationCommandInteraction") -> None:  # type: ignore # noqa: F821
        """Updates disnake slash command-related statistics."""

        self._command_count += 1
        self._active_users.add(inter.author.id)
        self._popular_commands[inter.data.name] += 1

    async def _pycord_slash_command_ran(self, inter: "discord.ApplicationContext") -> None:  # type: ignore # noqa: F821
        """Updates pycord slash command-related statistics."""

        self._command_count += 1
        self._active_users.add(inter.interaction.user.id)
        self._popular_commands[inter.interaction.data["name"]] += 1

    async def _post_loop(self) -> None:
        """The stat posting loop which posts stats to the Statcord API."""

        while not self.bot.is_closed():
            await self.bot.wait_until_ready()

            try:
                await self.post_stats()
            except Exception as e:
                self.logger.error(f"Statcord stat posting error:\n{self._format_traceback(e)}")

            await asyncio.sleep(60)

    async def _call_custom_graph(self, custom_graph_callable: Callable) -> object:
        if custom_graph_callable is None:
            return None

        if asyncio.iscoroutinefunction(custom_graph_callable):
            return await custom_graph_callable()

        return custom_graph_callable()

    async def post_stats(self) -> None:
        """Helper method used to actually post the stats to Statcord."""

        self.logger.debug("Posting stats to Statcord...")

        if self.resource_stats:
            mem = psutil.virtual_memory()
            mem_used = str(mem.used)
            mem_load = str(mem.percent)

            cpu_load = str(psutil.cpu_percent())

            net_io_counter = psutil.net_io_counters()
            total_net_usage = net_io_counter.bytes_sent + net_io_counter.bytes_recv  # current net usage
            period_net_usage = str(total_net_usage - self._prev_net_usage)  # net usage to be sent
            self._prev_net_usage = total_net_usage  # update previous net usage counter
        else:
            mem_used = "0"
            mem_load = "0"

            cpu_load = "0"

            period_net_usage = "0"

        data = {
            "id": str(self.bot.user.id),
            "key": self.statcord_key,
            "servers": str(len(self.bot.guilds)),  # server count
            "users": str(self._get_user_count()),  # user count
            "commands": str(self._command_count),  # command count
            "active": list(self._active_users),
            "popular": [{"name": k, "count": v} for k, v in self._popular_commands.items()],  # active commands
            "memactive": mem_used,
            "memload": mem_load,
            "cpuload": cpu_load,
            "bandwidth": period_net_usage,
        }

        custom_1_value = await self._call_custom_graph(self.custom_1)
        custom_2_value = await self._call_custom_graph(self.custom_2)

        if custom_1_value is not None:
            data["custom1"] = custom_1_value

        if custom_2_value is not None:
            data["custom2"] = custom_2_value

        # reset counters
        self._popular_commands = defaultdict(int)
        self._command_count = 0
        self._active_users = set()

        # actually send the post request
        resp = await self._aiohttp_ses.post(url=STAT_ENDPOINT, json=data, headers=HEADERS)

        # handle server response
        if resp.status == 429:
            self.logger.warning("Statcord is ratelimiting us.")
        elif resp.status != 200:
            raise Exception(f"Statcord server response status was not 200 OK (Was {resp.status}):\n{await resp.text()}")
        else:
            self.logger.debug("Successfully posted stats to Statcord.")
