# Copyright (C) 2026 Hookens
# See the LICENSE file in the project root for details.

from stoat.ext import commands
from stoat.ext.commands import Bot, Context
from stoat.message import SendableEmbed

from Debug.debughelpers import try_func_async
from Utilities.constants import DebugTexts, EmbedDefaults

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Debug.debugmethods import DebugMethods

class DebugCommands(commands.Gear):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.server_only()
    @commands.is_owner()
    @commands.command(name="announce", description=DebugTexts.C_ANNOUNCE)
    @try_func_async()
    async def handle_announce(
            self,
            ctx: Context,
            title: str,
            description: str):

        description = description.replace("\\n", "\n")
        embed: SendableEmbed = SendableEmbed(title=title, description=description, color=EmbedDefaults.STYLE)
        embed.icon_url=ctx.author.avatar.url()
        await ctx.channel.send(embeds=[embed])
        await ctx.channel.send(content="Announcement created.")

    @commands.server_only()
    @commands.is_owner()
    @commands.command(name="shutdown", description=DebugTexts.C_SHUTDOWN)
    @try_func_async()
    async def handle_shutdown(
            self,
            ctx: Context):
        
        await ctx.channel.send(content="Shutting down.")

        exit(1)

    @commands.server_only()
    @commands.is_owner()
    @commands.command(name="reload", description=DebugTexts.C_RELOAD)
    @try_func_async()
    async def handle_reload(
            self,
            ctx: Context,
            gear: str):
        
        methods: DebugMethods
        if (methods := self.bot.get_gear("DebugMethods")) is not None:
            await ctx.channel.send(embed=await methods.reload_gear(gear))
    
    @commands.server_only()
    @commands.is_owner()
    @commands.command(name="status", description=DebugTexts.C_STATUS)
    @try_func_async()
    async def handle_status(
            self,
            ctx: Context):
        
        methods: DebugMethods
        if (methods := self.bot.get_gear("DebugMethods")) is not None:
            await ctx.channel.send(embed=await methods.gear_status())



def setup(bot: Bot):
    bot.add_gear(DebugCommands(bot))