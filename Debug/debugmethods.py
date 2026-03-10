# Copyright (C) 2026 Hookens
# See the LICENSE file in the project root for details.

from stoat.ext.commands import Bot, Gear
from stoat.message import SendableEmbed

from Utilities.constants import DebugLists, EmbedDefaults, LoadOrder, LoggingDefaults

from Debug.debughelpers import try_func_async
from Utilities.gears import get_gear

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Utilities.embeds import Embeds


class DebugMethods(Gear):
    def __init__(self, bot: Bot):
        self.bot = bot

    @try_func_async(embed=True)
    async def generate_announcement(
        self, title: str, description: str
    ) -> SendableEmbed:
        embeds: "Embeds" = get_gear(self.bot, "Embeds")

        description = description.replace("\\n", "\n")
        embed = embeds.generate_embed(
            title=title, description=description, color=EmbedDefaults.STYLE
        )
        embeds.set_author(embed)

        return embed

    @try_func_async(embed=True)
    async def reload_gear(self, gear_name: str | None) -> SendableEmbed:
        embeds: "Embeds" = get_gear(self.bot, "Embeds")

        if gear_name not in LoadOrder.GEARS:
            return embeds.gear_not_found(gear_name)

        try:
            await self.bot.unload_extension(gear_name)
        except:
            pass

        try:
            await self.bot.load_extension(gear_name)
        except:
            return embeds.gear_restart_error(gear_name)

        return embeds.gear_restarted(gear_name)

    @try_func_async(embed=True)
    async def gear_status(self) -> SendableEmbed:
        embeds: "Embeds" = get_gear(self.bot, "Embeds")

        embed: SendableEmbed = embeds.generate_embed(
            "Gear Statuses", "", EmbedDefaults.STYLE
        )

        gear_dict = {}
        for gear in DebugLists.GEARS:
            gear_dict[gear] = self.bot.get_gear(gear)

        admin_gears = {k: v for (k, v) in gear_dict.items() if "Admin" in k}
        bundle_gears = {k: v for (k, v) in gear_dict.items() if "Bundle" in k}
        debug_gears = {k: v for (k, v) in gear_dict.items() if "Debug" in k}
        help_gears = {k: v for (k, v) in gear_dict.items() if "Help" in k}
        user_gears = {k: v for (k, v) in gear_dict.items() if "User" in k}
        other_gears = {
            k: v
            for (k, v) in gear_dict.items()
            if "Admin" not in k
            and "Bundle" not in k
            and "Debug" not in k
            and "Help" not in k
            and "User" not in k
        }

        adminfields = "".join(
            [
                f"{'🟢' if v is not None else '🔴' } {k}\n"
                for (k, v) in admin_gears.items()
            ]
        )
        bundlefields = "".join(
            [
                f"{'🟢' if v is not None else '🔴' } {k}\n"
                for (k, v) in bundle_gears.items()
            ]
        )
        debugfields = "".join(
            [
                f"{'🟢' if v is not None else '🔴' } {k}\n"
                for (k, v) in debug_gears.items()
            ]
        )
        helpfields = "".join(
            [
                f"{'🟢' if v is not None else '🔴' } {k}\n"
                for (k, v) in help_gears.items()
            ]
        )
        userfields = "".join(
            [
                f"{'🟢' if v is not None else '🔴' } {k}\n"
                for (k, v) in user_gears.items()
            ]
        )
        otherfields = "".join(
            [
                f"{'🟢' if v is not None else '🔴' } {k}\n"
                for (k, v) in other_gears.items()
            ]
        )

        embed.description = (
            f"{len(self.bot.gears)} of {LoggingDefaults.GEAR_COUNT} gears working."
        )

        embeds.add_field(embed, "Admin", adminfields)
        embeds.add_field(embed, "Bundle", bundlefields)
        embeds.add_field(embed, "Debug", debugfields)
        embeds.add_field(embed, "Help", helpfields)
        embeds.add_field(embed, "User", userfields)
        embeds.add_field(embed, "Utilities", otherfields)
        embeds.add_field(
            embed, "Server Count", f"Serving {len(self.bot.servers)} servers"
        )

        return embed


async def setup(bot: Bot):
    await bot.add_gear(DebugMethods(bot))
