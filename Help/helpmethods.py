# Copyright (C) 2026 Hookens
# See the LICENSE file in the project root for details.

from stoat.ext.commands import Bot, Gear
from stoat.message import SendableEmbed

from Utilities.constants import (
    HelpDefaults,
    AdminTexts,
    UserTexts,
    BundleTexts,
    Limits,
)

from Debug.debughelpers import try_func_async
from Utilities.gears import get_gear

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Utilities.embeds import Embeds


class HelpMethods(Gear):
    def __init__(self, bot: Bot):
        self.bot = bot

    @try_func_async(embed=True)
    async def generate_help(self, menu: str = "") -> SendableEmbed:
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        menu = menu.upper()

        if menu == HelpDefaults.Menus.CUSTOM_ROLES:
            embed = self.generate_help_custom_roles()
        elif menu == HelpDefaults.Menus.BUNDLE_ROLES:
            embed = self.generate_help_bundle_roles()
        elif menu == HelpDefaults.Menus.CUSTOM_CONFIG:
            embed = self.generate_help_custom_configuration()
        elif menu == HelpDefaults.Menus.BUNDLE_CONFIG:
            embed = self.generate_help_bundle_configuration()
        else:
            embed = self.generate_help_about_exophose()

        embeds.set_author(embed, developed=True)
        return embed

    def generate_help_about_exophose(self) -> SendableEmbed:
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        embed = embeds.generate_embed(
            title="About Exophose",
            description="Exophose is a simple role management bot that allows users to create custom roles for themselves and/or select roles from bundles, depending on the configuration.",
            color=HelpDefaults.COLOR,
        )

        embed.description += f"\n\n**Support server** • {HelpDefaults.SUPPORT_SERVER}\n**Invite Exophose** • {HelpDefaults.BOT_INVITE}\n**Support my work** • {HelpDefaults.SUPPORT_ME}\n**Source code** • {HelpDefaults.SOURCE_CODE}\n\nCall the help command with the highlit characters to view a help submenu and its commands, e.g. `{HelpDefaults.PREFIX}help cc`."

        embeds.add_field(
            embed,
            "`CC` Custom Configuration",
            "Configure what roles have access to complete customization.",
        )
        embeds.add_field(
            embed,
            "`BC` Bundle Configuration",
            "Configure bundles, what roles are allowed to use them, and what roles they offer.",
        )
        embeds.add_field(
            embed,
            "`CR` Custom Roles",
            "Manage your custom roles. Create, update and remove them to your liking.",
        )
        embeds.add_field(
            embed,
            "`BR` Bundle Roles",
            "List the customization roles that are available to you and choose your favorite.",
        )
        embeds.add_field(
            embed,
            "Limitations",
            "Stoat limits roles to 200 per server, plan ahead accordingly.",
            "#####",
        )

        return embed

    def generate_help_custom_configuration(self) -> SendableEmbed:
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        embed = embeds.generate_embed(
            title="Custom  •  Configuration",
            description="Commands for configuration of access to complete customization.",
            color=HelpDefaults.COLOR,
        )

        commands: str = (
            f"`allow` - {AdminTexts.C_ALLOW}\n"
            f"`disallow` - {AdminTexts.C_DISALLOW}\n"
            f"`allowed` - {AdminTexts.C_ALLOWED}\n"
        )
        tips: str = (
            f"- The maximum roles can be edited by re-allowing a role.\n"
            f"- A maximum of {Limits.ALLOW_LIMIT} roles can be allowed.\n"
            f"- A maximum of {Limits.CREATE_LIMIT} be configured for the creation limit."
        )

        embeds.add_field(embed, "Commands", commands)
        embeds.add_field(embed, "Tips", tips, "#####")

        return embed

    def generate_help_custom_roles(self) -> SendableEmbed:
        embeds: "Embeds" = get_gear(self.bot, "Embeds")

        embed = embeds.generate_embed(
            title="Custom  •  Roles",
            description="Commands for custom role management.",
            color=HelpDefaults.COLOR,
        )

        commands: str = (
            f"`create` - {UserTexts.C_CREATE}\n"
            f"`created` - {UserTexts.C_CREATED}\n"
            f"`recolor` - {UserTexts.C_RECOLOR}\n"
            # f"`rebadge` - {UserTexts.C_REBADGE}\n"
            f"`rename` - {UserTexts.C_RENAME}\n"
            f"`remove` - {UserTexts.C_REMOVE}\n"
        )
        tips: str = "- Colors use hexadecimal format (#FFFFFF)."

        embeds.add_field(embed, "Commands", commands)
        embeds.add_field(embed, "Tips", tips, "#####")

        return embed

    def generate_help_bundle_configuration(self) -> SendableEmbed:
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        embed = embeds.generate_embed(
            title="Bundle  •  Configuration",
            description="Commands for configuration of access to bundles and their selection.",
            color=HelpDefaults.COLOR,
        )

        howto: str = (
            "How to bundle with Exophose:\n"
            "1. Create a bundle.\n"
            "2. Add roles to the bundle.\n"
            "3. Allow roles to use it.\n"
            "4. Profit."
        )
        commands: str = (
            f"`bundle create` - {BundleTexts.C_CREATE}\n"
            f"`bundle list` - {BundleTexts.C_LIST}\n"
            f"`bundle allow` - {BundleTexts.C_ALLOW}\n"
            f"`bundle disallow` - {BundleTexts.C_DISALLOW}\n"
            f"`bundle edit` - {BundleTexts.C_EDIT}\n"
            f"`bundle delete` - {BundleTexts.C_DELETE}\n"
        )
        tips: str = (
            f"- A maximum of {Limits.BUNDLE_LIMIT} bundles can be created.\n"
            f"- A maximum of {Limits.BUNDLE_ALLOW_LIMIT} roles can be allowed per bundle.\n"
            f"- A maximum of {Limits.BUNDLE_ROLE_LIMIT} roles can be added per bundle."
        )

        embeds.add_field(embed, "Setup", howto)
        embeds.add_field(embed, "Commands", commands)
        embeds.add_field(embed, "Tips", tips, "#####")

        return embed

    def generate_help_bundle_roles(self) -> SendableEmbed:
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        embed = embeds.generate_embed(
            title="Bundle  •  Roles",
            description="Commands for bundle role selection.",
            color=HelpDefaults.COLOR,
        )

        commands: str = (
            f"`bundle choices` - {BundleTexts.C_CHOICES}\n"
            f"`bundle choose` - {BundleTexts.C_CHOOSE}\n"
        )

        embeds.add_field(embed, "Commands", commands)

        return embed


async def setup(bot: Bot):
    await bot.add_gear(HelpMethods(bot))
