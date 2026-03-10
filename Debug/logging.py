# Copyright (C) 2026 Hookens
# See the LICENSE file in the project root for details.

from datetime import datetime
from stoat.ext.commands import Bot, Gear
from stoat.channel import TextChannel
from stoat.message import SendableEmbed

from Utilities.constants import Identity, LoggingDefaults


class Logging(Gear):
    def __init__(self, bot: Bot):
        self.bot = bot

    # Parity with Utilities.embeds but without requiring it to ensure it is always available.
    def add_field(self, embed: SendableEmbed, name: str, value: str):
        embed.description += f"\n#### {name}\n{value}"

    async def log_event(self, event: str, type: str):
        print(
            f' {type}  [{datetime.now().strftime("%m/%d/%Y %H:%M:%S.%f")[:-3]}] - {event}'
        )

        console_channel: TextChannel = await self.bot.fetch_channel(LoggingDefaults.CHANNEL)

        await console_channel.send(content=f"```prolog\n{event}\n```")

    async def log_error(self, error: Exception, function: str, traceback: str, *args):
        print(
            f' ERROR  [{datetime.now().strftime("%m/%d/%Y %H:%M:%S.%f")[:-3]}] - {Identity.BOT} encountered {error} in {function}.'
        )

        epoch: int = int(datetime.now().timestamp())

        embed: SendableEmbed = SendableEmbed(
            title=f"Error in {Identity.BOT}", description=f"{error}", color="#CC0000"
        )

        self.add_field(embed, "Timestamp", f"<t:{epoch}:F>, <t:{epoch}:R>")
        self.add_field(embed, "Function", f"`{function}`")
        self.add_field(embed, "Traceback", f"```js\n{traceback}\n```")
        if any(args):
            self.add_field(embed, "Arguments", f"`{args}`")

        console_channel: TextChannel = self.bot.get_channel(LoggingDefaults.CHANNEL)

        await console_channel.send(embeds=[embed], content=f"<@{Identity.ID}>")


async def setup(bot: Bot):
    await bot.add_gear(Logging(bot))
