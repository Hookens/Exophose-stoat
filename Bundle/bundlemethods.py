# Copyright (C) 2026 Hookens
# See the LICENSE file in the project root for details.

from stoat.ext.commands import Bot, Gear
from stoat.message import SendableEmbed
from stoat.server import Member, Role, Server

from Utilities.constants import BundleTexts, Indicators

from Debug.debughelpers import try_func_async
from Utilities.gears import get_gear

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Utilities.data import Data
    from Utilities.embeds import Embeds
    from Utilities.verification import Verification


class BundleMethods(Gear):
    def __init__(self, bot: Bot):
        self.bot = bot

    @try_func_async(embed=True)
    async def bundle_create(self, server: Server, name: str) -> SendableEmbed:
        data: "Data" = get_gear(self.bot, "Data")
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        verification: "Verification" = get_gear(self.bot, "Verification")

        if not verification.is_name_allowed(name):
            return embeds.blacklisted_word()

        if await data.count_bundles(server.id) >= 5:
            return embeds.maximum_bundles()

        if await data.add_bundle(server.id, name):
            return embeds.bundle_created(name)

        return embeds.unexpected_sql_error()

    @try_func_async(embed=True)
    async def bundle_list(self, server_id: str) -> SendableEmbed:
        embeds: "Embeds" = get_gear(self.bot, "Embeds")

        return await embeds.bundle_list(server_id)

    @try_func_async(embed=True)
    async def bundle_edit(
        self, server: Server, index: int, role: Role, action: str
    ) -> SendableEmbed:
        data: "Data" = get_gear(self.bot, "Data")
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        verification: "Verification" = get_gear(self.bot, "Verification")

        index -= 1

        if not (0 <= index < await data.count_bundles(server.id)):
            return embeds.bundle_missing_index("edit")

        addable = await verification.is_bundle_role_addable(role.id, server.id, index)

        if action == BundleTexts.CHOICES[0]:
            if not verification.is_name_allowed(role.name):
                return embeds.blacklisted_word()

            if addable == 1:
                if await data.add_bundle_role(role.id, server.id, index):
                    return embeds.bundle_role_added(role)
            elif addable == 0:
                return embeds.bundle_role_present(role)
            else:
                return embeds.bundle_role_error(role)

        else:
            if addable == 1:
                return embeds.bundle_role_missing(role)
            else:
                if await data.delete_bundle_role(role.id, server.id, index):
                    return embeds.bundle_role_removed(role)

        return embeds.unexpected_sql_error()

    @try_func_async(embed=True)
    async def bundle_delete(
        self, server: Server, index: int, name: str
    ) -> SendableEmbed:
        data: "Data" = get_gear(self.bot, "Data")
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        verification: "Verification" = get_gear(self.bot, "Verification")

        index -= 1

        if not (0 <= index < await data.count_bundles(server.id)):
            return embeds.bundle_missing_index("delete")

        if not await verification.is_bundle_selection_valid(server.id, index, name):
            return embeds.bundle_selection_invalid()

        if await data.delete_bundle(server.id, index):
            return embeds.bundle_deleted()

        return embeds.unexpected_sql_error()

    @try_func_async(embed=True)
    async def bundle_allow(
        self, server: Server, index: int, role: Role
    ) -> SendableEmbed:
        data: "Data" = get_gear(self.bot, "Data")
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        verification: "Verification" = get_gear(self.bot, "Verification")

        index -= 1

        if not (0 <= index < await data.count_bundles(server.id)):
            return embeds.bundle_missing_index("allow")

        if not verification.is_name_allowed(role.name):
            return embeds.blacklisted_word()

        allowable: Indicators = await verification.is_bundle_allowed_role_allowable(
            role.id, server.id, index
        )
        if allowable == Indicators.ADDABLE:
            if await data.add_bundle_allowed_role(role.id, server.id, index):
                return embeds.bundle_allowed_role_added(role)
        elif allowable == Indicators.PRESENT:
            return embeds.bundle_allowed_role_present(role)
        else:
            return embeds.bundle_allowed_role_error(role)

        return embeds.unexpected_sql_error()

    @try_func_async(embed=True)
    async def bundle_disallow(
        self, server: Server, index: int, role: Role
    ) -> SendableEmbed:
        data: "Data" = get_gear(self.bot, "Data")
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        verification: "Verification" = get_gear(self.bot, "Verification")

        index -= 1

        if not (0 <= index < await data.count_bundles(server.id)):
            return embeds.bundle_missing_index("disallow")

        allowable = await verification.is_bundle_allowed_role_allowable(
            role.id, server.id, index
        )
        if allowable == Indicators.ADDABLE:
            return embeds.bundle_allowed_role_missing(role)
        else:
            if await data.delete_bundle_allowed_role(role.id, server.id, index):
                return embeds.bundle_allowed_role_removed(role)

        return embeds.unexpected_sql_error()

    @try_func_async(embed=True)
    async def bundle_choices(self, member: Member) -> SendableEmbed:
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        verification: "Verification" = get_gear(self.bot, "Verification")

        allowed_roles = await verification.get_allowed_bundle_roles(member)

        if not allowed_roles:
            return embeds.not_bundle_allowed()

        return await embeds.bundle_choices(allowed_roles)

    @try_func_async(embed=True)
    async def bundle_choose(
        self, server: Server, member: Member, index: int
    ) -> SendableEmbed:
        data: "Data" = get_gear(self.bot, "Data")
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        verification: "Verification" = get_gear(self.bot, "Verification")

        allowed_roles = await verification.get_allowed_bundle_roles(member)

        index -= 1

        if not allowed_roles:
            return embeds.not_bundle_allowed()
        
        # Remove this once backend gets overhauled with permissions to assign any lower role to anyone, including those with roles above us.
        if not verification.is_member_assignable(server.me, member):
            return embeds.not_assignable()

        if (
            not await verification.check_user_bundle_roles(allowed_roles, member, True)
        ) or (not (0 <= index < await data.count_bundles_choices(allowed_roles))):
            return embeds.bundle_missing_choice_index()

        chosen_role_id = await data.get_bundles_choice(allowed_roles, index)
        role: Role = await server.fetch_role(chosen_role_id)

        try:
            roles = set(member.role_ids)
            roles.add(role.id)
            await member.edit(roles=roles)
        except:
            return embeds.not_role_allowed(role)

        return embeds.bundle_role_selected(role)


async def setup(bot: Bot):
    await bot.add_gear(BundleMethods(bot))
