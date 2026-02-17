# Copyright (C) 2026 Hookens
# See the LICENSE file in the project root for details.

from stoat.ext.commands import Bot
from stoat.ext import commands
from stoat.message import SendableEmbed
from stoat.server import Server, Member, Role

from Debug.debughelpers import try_func_async
from Utilities.constants import UserTexts
from Utilities.datahelpers import CreatedRole
from Utilities.gears import get_gear

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Utilities.data import Data
    from Utilities.embeds import Embeds
    from Utilities.utilities import Utilities
    from Utilities.verification import Verification

class UserMethods(commands.Gear):
    def __init__(self, bot: Bot):
        self.bot = bot

    @try_func_async(embed=True)
    async def role_create (
            self,
            server: Server,
            member: Member,
            role_name: str,
            role_color: str) -> SendableEmbed:
        data = get_gear(self.bot, Data)
        embeds = get_gear(self.bot, Embeds)
        utilities = get_gear(self.bot, Utilities)
        verification = get_gear(self.bot, Verification)

        if not verification.has_permission(server):
            return embeds.not_permission_allowed()
        
        if not await verification.is_user_role_addable(member):
            return embeds.maximum_roles()

        if not verification.is_name_allowed(role_name):
            return embeds.blacklisted_word()

        hex_color = await utilities.parse_color(role_color)

        if hex_color is None:
            return embeds.color_parsing_error()
        
        created_role: Role = await server.create_role(name=role_name)
        created_role.edit(color=hex_color)
        if not await data.add_member_role(created_role.id, server.id, member.id):
            await created_role.delete(reason=UserTexts.DELETE_REASON)
            return embeds.unexpected_sql_error()
        
        await member.edit(roles=member.role_ids.append(created_role.id))
        #await utilities.reposition(created_role)
        embed: SendableEmbed = embeds.creation_success()

        #if role_secondary or role_holographic is True:
        #    if "ENHANCED_ROLE_COLORS" not in server.features:
        #        embed.set_footer(text=UserTexts.DF_NO_GRADIENT_PERMS)
        #    elif not await verification.is_gradient_allowed(ctx.author):
        #        embed.set_footer(text=UserTexts.DF_NOT_GRADIENT_ALLOWED)
        #    else:
        #        try:
        #            if role_holographic:
        #                await created_role.edit(holographic=True)
        #            else:
        #                hex_secondary = await utilities.parse_color(role_secondary)
        #                if hex_secondary is None:
        #                    embed.set_footer(text=UserTexts.DF_NOT_VALID_COLOR)
        #                else:
        #                    primary = Colour(hex_color)
        #                    colors = RoleColours(primary=primary, secondary=Colour(hex_secondary))
        #                    await created_role.edit(colors=colors)
        #        except:
        #            pass
        #
        #if role_badge:
        #    if "ROLE_ICONS" not in server.features:
        #        embed.set_footer(text=UserTexts.DF_NO_BADGE_PERMS)
        #    elif not await verification.is_badge_allowed(ctx.author):
        #        embed.set_footer(text=UserTexts.DF_NOT_BADGE_ALLOWED)
        #    elif not role_badge.content_type.startswith("image"):
        #        embed.set_footer(text=UserTexts.DF_INVALID_FILE)
        #    else:
        #        try:
        #            await created_role.edit(icon=await role_badge.read())
        #        except:
        #            pass

        return embed

    @try_func_async(embed=True)
    async def role_remove (
            self,
            server: Server,
            member: Member,
            role_index: int) -> SendableEmbed:
        embeds = get_gear(self.bot, Embeds)
        utilities = get_gear(self.bot, Utilities)
        verification = get_gear(self.bot, Verification)

        if not verification.has_permission(server):
            return embeds.not_permission_allowed()
        
        if await utilities.delete_role(member, role_index):
            return embeds.success_modification("remove")
        
        return embeds.missing_modification_index("remove")

    @try_func_async(embed=True)
    async def role_recolor (
            self,
            server: Server,
            member: Member,
            role_color: str,
            role_index: int) -> SendableEmbed:
        data = get_gear(self.bot, Data)
        embeds = get_gear(self.bot, Embeds)
        utilities = get_gear(self.bot, Utilities)
        verification = get_gear(self.bot, Verification)

        if not verification.has_permission(server):
            return embeds.not_permission_allowed()
        
        hex_color = await utilities.parse_color(role_color)

        if hex_color is None:
            return embeds.color_parsing_error()
        
        created_roles: list[CreatedRole] = await data.get_member_roles(server.id, member.id)

        if not any(created_roles):
            return embeds.missing_modification_role("recolor")
        
        if role_index >= len(created_roles):
            return embeds.missing_modification_index("recolor")
        
        role: Role = server.roles.get(created_roles[role_index].id)

        embed = embeds.success_modification("recolor")

        try:
            await role.edit(color=hex_color)

            #if role_secondary or role_holographic is True:
            #    if "ENHANCED_ROLE_COLORS" not in server.features:
            #        embed.set_footer(text=UserTexts.DF_NO_GRADIENT_PERMS)
            #    elif not await verification.is_gradient_allowed(ctx.author):
            #        embed.set_footer(text=UserTexts.DF_NOT_GRADIENT_ALLOWED)
            #    else:
            #        if role_holographic:
            #            await role.edit(holographic=True)
            #        else:
            #            hex_secondary = await utilities.parse_color(role_secondary)
            #            if hex_secondary is None:
            #                embed.set_footer(text=UserTexts.DF_NOT_VALID_COLOR)
            #            else:
            #                colors = RoleColours(primary=primary, secondary=Colour(hex_secondary))
            #                await role.edit(colors=colors)
        except:
            return embeds.not_edit_allowed(role, "recolor")

        return embed
    
    @try_func_async(embed=True)
    async def role_rename (
            self,
            server: Server,
            member: Member,
            role_name: str, 
            role_index: int) -> SendableEmbed:
        data = get_gear(self.bot, Data)
        embeds = get_gear(self.bot, Embeds)
        verification = get_gear(self.bot, Verification)
        
        if not verification.has_permission(server):
            return embeds.not_permission_allowed()

        if not verification.is_name_allowed(role_name):
            return embeds.blacklisted_word()
        
        created_roles: list[CreatedRole] = await data.get_member_roles(server.id, member.id)

        if not any(created_roles):
            return embeds.missing_modification_role("rename")
        
        if role_index >= len(created_roles):
            return embeds.missing_modification_index("rename")
        
        role: Role = server.roles.get(created_roles[role_index].id)

        try:
            await role.edit(name=role_name)
        except:
            return embeds.not_edit_allowed(role, "rename")
        
        return embeds.success_modification("rename")
    
    #@try_func_async(embed=True)
    #async def role_rebadge (
    #        self,
    #        ctx: ApplicationContext,
    #        role_badge: Attachment,
    #        role_index: int) -> SendableEmbed:
    #    data = get_gear(self.bot, Data)
    #    embeds = get_gear(self.bot, Embeds)
    #    verification = get_gear(self.bot, Verification)
    #    
    #    if "ROLE_ICONS" not in server.features:
    #        return embeds.not_feature_allowed()
    #    
    #    if not verification.has_permission(server):
    #        return embeds.not_permission_allowed()
    #
    #    if not await verification.is_badge_allowed(ctx.author):
    #        return embeds.not_badge_allowed()
    #    
    #    created_roles: list[CreatedRole] = await data.get_member_roles(server.id, ctx.author.id)
    #
    #    if not any(created_roles):
    #        return embeds.missing_modification_role("rebadge")
    #    
    #    if role_index >= len(created_roles):
    #        return embeds.missing_modification_index("rebadge")
    #    
    #    role: Role = server.get_role(created_roles[role_index].id)
    #    
    #    if role_badge is None:
    #        try:
    #            await role.edit(icon=None)
    #        except:
    #            return embeds.not_edit_allowed(role, "rebadge")
    #        
    #    elif role_badge.content_type.startswith("image"):
    #        try:
    #            await role.edit(icon=await role_badge.read())
    #            return embeds.success_modification("rebadge")
    #        except:
    #            pass
    #
    #    return embeds.not_file_allowed()
    

def setup(bot: Bot):
    bot.add_gear(UserMethods(bot))