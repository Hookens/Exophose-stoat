# Copyright (C) 2026 Hookens
# See the LICENSE file in the project root for details.

import stoat
from stoat.ext.commands import Bot
from stoat.ext import commands
from stoat.server import Server, Member, Role

from Debug.debughelpers import try_func_async
from Utilities.constants import LoggingDefaults
from Utilities.gears import get_gear

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Debug.logging import Logging
    from Utilities.data import Data
    from Utilities.utilities import Utilities
    from Utilities.verification import Verification

class Events(commands.Gear):
    def __init__(self, bot: Bot):
        self.bot = bot

    @try_func_async()
    async def delete_server(self, server: Server):
        data = get_gear(self.bot, Data)
        
        if server.name is None:
            return
        
        await data.delete_server(server.id)

    @commands.Gear.listener(stoat.ReadyEvent)
    @try_func_async()
    async def on_ready (self, event: stoat.ReadyEvent):
        logging = get_gear(self.bot, Logging)
        
        await logging.log_event(f"{LoggingDefaults.NAME} is up. {len(self.bot.gears)} of {LoggingDefaults.GEAR_COUNT} gears running. Currently serving {len(self.bot.servers)} servers.", "INFO")

        await self.bot
        
    @commands.Gear.listener(stoat.ServerMemberUpdateEvent)
    @try_func_async()
    async def on_member_update(self, event: stoat.ServerMemberUpdateEvent):
        data = get_gear(self.bot, Data)
        utilities = get_gear(self.bot, Utilities)
        verification = get_gear(self.bot, Verification)

        member: Member = await event.after
        
        if member is None: 
            return

        #If the bot does not have permissions or the member can manage roles, ignore.
        if (not verification.has_permission(member.get_server()) or
            member.server_permissions.manage_roles):
            return

        #Verify bundle-related permissions and remove accordingly.
        allowed_roles = await verification.get_allowed_bundle_roles(member)
        await verification.check_user_bundle_roles(allowed_roles, member)

        #If the member does not have any custom roles, ignore.
        if await data.count_member_roles(member.server_id, member.id) == 0:
            return
        
        #If the member has custom roles, verify if they can have them and if they are within their allowed maximum.
        if not await verification.is_user_allowed(member):
            while not await verification.is_user_within_max_roles(member):
                await utilities.delete_role(member, 0)
            return

        #if not await verification.is_badge_allowed(member):
        #    created_roles: list[CreatedRole] = await data.get_member_roles(member.server_id, member.id)
        #    for created_role in created_roles:
        #        role: Role = await member.get_server().fetch_role(created_role.id)
        #        if role is not None and role.icon is not None:
        #            try:
        #                await role.edit(icon=None)
        #            except:
        #                pass

        #if not await verification.is_gradient_allowed( member):
        #    created_roles: list[CreatedRole] = await data.get_member_roles(member.server_id, member.id)
        #    for created_role in created_roles:
        #        role: Role = await member.get_server().fetch_role(created_role.id)
        #        if role is not None and role.colors.secondary is not None:
        #            try:
        #                await role.edit(colors=RoleColours(primary=role.color))
        #            except:
        #                pass

    @commands.Gear.listener(stoat.ServerMemberRemoveEvent)
    @try_func_async()
    async def on_member_remove(self, event: stoat.ServerMemberRemoveEvent):
        utilities = get_gear(self.bot, Utilities)
        
        if(event.member.id == self.bot.me.id):
            await self.delete_server(event.member.get_server())
        
        await utilities.delete_all_roles(event.member)

    @commands.Gear.listener(stoat.ServerRoleDeleteEvent)
    @try_func_async()
    async def on_server_role_delete(self, event: stoat.ServerRoleDeleteEvent):
        data = get_gear(self.bot, Data)
        
        role = event.role_id

        if await data.is_bundle_role(role):
            await data.delete_bundles_role(role)

        if await data.is_bundle_allowed_role(role):
            await data.delete_bundles_allowed_role(role)
        
        if await data.is_member_role(role):
            await data.delete_member_role(role)

        if await data.is_allowed_role(role):
            await data.delete_allowed_role(role)


def setup(bot: Bot):
    bot.add_gear(Events(bot))