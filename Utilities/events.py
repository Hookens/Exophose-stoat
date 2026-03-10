# Copyright (C) 2026 Hookens
# See the LICENSE file in the project root for details.

from stoat import ReadyEvent, ServerMemberRemoveEvent, ServerMemberUpdateEvent, ServerRoleDeleteEvent
from stoat.ext.commands import Bot, Gear
from stoat.ext.commands.events import CommandErrorEvent
from stoat.ext.commands.errors import BadArgument, CommandNotFound
from stoat.server import Member, Server

from Commands.help import AdminHelp, BundleHelp, DebugHelp, UserHelp
from Utilities.constants import Identity, LoggingDefaults

from Debug.debughelpers import try_func_async
from Utilities.gears import get_gear

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Debug.logging import Logging
    from Help.helpcommands import HelpCommands
    from Utilities.data import Data
    from Utilities.utilities import Utilities
    from Utilities.verification import Verification


class Events(Gear):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def send_help(self, event: CommandErrorEvent, menu: str = ""):
        commands: "HelpCommands" = get_gear(self.bot, "HelpCommands")
        if commands:
            await commands.handle_help(event.context, menu=menu)

    @try_func_async()
    async def delete_server(self, server: Server):
        data: "Data" = get_gear(self.bot, "Data")

        if server.name is None:
            return

        await data.delete_server(server.id)

    @Gear.listener(ReadyEvent)
    @try_func_async()
    async def on_ready(self, event: ReadyEvent):
        logging: "Logging" = get_gear(self.bot, "Logging")

        await logging.log_event(
            f"{Identity.BOT} is up. {len(self.bot.gears)} of {LoggingDefaults.GEAR_COUNT} gears running. Currently serving {len(event.servers)} servers.",
            "INFO",
        )

    @Gear.listener(CommandErrorEvent)
    @try_func_async()
    async def on_command_error(self, event: CommandErrorEvent):
        embed = None

        if isinstance(event.error, CommandNotFound):
            await self.send_help(event)
        elif isinstance(event.error, BadArgument):
            match event.context.command.qualified_name:
                case "announce":
                    embed = DebugHelp.get_announce_help()
                case "allow":
                    embed = AdminHelp.get_allow_help()
                case "disallow":
                    embed = AdminHelp.get_disallow_help()
                case "remove":
                    embed = UserHelp.get_remove_help()
                case "recolor":
                    embed = UserHelp.get_recolor_help()
                case "rename":
                    embed = UserHelp.get_rename_help()
                case "created":
                    embed = UserHelp.get_created_help()
                case "bundle edit":
                    embed = BundleHelp.get_edit_help()
                case "bundle delete":
                    embed = BundleHelp.get_delete_help()
                case "bundle allow":
                    embed = BundleHelp.get_allow_help()
                case "bundle disallow":
                    embed = BundleHelp.get_disallow_help()
                case "bundle choose":
                    embed = BundleHelp.get_choose_help()
                case _:
                    await self.send_help(event)

        if embed is not None:
            await event.context.channel.send(embeds=[embed])

    @Gear.listener(ServerMemberUpdateEvent)
    @try_func_async()
    async def on_member_update(self, event: ServerMemberUpdateEvent):
        data: "Data" = get_gear(self.bot, "Data")
        utilities: "Utilities" = get_gear(self.bot, "Utilities")
        verification: "Verification" = get_gear(self.bot, "Verification")

        member: Member = event.after

        if member is None:
            return

        # If the bot does not have permissions or the member can manage roles, ignore.
        if (
            not verification.has_permission(member.get_server())
            or member.server_permissions.manage_roles
        ):
            return

        # Verify bundle-related permissions and remove accordingly.
        allowed_roles = await verification.get_allowed_bundle_roles(member)
        await verification.check_user_bundle_roles(allowed_roles, member)

        # If the member does not have any custom roles, ignore.
        if await data.count_member_roles(member.server_id, member.id) == 0:
            return

        # If the member has custom roles, verify if they can have them and if they are within their allowed maximum.
        if not await verification.is_user_allowed(member):
            while not await verification.is_user_within_max_roles(member):
                await utilities.delete_role(member, 0)
            return

        # if not await verification.is_badge_allowed(member):
        #    created_roles: list[CreatedRole] = await data.get_member_roles(member.server_id, member.id)
        #    for created_role in created_roles:
        #        role: Role = await member.get_server().fetch_role(created_role.id)
        #        if role is not None and role.icon is not None:
        #            try:
        #                await role.edit(icon=None)
        #            except:
        #                pass

        # if not await verification.is_gradient_allowed( member):
        #    created_roles: list[CreatedRole] = await data.get_member_roles(member.server_id, member.id)
        #    for created_role in created_roles:
        #        role: Role = await member.get_server().fetch_role(created_role.id)
        #        if role is not None and role.colors.secondary is not None:
        #            try:
        #                await role.edit(colors=RoleColours(primary=role.color))
        #            except:
        #                pass

    @Gear.listener(ServerMemberRemoveEvent)
    @try_func_async()
    async def on_member_remove(self, event: ServerMemberRemoveEvent):
        utilities: "Utilities" = get_gear(self.bot, "Utilities")

        if event.member.id == self.bot.me.id:
            await self.delete_server(event.member.get_server())

        await utilities.delete_all_roles(event.member)

    @Gear.listener(ServerRoleDeleteEvent)
    @try_func_async()
    async def on_server_role_delete(self, event: ServerRoleDeleteEvent):
        data: "Data" = get_gear(self.bot, "Data")

        role = event.role_id

        if await data.is_bundle_role(role):
            await data.delete_bundles_role(role)

        if await data.is_bundle_allowed_role(role):
            await data.delete_bundles_allowed_role(role)

        if await data.is_member_role(role):
            await data.delete_member_role(role)

        if await data.is_allowed_role(role):
            await data.delete_allowed_role(role)


async def setup(bot: Bot):
    await bot.add_gear(Events(bot))
