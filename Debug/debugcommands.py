# Copyright (C) 2026 Hookens
# See the LICENSE file in the project root for details.

from stoat.ext import commands
from stoat.ext.commands import Bot, Context, Gear
from stoat import TextChannel

from Commands.help import DebugHelp
from Utilities.constants import DebugTexts
from Utilities.datahelpers import Parameter

from Debug.debughelpers import try_func_async
from Utilities.gears import get_gear

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Commands.handling import Handling
    from Debug.debugmethods import DebugMethods


class DebugCommands(Gear):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.server_only()
    @commands.is_owner()
    @commands.command(name="announce", description=DebugTexts.C_ANNOUNCE)
    @try_func_async()
    async def handle_announce(
        self,
        ctx: Context,
        title: str = None,
        description: str = None,
        channel: TextChannel = None,
    ):
        methods: "DebugMethods" = get_gear(self.bot, "DebugMethods")
        handling: "Handling" = get_gear(self.bot, "Handling")

        embed = await handling.handle_command(
            methods.generate_announcement,
            DebugHelp.get_announce_help,
            Parameter("title", title, expected_type=str, required=True, min=1, max=100),
            Parameter(
                "description",
                description,
                expected_type=str,
                required=True,
                min=1,
                max=1024,
            ),
        )

        channel = channel or ctx.channel

        await channel.send(embeds=[embed])
        await ctx.message.reply(content="Announcement created.")

    @commands.server_only()
    @commands.is_owner()
    @commands.command(name="shutdown", description=DebugTexts.C_SHUTDOWN)
    @try_func_async()
    async def handle_shutdown(self, ctx: Context):

        await ctx.message.reply(content="Shutting down.")

        exit(1)

    @commands.server_only()
    @commands.is_owner()
    @commands.command(name="reload", description=DebugTexts.C_RELOAD)
    @try_func_async()
    async def handle_reload(self, ctx: Context, gear: str = None):
        methods: "DebugMethods" = get_gear(self.bot, "DebugMethods")

        await ctx.message.reply(embeds=[await methods.reload_gear(gear)])

    @commands.server_only()
    @commands.is_owner()
    @commands.command(name="status", description=DebugTexts.C_STATUS)
    @try_func_async()
    async def handle_status(self, ctx: Context):
        methods: "DebugMethods" = get_gear(self.bot, "DebugMethods")

        await ctx.message.reply(embeds=[await methods.gear_status()])


async def setup(bot: Bot):
    await bot.add_gear(DebugCommands(bot))
