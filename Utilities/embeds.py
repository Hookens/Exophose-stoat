# Copyright (C) 2026 Hookens
# See the LICENSE file in the project root for details.

import requests
import os
from stoat import Upload
from stoat.ext.commands import Bot, Gear
from stoat.message import Message, SendableEmbed
from stoat.server import Member, Role, Server
from PIL import Image, ImageDraw, ImageFilter

from Debug.debughelpers import try_func_async
from Utilities.constants import EmbedDefaults, Identity
from Utilities.datahelpers import Bundle, BundleRole, AllowedRole, CreatedRole
from Utilities.gears import get_gear

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from Utilities.data import Data
    from Utilities.utilities import Utilities


class Embeds(Gear):
    def __init__(self, bot: Bot):
        self.bot = bot

    def generate_embed(
        self,
        title: str,
        description: str,
        color: int = EmbedDefaults.FAILURE,
        image: str = None,
        footer: str = None,
        **kwargs,
    ) -> SendableEmbed:
        embed = SendableEmbed(title=title, description=description, color=color)
        if image is not None:
            embed.icon_url = image

        for key, value in kwargs.items():
            self.add_field(embed, key, value)

        if footer is not None:
            self.set_footer(embed, footer)

        return embed

    def add_field(
        self, embed: SendableEmbed, name: str, value: str, heading: Optional[str] = None
    ):
        embed.description += f"\n\n{heading or "####"} {name}\n{value}"

    def set_footer(self, embed: SendableEmbed, text: str):
        embed.description += f"\n\n###### {text}"

    def set_author(self, embed: SendableEmbed, developed: bool = False):
        self.set_footer(
            embed,
            f"{Identity.EMOTE} {"Developed by " if developed else ""}{Identity.NAME}",
        )

    def blacklisted_word(self) -> SendableEmbed:
        return self.generate_embed(
            "Blacklisted word",
            "The name must not contain excessively profane or offensive words.",
        )

    def creation_success(self) -> SendableEmbed:
        return self.generate_embed(
            "Role creation success",
            f"Exophose successfully created your new role.",
            EmbedDefaults.SUCCESS,
        )

    def maximum_roles(self) -> SendableEmbed:
        return self.generate_embed(
            "Maximum roles", "Maximum number of roles reached for your allowed role."
        )

    def maximum_allowed_roles(self) -> SendableEmbed:
        return self.generate_embed(
            "Maximum allowed roles",
            "Maximum number of allowed roles reached for your server.",
        )

    def maximum_bundles(self) -> SendableEmbed:
        return self.generate_embed(
            "Maximum bundles", "Maximum number of bundles reached for your server."
        )

    # Admin
    def allowed_role_added(self, role: Role) -> SendableEmbed:
        return self.generate_embed(
            "Configuration changed",
            f"Exophose allowed <%{role.id}> to use role management commands.",
            color=EmbedDefaults.SUCCESS,
        )

    def allowed_role_updated(self, role: Role) -> SendableEmbed:
        return self.generate_embed(
            "Configuration changed",
            f"Exophose updated the permissions for <%{role.id}>.",
            EmbedDefaults.SUCCESS,
        )

    def allowed_role_removed(self, role: Role) -> SendableEmbed:
        return self.generate_embed(
            "Configuration changed",
            f"Exophose disallowed <%{role.id}> from using role management commands.",
            EmbedDefaults.SUCCESS,
        )

    def allowed_role_error(self, role: Role) -> SendableEmbed:
        return self.generate_embed(
            "Unable to allow role",
            f"Exophose cannot allow <%{role.id}>. You have reached the maximum of 20 allowed roles.",
        )

    def allowed_role_missing(self, role: Role) -> SendableEmbed:
        return self.generate_embed(
            "Unable to disallow role",
            f"Exophose cannot disallow <%{role.id}> as it is already disallowed.",
        )

    @try_func_async(embed=True)
    async def allowed_roles(self, server_id: str) -> SendableEmbed:
        data: "Data" = get_gear(self.bot, "Data")

        allowed_roles: list[AllowedRole] = await data.get_allowed_roles(server_id)

        if not any(allowed_roles):
            return self.generate_embed(
                "Allowed roles",
                "Your server has no allowed roles.",
                EmbedDefaults.STYLE,
            )

        embed = self.generate_embed(
            "Allowed roles",
            "Here is a list of the allowed roles in your server.",
            EmbedDefaults.STYLE,
        )

        for allowed_role in allowed_roles:
            ping = (
                "**everyone**" if allowed_role.is_everyone else f"<%{allowed_role.id}>"
            )
            role_plural = "s" if allowed_role.max_roles > 1 else ""
            max_roles = f"**{allowed_role.max_roles}** role{role_plural}"
            # not_badges = ":white_check_mark:" if allowed_role.allow_badges else ":no_entry_sign:"
            # not_gradients = ":white_check_mark:" if allowed_role.allow_gradients else ":no_entry_sign:"
            # allow_badges = f"{not_badges} custom badges"
            # allow_gradients = f"{not_gradients} enhanced role styles"
            allowed_by = f"Allowed by <@{allowed_role.user_id}> on **<t:{int(allowed_role.created_date.timestamp())}>**"
            updated_by = (
                f"\nLast update by <@{allowed_role.updated_user_id}> on **<t:{int(allowed_role.updated_date.timestamp())}>**"
                if allowed_role.updated_user_id is not None
                else ""
            )
            field = f"{ping} | {max_roles}\n{allowed_by}{updated_by}"

            self.add_field(embed, "\u200b", field)

        return embed

    # User
    @try_func_async(embed=True)
    async def created_roles(self, server: Server, member: Member) -> SendableEmbed:
        data: "Data" = get_gear(self.bot, "Data")

        created_roles: list[CreatedRole] = await data.get_member_roles(
            member.server_id, member.id
        )

        if not any(created_roles):
            return self.generate_embed(
                "Created roles",
                f"{member.mention} has not created any roles.",
                EmbedDefaults.STYLE,
            )

        embed = self.generate_embed(
            "Created roles",
            f"Here is a list of the created roles for {member.mention}.",
            EmbedDefaults.STYLE,
        )

        i: int = 0
        for created_role in created_roles:
            role: Role = await server.fetch_role(created_role.id)
            index = f"Index: `{i + 1}`"
            ping = f"<%{role.id}>"
            # badge = f" | [View badge]({role.icon.url})" if role.icon is not None else ""
            created_date = (
                f"Created on **<t:{int(created_role.created_date.timestamp())}>**"
            )
            field = f"{index} | {ping} | {role.color or "No color"}\n{created_date}"

            self.add_field(embed, f"\u200b", field)
            i += 1

        return embed

    def success_modification(self, action: str) -> SendableEmbed:
        return self.generate_embed(
            f"Role {action} successful",
            f"Exophose successfully {action}{'d' if action.endswith('e') else 'ed'} your role.",
            EmbedDefaults.SUCCESS,
        )

    def missing_modification_index(self, action: str) -> SendableEmbed:
        return self.generate_embed(
            f"Role {action} failed",
            f"You must specify a valid index for the role you want to {action}.",
        )

    def missing_modification_role(self, action: str) -> SendableEmbed:
        return self.generate_embed(
            f"Role {action} impossible",
            f"Exophose cannot {action} your custom role as you do not have one.",
        )

    # Errors
    def unexpected_error(self) -> SendableEmbed:
        return self.generate_embed(
            "Unexpected error",
            f"Exophose encountered an unexpected error. The developer has been notified. Apologies for the inconvenience.",
        )

    def unexpected_sql_error(self) -> SendableEmbed:
        return self.generate_embed(
            "Unexpected error",
            f"Exophose encountered an unexpected error with the database. Impossible to complete this action at the moment. Apologies for the inconvenience.",
        )

    # Verification
    def not_user_allowed(self) -> SendableEmbed:
        return self.generate_embed(
            "User not allowed",
            "You are not allowed to create custom roles for yourself as you have none of the allowed roles.",
        )

    def not_badge_allowed(self) -> SendableEmbed:
        return self.generate_embed(
            "User not allowed",
            "You are not allowed to set custom badges with your currently allowed role(s).",
        )

    def not_file_allowed(self) -> SendableEmbed:
        return self.generate_embed(
            "Invalid file",
            "The file you have provided is invalid. Make sure it's an image file type supported by stoat (.png, .jpg, .webp).",
        )

    def not_role_allowed(self, role: Role) -> SendableEmbed:
        return self.generate_embed(
            "Permission error", f"Exophose is unable to grant <%{role.id}>."
        )

    def not_edit_allowed(self, role: Role, action: str) -> SendableEmbed:
        return self.generate_embed(
            "Permission error",
            f"Exophose cannot {action} <%{role.id}>. It might be too high in the hierarchy, or your custom color argument was invalid.",
        )

    def not_feature_allowed(self) -> SendableEmbed:
        return self.generate_embed(
            "Missing feature",
            "Your server does not have role bages unlocked as they are a level 2 boost feature.",
        )

    # Bundle
    def not_bundle_allowed(self) -> SendableEmbed:
        return self.generate_embed(
            "User not allowed", "You are not allowed to use any of the bundles."
        )

    def no_bundle_roles(self) -> SendableEmbed:
        return self.generate_embed(
            "User not allowed", "You are not allowed to use any of the bundles."
        )

    def bundle_created(self, name: str) -> SendableEmbed:
        return self.generate_embed(
            "Bundle created",
            f"Exophose created a new bundle named {name}.",
            color=EmbedDefaults.SUCCESS,
        )

    def bundle_deleted(self) -> SendableEmbed:
        return self.generate_embed(
            "Bundle deleted",
            f"Exophose deleted the bundle.",
            color=EmbedDefaults.SUCCESS,
        )

    def bundle_role_selected(self, role: Role) -> SendableEmbed:
        return self.generate_embed(
            "Role selected",
            f"Exophose granted you <%{role.id}>.",
            color=EmbedDefaults.SUCCESS,
        )

    def bundle_missing_index(self, action: str) -> SendableEmbed:
        return self.generate_embed(
            f"Bundle {action} invalid",
            f"You must specify a valid index for the bundle you want to {action}.",
        )

    def bundle_missing_choice_index(self) -> SendableEmbed:
        return self.generate_embed(
            f"Role selection invalid",
            f"You must specify a valid index for the role you want to choose.",
        )

    def bundle_selection_invalid(self) -> SendableEmbed:
        return self.generate_embed(
            f"Bundle selection invalid",
            f"You must enter the matching index and name of the bundle to confirm its deletion.",
        )

    def bundle_allowed_role_added(self, role: Role) -> SendableEmbed:
        return self.generate_embed(
            "Bundle allowed role added",
            f"Exophose allowed <%{role.id}> in the bundle.",
            color=EmbedDefaults.SUCCESS,
        )

    def bundle_allowed_role_removed(self, role: Role) -> SendableEmbed:
        return self.generate_embed(
            "Bundle allowed role removed",
            f"Exophose disallowed <%{role.id}> from the bundle.",
            color=EmbedDefaults.SUCCESS,
        )

    def bundle_allowed_role_present(self, role: Role) -> SendableEmbed:
        return self.generate_embed(
            "Bundle role allow impossible",
            f"Exophose cannot allow <%{role.id}> in the bundle as it is already allowed.",
        )

    def bundle_allowed_role_missing(self, role: Role) -> SendableEmbed:
        return self.generate_embed(
            "Bundle role disallow impossible",
            f"Exophose cannot disallow <%{role.id}> from the bundle as it is already disallowed.",
        )

    def bundle_allowed_role_error(self, role: Role) -> SendableEmbed:
        return self.generate_embed(
            "Bundle role allow impossible",
            f"Exophose cannot allow <%{role.id}> in the bundle. You have reached the maximum of 10 roles.",
        )

    def bundle_role_added(self, role: Role) -> SendableEmbed:
        return self.generate_embed(
            "Bundle role added",
            f"Exophose added <%{role.id}> to the bundle.",
            color=EmbedDefaults.SUCCESS,
        )

    def bundle_role_removed(self, role: Role) -> SendableEmbed:
        return self.generate_embed(
            "Bundle role removed",
            f"Exophose removed <%{role.id}> from the bundle.",
            color=EmbedDefaults.SUCCESS,
        )

    def bundle_role_present(self, role: Role) -> SendableEmbed:
        return self.generate_embed(
            "Bundle role add impossible",
            f"Exophose cannot add <%{role.id}> to the bundle as it is already present.",
        )

    def bundle_role_missing(self, role: Role) -> SendableEmbed:
        return self.generate_embed(
            "Bundle role remove impossible",
            f"Exophose cannot remove <%{role.id}> from the bundle as it is already not present.",
        )

    def bundle_role_error(self, role: Role) -> SendableEmbed:
        return self.generate_embed(
            "Bundle role add impossible",
            f"Exophose cannot add <%{role.id}> to the bundle. You have reached the maximum of 10 roles.",
        )

    @try_func_async(embed=True)
    async def bundle_list(self, server_id: str) -> SendableEmbed:
        data: "Data" = get_gear(self.bot, "Data")

        bundles: list[Bundle] = await data.get_bundles(server_id)

        if not any(bundles):
            return self.generate_embed(
                "Created bundles",
                f"There are no created bundles in your server.",
                EmbedDefaults.STYLE,
            )

        embed = self.generate_embed(
            "Created bundles",
            f"Here is a list of the bundles in your server.",
            EmbedDefaults.STYLE,
        )

        i: int = 0
        for bundle in bundles:
            bundle_allowed_roles: list[BundleRole] = (
                await data.get_bundle_allowed_roles(bundle.id)
            )
            bundle_roles: list[BundleRole] = await data.get_bundle_roles(bundle.id)

            field = ""
            has_allowed_roles = any(bundle_allowed_roles)
            has_roles = any(bundle_roles)

            if has_allowed_roles or has_roles:
                if has_roles:
                    field += "Roles:\n"
                    for bundle_role in bundle_roles:
                        field += f"> <%{bundle_role.id}>\n"

                if has_allowed_roles:
                    field += "Allowed Roles:\n"
                    for bundle_allowed_role in bundle_allowed_roles:
                        field += f"> <%{bundle_allowed_role.id}>\n"
            else:
                field = "No roles were allowed or added yet."

            self.add_field(embed, f"{i + 1} | {bundle.name}", field)
            i += 1

        return embed

    @try_func_async(embed=True)
    async def bundle_choices(self, allowed_roles: list[BundleRole]) -> SendableEmbed:
        data: "Data" = get_gear(self.bot, "Data")

        embed = self.generate_embed(
            "Role choices",
            f"These are the roles you have access to.",
            EmbedDefaults.STYLE,
        )

        bundle_roles: list[int] = await data.get_bundles_choices(allowed_roles)

        field = ""
        i: int = 0
        for bundle_role in bundle_roles:
            field += f"`{i + 1}` | <%{bundle_role}>\n"
            i += 1

        self.add_field(embed, "Available roles", field)

        return embed

    # Debug
    def gear_restarted(self, gear: str) -> SendableEmbed:
        return self.generate_embed(
            "Gear restarted",
            f"`{gear}` was successfully restarted.",
            color=EmbedDefaults.SUCCESS,
        )

    def gear_restart_error(self, gear: str) -> SendableEmbed:
        return self.generate_embed(
            "Gear restart failed", f"`{gear}` could not be restarted."
        )

    def gear_not_found(self, gear: str) -> SendableEmbed:
        return self.generate_embed(
            "Gear not found",
            f"`{gear}` was not found. Double-check the name and refer to the gear list.",
        )


async def setup(bot: Bot):
    await bot.add_gear(Embeds(bot))
