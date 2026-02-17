# Copyright (C) 2026 Hookens
# See the LICENSE file in the project root for details.

from stoat.ext.commands import Bot
from stoat.ext import commands
from stoat import TextEmbed

from Debug.debughelpers import try_func_async
from Utilities.constants import DebugLists, LoggingDefaults, EmbedDefaults
from Utilities.gears import get_gear

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Utilities.embeds import Embeds

class DebugMethods(commands.Gear):
    def __init__(self, bot: Bot):
        self.bot = bot

    @try_func_async(embed=True)
    async def reload_gear(self, gear_name: str) -> TextEmbed:
        embeds = get_gear(self.bot, Embeds)

        try:
            self.bot.unload_extension(gear_name)
        except:
            pass

        try:
            self.bot.load_extension(gear_name)
        except:
            return embeds.gear_restart_error(gear_name)
        
        return embeds.gear_restarted(gear_name)

    @try_func_async(embed=True)
    async def gear_status(self) -> TextEmbed:
        embeds = get_gear(self.bot, Embeds)
        
        embed: TextEmbed = embeds.generate_embed("Gear Statuses", "", EmbedDefaults.STYLE)

        gear_dict = {}
        for gear in DebugLists.GEARS:
            gear_dict[gear] = self.bot.get_gear(gear)
            
        admin_gears = {k:v for (k,v) in gear_dict.items() if "Admin" in k}
        bundle_gears = {k:v for (k,v) in gear_dict.items() if "Bundle" in k}
        debug_gears = {k:v for (k,v) in gear_dict.items() if "Debug" in k}
        help_gears = {k:v for (k,v) in gear_dict.items() if "Help" in k}
        user_gears = {k:v for (k,v) in gear_dict.items() if "User" in k}
        other_gears = {k:v for (k,v) in gear_dict.items() if "Admin" not in k and "Bundle" not in k and "Debug" not in k and "Help" not in k and "User" not in k}

        adminfields = ''.join([f"{'🟢' if v is not None else '🔴' } {k}\n" for (k,v) in admin_gears.items()])
        bundlefields = ''.join([f"{'🟢' if v is not None else '🔴' } {k}\n" for (k,v) in bundle_gears.items()])
        debugfields = ''.join([f"{'🟢' if v is not None else '🔴' } {k}\n" for (k,v) in debug_gears.items()])
        helpfields = ''.join([f"{'🟢' if v is not None else '🔴' } {k}\n" for (k,v) in help_gears.items()])
        userfields = ''.join([f"{'🟢' if v is not None else '🔴' } {k}\n" for (k,v) in user_gears.items()])
        otherfields = ''.join([f"{'🟢' if v is not None else '🔴' } {k}\n" for (k,v) in other_gears.items()])

        #embed.add_field(name="Admin", value=adminfields, inline=False)
        #embed.add_field(name="Bundle", value=bundlefields, inline=False)
        #embed.add_field(name="Debug", value=debugfields, inline=False)
        #embed.add_field(name="Help", value=helpfields, inline=False)
        #embed.add_field(name="User", value=userfields, inline=False)
        #embed.add_field(name="Utilities", value=otherfields, inline=False)
        #embed.add_field(name="Server Count", value=f"Serving {len(self.bot.servers)} servers")
        
        embed.description = f"{len(self.bot.gears)} of {LoggingDefaults.GEAR_COUNT} gears working."

        return embed



def setup(bot: Bot):
    bot.add_gear(DebugMethods(bot))