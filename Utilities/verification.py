# Copyright (C) 2026 Hookens
# See the LICENSE file in the project root for details.

from stoat.ext import commands
from stoat.ext.commands import Bot
from stoat.server import Server, Member

from Utilities.datahelpers import AllowedRole, Bundle, BundleRole
from Utilities.gears import get_gear
from Utilities.constants import Indicators, Limits

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Utilities.data import Data

class Verification(commands.Gear):
    def __init__(self, bot: Bot):
        self.bot = bot

    def has_permission(self, server: Server) -> bool:
        return server.me.server_permissions.manage_roles

    def is_name_allowed(self, name: str) -> bool:
        lowercase_words = set(name.lower().split())

        with open("Exophose/bannedwords.txt", "r") as file:
            banned_exact = set()
            banned_contained = set()

            for line in file:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("*"):
                    banned_contained.add(line[1:])
                else:
                    banned_exact.add(line)

        if lowercase_words & banned_exact:
            return False

        for word in lowercase_words:
            if any(banned in word for banned in banned_contained):
                return False

        return True


    #Custom roles
    async def is_role_allowable(self, role_id: int, server_id: int) -> tuple[Indicators, AllowedRole | None]:
        data = get_gear(self.bot, Data)
        
        allowed_roles: list[AllowedRole] = await data.get_allowed_roles(server_id)

        for allowed_role in allowed_roles:
            if allowed_role.id == role_id:
                return (Indicators.PRESENT, allowed_role)

        if len(allowed_roles) == Limits.ALLOW_LIMIT:
            return (Indicators.MAXIMUM_REACHED, None)
        
        return (Indicators.ADDABLE, None)

    async def is_user_role_addable(self, member: Member) -> bool:
        data = get_gear(self.bot, Data)
        
        created_count: int = await data.count_member_roles(member.server_id, member.id)

        if member.server_permissions.manage_roles:
            highest = Limits.CREATE_LIMIT
        else:
            allowed_roles: list[AllowedRole] = await data.get_allowed_roles(member.server_id)

            highest = max(
                (role.max_roles for role in allowed_roles if role.id in set(member.role_ids)),
                default=0
            )

        return created_count < highest

    async def is_user_within_max_roles(self, member: Member) -> bool:
        data = get_gear(self.bot, Data)
        
        created_count: int = await data.count_member_roles(member.server_id, member.id)

        if created_count == 0:
            return True

        allowed_roles: list[AllowedRole] = await data.get_allowed_roles(member.server_id)

        highest = max(
            (role.max_roles for role in allowed_roles if role.id in set(member.role_ids)),
            default=0
        )

        return created_count <= highest

    async def is_user_allowed(self, member: Member) -> bool:
        data = get_gear(self.bot, Data)
        
        if member.server_permissions.manage_roles:
            return True
        
        allowed_roles: list[AllowedRole] = await data.get_allowed_roles(member.server_id)

        return any(role.id in set(member.role_ids) for role in allowed_roles)

    #async def is_badge_allowed(self, member: Member) -> bool:
    #    data = get_gear(self.bot, Data)
    #    
    #    if member.server_permissions.manage_roles:
    #        return True
    #
    #    allowed_roles: list[AllowedRole] = await data.get_badge_allowed_roles(member.server_id)
    #
    #    return any(role.id in set(member.role_ids) for role in allowed_roles)

    #async def is_gradient_allowed(self, member: Member) -> bool:
    #    data = get_gear(self.bot, Data)
    #    
    #    if member.server_permissions.manage_roles:
    #        return True
    #
    #    allowed_roles: list[AllowedRole] = await data.get_gradient_allowed_roles(member.server_id)
    #
    #    return any(role.id in set(member.role_ids) for role in allowed_roles)

    #Bundles
    async def is_bundle_role_addable(self, role_id: int, server_id: int, index: int) -> Indicators:
        data = get_gear(self.bot, Data)
        
        bundle: Bundle = await data.get_bundle(server_id, index)
        bundle_roles: list[AllowedRole] = await data.get_bundle_roles(bundle.id)

        if any(r.id == role_id for r in bundle_roles):
            return Indicators.PRESENT

        if len(bundle_roles) == Limits.BUNDLE_ROLE_LIMIT:
            return Indicators.MAXIMUM_REACHED

        return Indicators.ADDABLE
    
    async def is_bundle_allowed_role_allowable(self, role_id: int, server_id: int, index: int) -> int:
        data = get_gear(self.bot, Data)
        
        bundle: Bundle = await data.get_bundle(server_id, index)
        bundle_roles: list[AllowedRole] = await data.get_allowed_bundle_roles(bundle.id)

        if any(r.id == role_id for r in bundle_roles):
            return Indicators.PRESENT

        if len(bundle_roles) == Limits.BUNDLE_ALLOW_LIMIT:
            return Indicators.MAXIMUM_REACHED

        return Indicators.ADDABLE

    async def is_bundle_selection_valid(self, server_id: int, index: int, name: str) -> bool:
        data = get_gear(self.bot, Data)
        
        return (await data.get_bundle(server_id, index)).name == name

    async def get_allowed_bundle_roles(self, member: Member) -> list[BundleRole]:
        data = get_gear(self.bot, Data)
        
        allowed_server_roles: list[BundleRole] = await data.get_allowed_bundle_roles(member.server_id)

        return [
            role
            for role in allowed_server_roles
            if role.id in set(member.role_ids)
        ]

    async def check_user_bundle_roles(self, allowed_roles: list[BundleRole], member: Member, remove_all: bool = False) -> bool:
        data = get_gear(self.bot, Data)

        if member.server_permissions.manage_roles:
            return True

        bundle_role_ids: set[int] = set(await data.get_bundles_roles(member.server_id))
        allowed_bundle_role_ids: set[int] = set(await data.get_bundles_choices(allowed_roles))

        if remove_all:
            role_ids_to_remove = bundle_role_ids
        else:
            role_ids_to_remove = bundle_role_ids - allowed_bundle_role_ids

        if not role_ids_to_remove:
            return True

        new_roles = [
            role for role in member.roles
            if role.id not in role_ids_to_remove
        ]

        if len(new_roles) != len(member.roles):
            try:
                await member.edit(roles=new_roles)
            except Exception:
                return False

        return True

def setup(bot: Bot):
    bot.add_gear(Verification(bot))