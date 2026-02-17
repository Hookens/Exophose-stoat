# Copyright (C) 2026 Hookens
# See the LICENSE file in the project root for details.

from stoat.ext.commands import Bot
from stoat.ext import commands
from stoat.server import Server, Member, Role

from Debug.debughelpers import try_func_async
from Utilities.datahelpers import CreatedRole
from Utilities.gears import get_gear

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Utilities.data import Data

class Utilities(commands.Gear):
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
        hexcolor = color.replace('#', '')

        if not self.parsable_color(hexcolor):
            return None
        
        intcolor = int(hexcolor, 16)
        if intcolor > 0xFFFFFF:
            intcolor = 0xFFFFFF
        elif intcolor <= 0:
            intcolor = 0x010101
        
        return intcolor

    #I need to implement a "reference" role feature it appears.
    #@try_func_async()
    #async def reposition(self, role: Role):
    #    data = get_gear(self.bot, Data)
    #    
    #    exo_role: ExoRole = await data.get_server(role.server_id)
    #    
    #    if exo_role is None or exo_role.id == 0:
    #        return
    #    
    #    botrole = await role.server.fetch_role(exo_role.id)
    #
    #    if botrole and role.server.me.server_permissions.manage_roles:
    #        try:
    #            await role.edit(rank=botrole.rank - 1)
    #        except:
    #            pass

    @try_func_async()
    async def delete_role(self, member: Member, role_index: int) -> bool:
        data = get_gear(self.bot, Data)
        
        created_roles: list[CreatedRole] = await data.get_member_roles(member.server_id, member.id)

        if 0 <= role_index < len(created_roles):
            server: Server = self.bot.get_server(created_roles[role_index].server_id)
            role: Role = server.roles.get(created_roles[role_index].id)

            if await data.delete_member_role(created_roles[role_index].id):
                try:
                    await role.delete()
                except:
                    pass
                return True
            
        return False

    @try_func_async()
    async def delete_all_roles(self, member: Member):
        data = get_gear(self.bot, Data)

        if not member.roles:
            return
        
        created_roles: list[CreatedRole] = await data.get_member_roles(member.server_id, member.id)
        if not created_roles:
            return
        
        await data.delete_member_roles(member.server_id, member.id)

        server: Server = self.bot.get_server(member.server_id)
        for created_role in created_roles:
            role: Role = server.roles.get(created_role.id)
            try:
                await role.delete()
            except:
                pass


def setup(bot: Bot):
    bot.add_gear(Utilities(bot))