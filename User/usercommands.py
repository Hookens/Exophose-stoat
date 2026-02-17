# Copyright (C) 2026 Hookens
# See the LICENSE file in the project root for details.

from stoat.ext.commands import Context
from stoat.ext import commands
from stoat.ext.commands import Bot
from stoat.server import Member

from Debug.debughelpers import try_func_async
from Utilities.constants import UserTexts
from Utilities.gears import get_gear


from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from User.usermethods import UserMethods
    from Utilities.embeds import Embeds
    from Utilities.verification import Verification

class UserCommands(commands.Gear):
    def __init__(self, bot: Bot):
        self.bot = bot
    
    async def allowed(self, ctx: Context) -> bool:
        embeds = get_gear(self.bot, Embeds)
        verification = get_gear(self.bot, Verification)

        if not (allowed := await verification.is_user_allowed(ctx.author)):
            await ctx.channel.send(embeds=[embeds.not_user_allowed()])

        return allowed

    @commands.server_only()
    @commands.command(name="create", description=UserTexts.C_CREATE)
    @try_func_async()
    async def handle_create(
            self,
            ctx: Context,
            name: str,
            color: str):
        methods = get_gear(self.bot, UserMethods)

        if await self.allowed(ctx):
            await ctx.channel.send(embeds=[await methods.role_create(ctx.server, ctx.author, name, color)])

    @commands.server_only()
    @commands.command(name="remove", description=UserTexts.C_REMOVE)
    @try_func_async()
    async def handle_remove(
            self,
            ctx: Context,
            index: Optional[int] = 0):
        methods = get_gear(self.bot, UserMethods)

        if await self.allowed(ctx):
            await ctx.channel.send(embeds=[await methods.role_remove(ctx.server, ctx.author, index)])

    @commands.server_only()
    @commands.command(name="recolor", description=UserTexts.C_RECOLOR)
    @try_func_async()
    async def handle_recolor(
            self,
            ctx: Context,
            color: str,
            index: Optional[int] = 0):
        methods = get_gear(self.bot, UserMethods)

        if await self.allowed(ctx):
            await ctx.channel.send(embeds=[await methods.role_recolor(ctx.server, ctx.author, color, index)])

    @commands.server_only()
    @commands.command(name="rename", description=UserTexts.C_RENAME)
    @try_func_async()
    async def handle_rename(
            self,
            ctx: Context,
            name: str,
            index: Optional[int] = 0):
        methods = get_gear(self.bot, UserMethods)

        if await self.allowed(ctx):
            await ctx.channel.send(embeds=[await methods.role_rename(ctx.server, ctx.author, name, index)])

    #@commands.server_only()
    #@commands.command(name="rebadge", description=UserTexts.C_REBADGE)
    #@try_func_async()
    #async def handle_rebadge(
    #        self,
    #        ctx: Context,
    #        badge: Option(SlashCommandOptionType.attachment, UserTexts.F_BADGE, required=False) = None,
    #        index: Option(int, UserTexts.F_INDEX, min_value=0, max_value=19, required=False) = 0):
    #    methods = get_gear(self.bot, UserMethods)
    #
    #    if await self.allowed(ctx):
    #                await ctx.channel.send(embeds=[await methods.role_rebadge(ctx.server, ctx.author, badge, index)])

    @commands.server_only()
    @commands.command(name="created", description=UserTexts.C_CREATED)
    @try_func_async()
    async def handle_created(
            self,
            ctx: Context,
            member: Optional[Member] = None):
        embeds = get_gear(self.bot, Embeds)
        
        if await self.allowed(ctx):
            await ctx.channel.send(embeds=[await embeds.created_roles(member or ctx.author)])

    @commands.server_only()
    @commands.command(name="preview", description=UserTexts.C_PREVIEW)
    @try_func_async()
    async def handle_preview(
            self,
            ctx: Context,
            color: Optional[str] = None):
        embeds = get_gear(self.bot, Embeds)
        
        if await self.allowed(ctx):
            await ctx.channel.send(embeds=[await embeds.preview_color(ctx.author, color)])


def setup(bot: Bot):
    bot.add_gear(UserCommands(bot))