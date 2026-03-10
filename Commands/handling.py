# Copyright (C) 2026 Hookens
# See the LICENSE file in the project root for details.

from stoat.ext.commands import Bot, Gear
from stoat.message import SendableEmbed
from stoat.server import Server
from stoat.channel import BaseServerChannel

from Utilities.datahelpers import Parameter
from Utilities.gears import get_gear

from typing import TYPE_CHECKING, Any, Callable, Awaitable

if TYPE_CHECKING:
    from Utilities.embeds import Embeds


class Handling(Gear):
    def __init__(self, bot: Bot):
        self.bot = bot

    def list_match(values):
        values = [f'"{v}"' for v in values]

        if not values:
            return ""
        if len(values) == 1:
            return values[0]
        if len(values) == 2:
            return " or ".join(values)

        return ", ".join(values[:-1]) + f", or {values[-1]}"

    def verify_permissions(
        self, server: Server, channel: BaseServerChannel
    ) -> str | None:
        if not channel.permissions_for(server.me).send_messages:
            return "..."
        if not channel.permissions_for(server.me).send_embeds:
            return "I require `Send Embeds` in this channel."
        if not server.me.server_permissions.manage_roles:
            return "I require `Manage Roles` in this server."
        if not server.me.server_permissions.assign_roles:
            return "I require `Assign Roles` in this server."

    async def handle_command(
        self,
        callback: Callable[..., Awaitable[SendableEmbed]],
        fallback_factory: Callable[[], SendableEmbed],
        *parameters: Parameter,
        **kwargs,
    ) -> SendableEmbed:
        def fail(message: str) -> SendableEmbed:
            embeds: "Embeds" = get_gear(self.bot, "Embeds")
            embed = fallback_factory()
            embeds.set_footer(embed, message)
            return embed

        validated: dict[str, Any] = {}

        for parameter in parameters:
            name = parameter.name
            value = parameter.value
            expected_type = parameter.expected_type

            if parameter.required and value is None:
                return fail(f"Missing required parameter `{name}`")

            if value is None:
                validated[name] = None
                continue

            if not isinstance(value, expected_type):
                return fail(f"`{name}` was not the correct type.")

            if isinstance(value, str):
                if parameter.min is not None and len(value) < parameter.min:
                    if len(value) == 0:
                        return fail(f"`{name}` must not be empty.")
                    return fail(
                        f"`{name}` must be at least {parameter.min} characters."
                    )
                if parameter.max is not None and len(value) > parameter.max:
                    return fail(f"`{name}` must be at most {parameter.max} characters.")

            if isinstance(value, (int, float)):
                if parameter.min is not None and value < parameter.min:
                    return fail(f"`{name}` must be ≥ {parameter.min}.")
                if parameter.max is not None and value > parameter.max:
                    return fail(f"`{name}` must be ≤ {parameter.max}.")

            if parameter.match is not None and parameter.value not in parameter.match:
                match_values = list(parameter.match)
                if value not in match_values:
                    return fail(f"`{name}` must be {self.list_match(parameter.match)}.")

            validated[name] = value

        validated |= kwargs

        return await callback(**validated)


async def setup(bot: Bot):
    await bot.add_gear(Handling(bot))
