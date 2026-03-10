# Copyright (C) 2026 Hookens
# See the LICENSE file in the project root for details.

from stoat.ext.commands import Bot, Gear
from stoat.message import SendableEmbed
from stoat.server import Member, Role, Server

from Utilities.datahelpers import CreatedRole

from Debug.debughelpers import try_func_async
from Utilities.gears import get_gear

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Utilities.data import Data
    from Utilities.embeds import Embeds
    from Utilities.utilities import Utilities
    from Utilities.verification import Verification


class UserMethods(Gear):
    def __init__(self, bot: Bot):
        self.bot = bot

    @try_func_async(embed=True)
    async def role_create(
        self, server: Server, member: Member, name: str, color: str
    ) -> SendableEmbed:
        data: "Data" = get_gear(self.bot, "Data")
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        utilities: "Utilities" = get_gear(self.bot, "Utilities")
        verification: "Verification" = get_gear(self.bot, "Verification")

        if not await verification.is_user_role_addable(member):
            return embeds.maximum_roles()

        if not verification.is_name_allowed(name):
            return embeds.blacklisted_word()

        hex_color = await utilities.parse_color(color)

        created_role: Role = await server.create_role(name=name)
        await created_role.edit(color=hex_color)
        if not await data.add_member_role(created_role.id, server.id, member.id):
            await created_role.delete()
            return embeds.unexpected_sql_error()

        roles = set(member.role_ids)
        roles.add(created_role.id)
        await member.edit(roles=roles)
        # await utilities.reposition(created_role)
        embed: SendableEmbed = embeds.creation_success()

        # if role_badge:
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
    async def role_remove(self, member: Member, index: int) -> SendableEmbed:
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        utilities: "Utilities" = get_gear(self.bot, "Utilities")

        index -= 1

        if await utilities.delete_role(member, index):
            return embeds.success_modification("remove")

        return embeds.missing_modification_index("remove")

    @try_func_async(embed=True)
    async def role_recolor(
        self, server: Server, member: Member, color: str, index: int
    ) -> SendableEmbed:
        data: "Data" = get_gear(self.bot, "Data")
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        utilities: "Utilities" = get_gear(self.bot, "Utilities")

        index -= 1

        hex_color = await utilities.parse_color(color)

        created_roles: list[CreatedRole] = await data.get_member_roles(
            server.id, member.id
        )

        if not any(created_roles):
            return embeds.missing_modification_role("recolor")

        if index >= len(created_roles):
            return embeds.missing_modification_index("recolor")

        role: Role = await server.fetch_role(created_roles[index].id)

        embed = embeds.success_modification("recolor")

        try:
            await role.edit(color=hex_color)

            # if role_secondary or role_holographic is True:
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
        except Exception as e:
            return embeds.not_edit_allowed(role, "recolor")

        return embed

    @try_func_async(embed=True)
    async def role_rename(
        self, server: Server, member: Member, name: str, index: int
    ) -> SendableEmbed:
        data: "Data" = get_gear(self.bot, "Data")
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        verification: "Verification" = get_gear(self.bot, "Verification")

        index -= 1

        if not verification.is_name_allowed(name):
            return embeds.blacklisted_word()

        created_roles: list[CreatedRole] = await data.get_member_roles(
            server.id, member.id
        )

        if not any(created_roles):
            return embeds.missing_modification_role("rename")

        if index >= len(created_roles):
            return embeds.missing_modification_index("rename")

        role: Role = await server.fetch_role(created_roles[index].id)

        try:
            await role.edit(name=name)
        except:
            return embeds.not_edit_allowed(role, "rename")

        return embeds.success_modification("rename")

    # @try_func_async(embed=True)
    # async def role_rebadge (
    #        self,
    #        ctx: ApplicationContext,
    #        role_badge: Attachment,
    #        index: int) -> SendableEmbed:
    #    data: 'Data' = get_gear(self.bot, "Data")
    #    embeds: 'Embeds' = get_gear(self.bot, "Embeds")
    #    verification: 'Verification' = get_gear(self.bot, "Verification")
    #
    #    if "ROLE_ICONS" not in server.features:
    #        return embeds.not_feature_allowed()
    #
    #    if not await verification.is_badge_allowed(ctx.author):
    #        return embeds.not_badge_allowed()
    #
    #    created_roles: list[CreatedRole] = await data.get_member_roles(server.id, ctx.author.id)
    #
    #    if not any(created_roles):
    #        return embeds.missing_modification_role("rebadge")
    #
    #    if index >= len(created_roles):
    #        return embeds.missing_modification_index("rebadge")
    #
    #    role: Role = server.get_role(created_roles[index].id)
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


async def setup(bot: Bot):
    await bot.add_gear(UserMethods(bot))
