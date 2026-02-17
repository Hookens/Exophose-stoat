# Copyright (C) 2026 Hookens
# See the LICENSE file in the project root for details.

from datetime import datetime
from stoat.ext.commands import Bot
from stoat.ext import commands
from stoat.channel import TextChannel
from stoat.embed import TextEmbed

from Utilities.constants import LoggingDefaults

class Logging(commands.Gear):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def log_event (self, event: str, type: str):
        print(f' {type}  [{datetime.now().strftime("%m/%d/%Y %H:%M:%S.%f")[:-3]}] - {event}')

        console_channel: TextChannel = self.bot.get_channel(LoggingDefaults.CHANNEL)

        await console_channel.send(content=f"```prolog\r\n{event}```")

    async def log_error (self, error, function, traceback, *args):
        print(f' ERROR  [{datetime.now().strftime("%m/%d/%Y %H:%M:%S.%f")[:-3]}] - {LoggingDefaults.NAME} encountered {error} in {function}.')

        epoch: int = int(datetime.now().timestamp())

        embed: TextEmbed = TextEmbed(title=f"Error in {LoggingDefaults.NAME}", description=error, color="CC0000")

        #embed.add_field(name="Timestamp", value=f"<t:{epoch}:F>, <t:{epoch}:R>", inline=True)
        #embed.add_field(name="Function", value=f"`{function}`", inline=True)
        #embed.add_field(name="Traceback", value=f'`{traceback}`', inline=False)
        #if any(args):
        #    embed.add_field(name="Arguments", value=f'`{args}`', inline=False)

        console_channel: TextChannel = self.bot.get_channel(LoggingDefaults.CHANNEL)

        await console_channel.send(embeds=[embed], content=f"<@{LoggingDefaults.PING}>")



def setup(bot: Bot):
    bot.add_gear(Logging(bot))