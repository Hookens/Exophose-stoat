# Copyright (C) 2026 Hookens
# See the LICENSE file in the project root for details.

from stoat.ext.commands import Bot, Context, Gear, Group
from stoat.server import Role

from Commands.help import BundleHelp
from Utilities.constants import BundleTexts, Limits
from Utilities.datahelpers import Parameter

from Debug.debughelpers import try_func_async
from Utilities.gears import get_gear

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Bundle.bundlemethods import BundleMethods
    from Commands.handling import Handling
    from Help.helpcommands import HelpCommands
    from Utilities.embeds import Embeds


class BundleCommands(Gear):

    async def bundle_callback(self, ctx: Context):
        commands: "HelpCommands" = get_gear(self.bot, "HelpCommands")
        if commands:
            await commands.handle_help(ctx, menu="BC")

    bundle = Group(
        bundle_callback,
        name="bundle",
        invoke_without_command=True,
        case_insensitive=True,
    )

    def __init__(self, bot: Bot):
        self.bot = bot

    @bundle.command(name="create", description=BundleTexts.C_CREATE)
    @try_func_async()
    async def handle_create(self, ctx: Context, name: str = None):
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        methods: "BundleMethods" = get_gear(self.bot, "BundleMethods")
        handling: "Handling" = get_gear(self.bot, "Handling")

        content = handling.verify_permissions(ctx.server, ctx.channel)
        if content:
            if content != "...":
                await ctx.channel.send(content=content)
            return

        if not ctx.author.server_permissions.manage_roles:
            await ctx.channel.send(embeds=[embeds.not_user_allowed()])
            return

        embed = await handling.handle_command(
            methods.bundle_create,
            BundleHelp.get_create_help,
            Parameter("name", name, expected_type=str, required=True, min=1, max=100),
            server=ctx.server,
        )

        await ctx.channel.send(embeds=[embed])

    @bundle.command(name="list", description=BundleTexts.C_LIST)
    @try_func_async()
    async def handle_list(self, ctx: Context):
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        methods: "BundleMethods" = get_gear(self.bot, "BundleMethods")
        handling: "Handling" = get_gear(self.bot, "Handling")

        content = handling.verify_permissions(ctx.server, ctx.channel)
        if content:
            if content != "...":
                await ctx.channel.send(content=content)
            return

        if not ctx.author.server_permissions.manage_roles:
            await ctx.channel.send(embeds=[await embeds.allowed_roles(ctx.server.id)])
        else:
            await ctx.channel.send(embeds=[await methods.bundle_list(ctx.server.id)])

    @bundle.command(name="edit", description=BundleTexts.C_EDIT)
    @try_func_async()
    async def handle_edit(
        self, ctx: Context, index: int = None, role: Role = None, action: str = None
    ):
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        methods: "BundleMethods" = get_gear(self.bot, "BundleMethods")
        handling: "Handling" = get_gear(self.bot, "Handling")

        content = handling.verify_permissions(ctx.server, ctx.channel)
        if content:
            if content != "...":
                await ctx.channel.send(content=content)
            return

        if not ctx.author.server_permissions.manage_roles:
            await ctx.channel.send(embeds=[embeds.not_user_allowed()])
            return

        embed = await handling.handle_command(
            methods.bundle_edit,
            BundleHelp.get_edit_help,
            Parameter(
                "index",
                index or 1,
                expected_type=int,
                required=True,
                min=1,
                max=Limits.BUNDLE_LIMIT,
            ),
            Parameter("role", role, expected_type=Role, required=True),
            Parameter(
                "action",
                action,
                expected_type=str,
                required=True,
                match=BundleTexts.CHOICES,
            ),
            server=ctx.server,
        )

        await ctx.channel.send(embeds=[embed])

    @bundle.command(name="delete", description=BundleTexts.C_DELETE)
    @try_func_async()
    async def handle_delete(self, ctx: Context, index: int = None, name: str = None):
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        methods: "BundleMethods" = get_gear(self.bot, "BundleMethods")
        handling: "Handling" = get_gear(self.bot, "Handling")

        content = handling.verify_permissions(ctx.server, ctx.channel)
        if content:
            if content != "...":
                await ctx.channel.send(content=content)
            return

        if not ctx.author.server_permissions.manage_roles:
            await ctx.channel.send(embeds=[embeds.not_user_allowed()])
            return

        embed = await handling.handle_command(
            methods.bundle_delete,
            BundleHelp.get_delete_help,
            Parameter(
                "index",
                index,
                expected_type=int,
                required=True,
                min=1,
                max=Limits.BUNDLE_LIMIT,
            ),
            Parameter(
                "name",
                name,
                expected_type=str,
                required=True,
                min=1,
                max=Limits.BUNDLE_LIMIT,
            ),
            server=ctx.server,
        )

        await ctx.channel.send(embeds=[embed])

    @bundle.command(name="allow", description=BundleTexts.C_ALLOW)
    @try_func_async()
    async def handle_allow(self, ctx: Context, index: int = None, role: Role = None):
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        methods: "BundleMethods" = get_gear(self.bot, "BundleMethods")
        handling: "Handling" = get_gear(self.bot, "Handling")

        content = handling.verify_permissions(ctx.server, ctx.channel)
        if content:
            if content != "...":
                await ctx.channel.send(content=content)
            return

        if not ctx.author.server_permissions.manage_roles:
            await ctx.channel.send(embeds=[embeds.not_user_allowed()])
            return

        embed = await handling.handle_command(
            methods.bundle_allow,
            BundleHelp.get_allow_help,
            Parameter(
                "index",
                index,
                expected_type=int,
                required=True,
                min=1,
                max=Limits.BUNDLE_LIMIT,
            ),
            Parameter("role", role, expected_type=Role, required=True),
            server=ctx.server,
        )

        await ctx.channel.send(embeds=[embed])

    @bundle.command(name="disallow", description=BundleTexts.C_DISALLOW)
    @try_func_async()
    async def handle_disallow(self, ctx: Context, index: int = None, role: Role = None):
        embeds: "Embeds" = get_gear(self.bot, "Embeds")
        methods: "BundleMethods" = get_gear(self.bot, "BundleMethods")
        handling: "Handling" = get_gear(self.bot, "Handling")

        content = handling.verify_permissions(ctx.server, ctx.channel)
        if content:
            if content != "...":
                await ctx.channel.send(content=content)
            return

        if not ctx.author.server_permissions.manage_roles:
            await ctx.channel.send(embeds=[embeds.not_user_allowed()])
            return

        embed = await handling.handle_command(
            methods.bundle_disallow,
            BundleHelp.get_disallow_help,
            Parameter(
                "index",
                index,
                expected_type=int,
                required=True,
                min=1,
                max=Limits.BUNDLE_LIMIT,
            ),
            Parameter("role", role, expected_type=Role, required=True),
            server=ctx.server,
        )

        await ctx.channel.send(embeds=[embed])

    @bundle.command(name="choices", description=BundleTexts.C_CHOICES)
    @try_func_async()
    async def handle_choices(self, ctx: Context):
        methods: "BundleMethods" = get_gear(self.bot, "BundleMethods")
        handling: "Handling" = get_gear(self.bot, "Handling")

        content = handling.verify_permissions(ctx.server, ctx.channel)
        if content:
            if content != "...":
                await ctx.channel.send(content=content)
            return

        embed = await handling.handle_command(
            methods.bundle_choices, BundleHelp.get_choices_help, member=ctx.author
        )

        await ctx.channel.send(embeds=[embed])

    @bundle.command(name="choose", description=BundleTexts.C_CHOOSE)
    @try_func_async()
    async def handle_choose(self, ctx: Context, index: int = None):
        methods: "BundleMethods" = get_gear(self.bot, "BundleMethods")
        handling: "Handling" = get_gear(self.bot, "Handling")

        content = handling.verify_permissions(ctx.server, ctx.channel)
        if content:
            if content != "...":
                await ctx.channel.send(content=content)
            return

        embed = await handling.handle_command(
            methods.bundle_choose,
            BundleHelp.get_choose_help,
            Parameter(
                "index",
                index,
                expected_type=int,
                required=True,
                min=1,
                max=Limits.BUNDLE_ROLE_LIMIT,
            ),
            server=ctx.server,
            member=ctx.author,
        )

        await ctx.channel.send(embeds=[embed])


async def setup(bot: Bot):
    await bot.add_gear(BundleCommands(bot))
