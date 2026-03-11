# Copyright (C) 2026 Hookens
# See the LICENSE file in the project root for details.

from stoat.ext import commands
from stoat.ext.commands import Bot, Context, Gear
from stoat.server import Member

from Commands.help import UserHelp
from Utilities.constants import UserTexts
from Utilities.datahelpers import Parameter

from Debug.debughelpers import try_func_async
from Utilities.gears import get_gear

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Commands.handling import Handling
    from User.usermethods import UserMethods
    from Utilities.embeds import Embeds
    from Utilities.verification import Verification


class UserCommands(Gear):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def allowed(self, member: Member) -> bool:
        verification: "Verification" = get_gear(self.bot, "Verification")

        return await verification.is_user_allowed(member)

    @commands.server_only()
    @commands.command(name="create", description=UserTexts.C_CREATE)
    @try_func_async()
    async def handle_create(self, ctx: Context, name: str = None, color: str = None):
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        methods: "UserMethods" = get_gear(self.bot, "UserMethods")
        handling: "Handling" = get_gear(self.bot, "Handling")

        content = handling.verify_permissions(ctx.server, ctx.channel)
        if content:
            if content != "...":
                await ctx.message.reply(content=content)
            return

        if not await self.allowed(ctx.author):
            await ctx.message.reply(embeds=[embeds.not_user_allowed()])
            return

        embed = await handling.handle_command(
            methods.role_create,
            UserHelp.get_create_help,
            Parameter("name", name, expected_type=str, required=True, min=1, max=32),
            Parameter(
                "color", color, expected_type=str, required=True, min=1, max=1000
            ),
            server=ctx.server,
            member=ctx.author,
        )

        await ctx.message.reply(embeds=[embed])

    @commands.server_only()
    @commands.command(name="remove", description=UserTexts.C_REMOVE)
    @try_func_async()
    async def handle_remove(self, ctx: Context, index: int = None):
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        methods: "UserMethods" = get_gear(self.bot, "UserMethods")
        handling: "Handling" = get_gear(self.bot, "Handling")

        content = handling.verify_permissions(ctx.server, ctx.channel)
        if content:
            if content != "...":
                await ctx.message.reply(content=content)
            return

        if not await self.allowed(ctx.author):
            await ctx.message.reply(embeds=[embeds.not_user_allowed()])
            return

        embed = await handling.handle_command(
            methods.role_remove,
            UserHelp.get_remove_help,
            Parameter("index", index or 1, expected_type=int),
            member=ctx.author,
        )

        await ctx.message.reply(embeds=[embed])

    @commands.server_only()
    @commands.command(name="recolor", description=UserTexts.C_RECOLOR)
    @try_func_async()
    async def handle_recolor(self, ctx: Context, color: str = None, index: int = None):
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        methods: "UserMethods" = get_gear(self.bot, "UserMethods")
        handling: "Handling" = get_gear(self.bot, "Handling")

        content = handling.verify_permissions(ctx.server, ctx.channel)
        if content:
            if content != "...":
                await ctx.message.reply(content=content)
            return

        if not await self.allowed(ctx.author):
            await ctx.message.reply(embeds=[embeds.not_user_allowed()])
            return

        embed = await handling.handle_command(
            methods.role_recolor,
            UserHelp.get_recolor_help,
            Parameter(
                "color", color, expected_type=str, required=True, min=1, max=1000
            ),
            Parameter("index", index or 1, expected_type=int),
            server=ctx.server,
            member=ctx.author,
        )

        await ctx.message.reply(embeds=[embed])

    @commands.server_only()
    @commands.command(name="rename", description=UserTexts.C_RENAME)
    @try_func_async()
    async def handle_rename(self, ctx: Context, name: str = None, index: int = None):
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        methods: "UserMethods" = get_gear(self.bot, "UserMethods")
        handling: "Handling" = get_gear(self.bot, "Handling")

        content = handling.verify_permissions(ctx.server, ctx.channel)
        if content:
            if content != "...":
                await ctx.message.reply(content=content)
            return

        if not await self.allowed(ctx.author):
            await ctx.message.reply(embeds=[embeds.not_user_allowed()])
            return

        embed = await handling.handle_command(
            methods.role_rename,
            UserHelp.get_rename_help,
            Parameter("name", name, expected_type=str, required=True, min=1, max=32),
            Parameter("index", index or 1, expected_type=int),
            server=ctx.server,
            member=ctx.author,
        )

        await ctx.message.reply(embeds=[embed])

    # @commands.server_only()
    # @commands.command(name="rebadge", description=UserTexts.C_REBADGE)
    # @try_func_async()
    # async def handle_rebadge(
    #        self,
    #        ctx: Context,
    #        badge: Option(SlashCommandOptionType.attachment, UserTexts.F_BADGE, required=False) = None,
    #        index: Option(int, UserTexts.F_INDEX, min_value=0, max_value=19, required=False) = 0):
    #    methods: 'UserMethods' = get_gear(self.bot, "UserMethods")
    #
    #    if await self.allowed(ctx):
    #                await ctx.message.reply(embeds=[await methods.role_rebadge(ctx.server, ctx.author, badge, index)])

    @commands.server_only()
    @commands.command(name="created", description=UserTexts.C_CREATED)
    @try_func_async()
    async def handle_created(self, ctx: Context, member: Member = None):
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        handling: "Handling" = get_gear(self.bot, "Handling")

        content = handling.verify_permissions(ctx.server, ctx.channel)
        if content:
            if content != "...":
                await ctx.message.reply(content=content)
            return

        if not await self.allowed(ctx.author):
            await ctx.message.reply(embeds=[embeds.not_user_allowed()])
            return

        embed = await handling.handle_command(
            embeds.created_roles,
            UserHelp.get_rename_help,
            Parameter(
                "member", member or ctx.author, expected_type=Member, required=True
            ),
            server=ctx.server,
        )

        await ctx.message.reply(embeds=[embed])


async def setup(bot: Bot):
    await bot.add_gear(UserCommands(bot))
