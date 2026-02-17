# Copyright (C) 2026 Hookens
# See the LICENSE file in the project root for details.

from stoat.ext import commands
from stoat.ext.commands import Bot
from stoat.message import SendableEmbed
from stoat.server import Member, Server, Role

from Debug.debughelpers import try_func_async
from Utilities.gears import get_gear

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Utilities.data import Data
    from Utilities.embeds import Embeds
    from Utilities.verification import Verification

class BundleMethods(commands.Gear):
    def __init__(self, bot: Bot):
        self.bot = bot

    @try_func_async(embed=True)
    async def bundle_create(
            self,
            server: Server,
            name: str) -> SendableEmbed:
        data = get_gear(self.bot, Data)
        embeds = get_gear(self.bot, Embeds)
        verification = get_gear(self.bot, Verification)
        
        if not verification.is_name_allowed(name):
            return embeds.blacklisted_word()
        
        if await data.count_bundles(server.id) >= 5:
            return embeds.maximum_bundles()

        if await data.add_bundle(server.id, name):
            return embeds.bundle_created(name)

            
        return embeds.unexpected_sql_error()

    @try_func_async(embed=True)
    async def bundle_list(
            self,
            server: Server) -> SendableEmbed:
        embeds = get_gear(self.bot, Embeds)

        return await embeds.bundle_list(server.id)

    @try_func_async(embed=True)
    async def bundle_edit(
            self,
            server: Server,
            index: int,
            role: Role,
            add: bool) -> SendableEmbed:
        data = get_gear(self.bot, Data)
        embeds = get_gear(self.bot, Embeds)
        verification = get_gear(self.bot, Verification)
        
        if not (0 <= index < await data.count_bundles(server.id)):
            return embeds.bundle_missing_index("edit")

        addable = await verification.is_bundle_role_addable(role.id, server.id, index)

        if add:
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
            self,
            server: Server,
            index: int,
            name: str) -> SendableEmbed:
        data = get_gear(self.bot, Data)
        embeds = get_gear(self.bot, Embeds)
        verification = get_gear(self.bot, Verification)
        
        if not (0 <= index < await data.count_bundles(server.id)):
            return embeds.bundle_missing_index("delete")
        
        if not await verification.is_bundle_selection_valid(server.id, index, name):
            return embeds.bundle_selection_invalid()
        
        if await data.delete_bundle(server.id, index):
            return embeds.bundle_deleted()
            
        return embeds.unexpected_sql_error()

    @try_func_async(embed=True)
    async def bundle_allow(
            self,
            server: Server,
            index: int,
            role: Role) -> SendableEmbed:
        data = get_gear(self.bot, Data)
        embeds = get_gear(self.bot, Embeds)
        verification = get_gear(self.bot, Verification)
        
        if not (0 <= index < await data.count_bundles(server.id)):
            return embeds.bundle_missing_index("allow")
        
        if not verification.is_name_allowed(role.name):
                return embeds.blacklisted_word()
        
        allowable = await verification.is_bundle_allowed_role_allowable(role.id, server.id, index)
        if allowable == 1:
            if await data.add_bundle_allowed_role(role.id, server.id, index):
                return embeds.bundle_allowed_role_added(role)
        elif allowable == 0:
            return embeds.bundle_allowed_role_present(role)
        else:
            return embeds.bundle_allowed_role_error(role)
            
        return embeds.unexpected_sql_error()

    @try_func_async(embed=True)
    async def bundle_disallow(
            self,
            server: Server,
            index: int,
            role: Role) -> SendableEmbed:
        data = get_gear(self.bot, Data)
        embeds = get_gear(self.bot, Embeds)
        verification = get_gear(self.bot, Verification)
        
        if not (0 <= index < await data.count_bundles(server.id)):
            return embeds.bundle_missing_index("disallow")

        allowable = await verification.is_bundle_allowed_role_allowable(role.id, server.id, index)
        if allowable == 1:
            return embeds.bundle_allowed_role_missing(role)
        else:
            if await data.delete_bundle_allowed_role(role.id, server.id, index):
                return embeds.bundle_allowed_role_removed(role)
            
        return embeds.unexpected_sql_error()

    @try_func_async(embed=True)
    async def bundle_choices(
            self,
            member: Member) -> SendableEmbed:
        embeds = get_gear(self.bot, Embeds)
        verification = get_gear(self.bot, Verification)
        
        allowed_roles = await verification.get_allowed_bundle_roles(member)

        if not allowed_roles:
            return embeds.not_bundle_allowed()
        
        return await embeds.bundle_choices(allowed_roles)

    @try_func_async(embed=True)
    async def bundle_choose(
            self,
            server: Server,
            member: Member,
            index: int) -> SendableEmbed:
        data = get_gear(self.bot, Data)
        embeds = get_gear(self.bot, Embeds)
        verification = get_gear(self.bot, Verification)

        allowed_roles = await verification.get_allowed_bundle_roles(member)

        if not allowed_roles:
            return embeds.not_bundle_allowed()
        
        if ((not await verification.check_user_bundle_roles(allowed_roles, member, True)) 
            or (not (0 <= index < await data.count_bundles_choices(allowed_roles)))):
            return embeds.bundle_missing_choice_index()
        
        chosen_role_id = await data.get_bundles_choice(allowed_roles, index)
        role: Role = server.roles.get(chosen_role_id)
        
        try:
            await member.edit(roles=member.role_ids.append(role.id))
        except:
            return embeds.not_role_allowed(role)

        return embeds.bundle_role_selected(role)
    

def setup(bot: Bot):
    bot.add_gear(BundleMethods(bot))