# Copyright (C) 2026 Hookens
# See the LICENSE file in the project root for details.

from stoat.ext import commands
from stoat.ext.commands import Bot, Context, Gear

from Utilities.constants import HelpTexts

from Debug.debughelpers import try_func_async
from Utilities.gears import get_gear

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Help.helpmethods import HelpMethods


class HelpCommands(Gear):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.server_only()
    @commands.command(name="help", description=HelpTexts.C_HELP)
    @try_func_async()
    async def handle_help(self, ctx: Context, menu: str = ""):
        methods: "HelpMethods" = get_gear(self.bot, "HelpMethods")

        await ctx.message.reply(embeds=[await methods.generate_help(menu)])


async def setup(bot: Bot):
    await bot.add_gear(HelpCommands(bot))
