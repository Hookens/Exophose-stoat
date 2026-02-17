# Copyright (C) 2026 Hookens
# See the LICENSE file in the project root for details.

from stoat.ext import commands
from stoat.ext.commands import Bot, Context
from stoat.server import Role

from Debug.debughelpers import try_func_async
from Utilities.constants import AdminTexts
from Utilities.gears import get_gear

from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from Admin.adminmethods import AdminMethods
    from Utilities.embeds import Embeds

class AdminCommands(commands.Gear):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.server_only()
    @commands.slash_command(name="allow", description=AdminTexts.C_ALLOW)
    @try_func_async()
    async def slash_allow(
            self,
            ctx: Context,
            role: Role,
            max_roles: int):
        methods = get_gear(self.bot, AdminMethods)
        
        await ctx.channel.send(embeds=[await methods.allow_role(ctx.server, ctx.author, role, max_roles)])

    @commands.server_only()
    @commands.slash_command(name="disallow", description=AdminTexts.C_DISALLOW)
    @try_func_async()
    async def slash_disallow(
            self,
            ctx: Context,
            role: Role):
        methods = get_gear(self.bot, AdminMethods)
        
        await ctx.channel.send(embeds=[await methods.disallow_role(ctx.server, role)])

    @commands.server_only()
    @commands.slash_command(name="allowed", description=AdminTexts.C_ALLOWED)
    @try_func_async()
    async def slash_allowedroles(
            self,
            ctx: Context,
            public: Optional[bool] = False):
        embeds = get_gear(self.bot, Embeds)
        
        await ctx.channel.send(embeds=[await embeds.allowed_roles(ctx.server.id)])

def setup(bot: Bot):
    bot.add_gear(AdminCommands(bot))