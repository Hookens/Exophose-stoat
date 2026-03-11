# Copyright (C) 2026 Hookens
# See the LICENSE file in the project root for details.

from stoat.ext.commands import Bot, Gear
from stoat.server import Member, Role, Server

from Utilities.datahelpers import CreatedRole

from Debug.debughelpers import try_func_async
from Utilities.gears import get_gear

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Utilities.data import Data


class Utilities(Gear):
    def __init__(self, bot: Bot):
        self.bot = bot

    def parsable_color(self, color: str) -> bool:
        try:
            intcolor: int = int(color, 16)
        except:
            return False

        return True

    @try_func_async()
    async def parse_color(self, color: str):

        hexcolor = color.replace("#", "")

        if not self.parsable_color(hexcolor):
            return color

        intcolor = int(hexcolor, 16)
        if intcolor > 0xFFFFFF:
            hexcolor = "FFFFFF"
        elif intcolor <= 0:
            hexcolor = "FFFFFF"

        return f"#{hexcolor}"

    def get_highest_role(
        self, member: Member, requires_assignation: bool = False
    ) -> int | None:
        roles = (
            [role for role in member.roles if role.permissions.allow.assign_roles]
            if requires_assignation
            else member.roles
        )

        if not roles:
            return None

        return min(role.rank for role in roles)

    # Hopefully replace this in the future if they decide to re-implement individual ranking in role create/edit.
    @try_func_async()
    async def reposition(self, server: Server, role: Role):
        highest = self.get_highest_role(server.me, True)

        if highest is None:
            return

        target_rank = highest + 1

        roles = sorted(server.roles.values(), key=lambda r: r.rank)
        roles = [r for r in roles if r.id != role.id]
        target_rank = min(target_rank, len(roles))

        roles.insert(target_rank, role)

        await server.bulk_edit_role_ranks(roles)

    @try_func_async()
    async def delete_role(self, member: Member, role_index: int) -> bool:
        data: "Data" = get_gear(self.bot, "Data")

        created_roles: list[CreatedRole] = await data.get_member_roles(
            member.server_id, member.id
        )

        if 0 <= role_index < len(created_roles):
            server: Server = self.bot.get_server(created_roles[role_index].server_id)
            role: Role = await server.fetch_role(created_roles[role_index].id)

            if await data.delete_member_role(created_roles[role_index].id):
                try:
                    await role.delete()
                except:
                    pass
                return True

        return False

    @try_func_async()
    async def delete_all_roles(self, member: Member):
        data: "Data" = get_gear(self.bot, "Data")

        if not member.roles:
            return

        created_roles: list[CreatedRole] = await data.get_member_roles(
            member.server_id, member.id
        )
        if not created_roles:
            return

        await data.delete_member_roles(member.server_id, member.id)

        server: Server = self.bot.get_server(member.server_id)
        for created_role in created_roles:
            role: Role = await server.fetch_role(created_role.id)
            try:
                await role.delete()
            except:
                pass


async def setup(bot: Bot):
    await bot.add_gear(Utilities(bot))
