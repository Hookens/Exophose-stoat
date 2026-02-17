# Copyright (C) 2026 Hookens
# See the LICENSE file in the project root for details.

from stoat.ext import commands
from stoat.ext.commands import Bot, Context

from Debug.debughelpers import try_func_async
from Utilities.constants import HelpTexts
from Utilities.gears import get_gear

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Help.helpmethods import HelpMethods

class HelpCommands(commands.Gear):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.server_only()
    @commands.command(name="help", description=HelpTexts.C_HELP)
    @try_func_async()
    async def slash_help(
            self,
            ctx: Context):
        methods = get_gear(self.bot, HelpMethods)

        await ctx.channel.send(embeds=[await methods.generate_help()])


def setup(bot: Bot):
    bot.add_gear(HelpCommands(bot))