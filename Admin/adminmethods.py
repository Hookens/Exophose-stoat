# Copyright (C) 2026 Hookens
# See the LICENSE file in the project root for details.

from stoat.ext.commands import Bot
from stoat.ext import commands
from stoat.message import SendableEmbed
from stoat.server import Server, Member, Role

from Debug.debughelpers import try_func_async
from Utilities.constants import Indicators
from Utilities.gears import get_gear

from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from Utilities.data import Data
    from Utilities.embeds import Embeds
    from Utilities.verification import Verification

class AdminMethods(commands.Gear):
    def __init__(self, bot: Bot):
        self.bot = bot

    @try_func_async(embed=True)
    async def allow_role(
            self,
            server: Server,
            member: Member,
            role: Role,
            max_roles: Optional[int] = None) -> SendableEmbed:
        data = get_gear(self.bot, Data)
        embeds = get_gear(self.bot, Embeds)
        verification = get_gear(self.bot, Verification)

        if not verification.is_name_allowed(role.name):
            return embeds.blacklisted_word()

        status, allowed_role = await verification.is_role_allowable(role.id, server.id)
        if status == Indicators.UNABLE:
            return embeds.allowed_role_error(role)
        
        if status == Indicators.MAXIMUM_REACHED:
            return embeds.maximum_allowed_roles()
        
        if max_roles is None:
            max_roles = (allowed_role.max_roles if status == Indicators.PRESENT and allowed_role else 1)

        # Add or update
        success = await data.add_allowed_role(
            role.id,
            server.id,
            member.id,
            max_roles,
            False,
            False
        )

        if not success:
            return embeds.unexpected_sql_error()

        if status == Indicators.ADDABLE:
            return embeds.allowed_role_added(role)

        if status == Indicators.PRESENT:
            return embeds.allowed_role_updated(role)

    @try_func_async(embed=True)
    async def disallow_role(
            self,
            server: Server,
            role: Role) -> SendableEmbed:
        data = get_gear(self.bot, Data)
        embeds = get_gear(self.bot, Embeds)
        verification = get_gear(self.bot, Verification)
        
        if not await verification.is_role_allowable(role.id, server.id) == Indicators.PRESENT:
            return embeds.allowed_role_missing(role)
        
        if await data.delete_allowed_role(role.id):
            return embeds.allowed_role_removed(role)


def setup(bot: Bot):
    bot.add_gear(AdminMethods(bot))