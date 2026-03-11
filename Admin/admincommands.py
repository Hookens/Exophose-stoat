# Copyright (C) 2026 Hookens
# See the LICENSE file in the project root for details.

from stoat.ext import commands
from stoat.ext.commands import Bot, Context, Gear
from stoat.server import Role

from Commands.help import AdminHelp
from Utilities.constants import AdminTexts, Limits
from Utilities.datahelpers import Parameter

from Debug.debughelpers import try_func_async
from Utilities.gears import get_gear

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Admin.adminmethods import AdminMethods
    from Commands.handling import Handling
    from Utilities.embeds import Embeds


class AdminCommands(Gear):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.server_only()
    @commands.command(name="allow", description=AdminTexts.C_ALLOW)
    @try_func_async()
    async def handle_allow(
        self, ctx: Context, role: Role = None, max_roles: int = None
    ):
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        methods: "AdminMethods" = get_gear(self.bot, "AdminMethods")
        handling: "Handling" = get_gear(self.bot, "Handling")

        content = handling.verify_permissions(ctx.server, ctx.channel)
        if content:
            if content != "...":
                await ctx.message.reply(content=content)
            return

        if not ctx.author.server_permissions.manage_roles:
            await ctx.message.reply(embeds=[embeds.not_user_allowed()])
            return

        embed = await handling.handle_command(
            methods.allow_role,
            AdminHelp.get_allow_help,
            Parameter("role", role, expected_type=Role, required=True),
            Parameter(
                "max_roles",
                max_roles or 1,
                expected_type=int,
                min=1,
                max=Limits.CREATE_LIMIT,
            ),
            server=ctx.server,
            member=ctx.author,
        )

        await ctx.message.reply(embeds=[embed])

    @commands.server_only()
    @commands.command(name="disallow", description=AdminTexts.C_DISALLOW)
    @try_func_async()
    async def handle_disallow(self, ctx: Context, role: Role = None):
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        methods: "AdminMethods" = get_gear(self.bot, "AdminMethods")
        handling: "Handling" = get_gear(self.bot, "Handling")

        content = handling.verify_permissions(ctx.server, ctx.channel)
        if content:
            if content != "...":
                await ctx.message.reply(content=content)
            return

        if not ctx.author.server_permissions.manage_roles:
            await ctx.message.reply(embeds=[embeds.not_user_allowed()])
            return

        embed = await handling.handle_command(
            methods.disallow_role,
            AdminHelp.get_disallow_help,
            Parameter("role", role, expected_type=Role, required=True),
            server=ctx.server,
        )

        await ctx.message.reply(embeds=[embed])

    @commands.server_only()
    @commands.command(name="allowed", description=AdminTexts.C_ALLOWED)
    @try_func_async()
    async def handle_allowedroles(self, ctx: Context):
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        handling: "Handling" = get_gear(self.bot, "Handling")

        content = handling.verify_permissions(ctx.server, ctx.channel)
        if content:
            if content != "...":
                await ctx.message.reply(content=content)
            return

        if not ctx.author.server_permissions.manage_roles:
            await ctx.message.reply(embeds=[embeds.not_user_allowed()])
        else:
            await ctx.message.reply(embeds=[await embeds.allowed_roles(ctx.server.id)])


async def setup(bot: Bot):
    await bot.add_gear(AdminCommands(bot))
