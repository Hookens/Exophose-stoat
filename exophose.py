# Copyright (C) 2026 Hookens
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import logging
import time

from stoat.ext.commands import Bot
from stoat.shard import Reconnect
from Utilities.constants import Env, LoadOrder, Identity

_log = logging.getLogger(__name__)

MIN_DELAY = 5
MAX_DELAY = 300
HEALTHY_AFTER = 60

class Exophose(Bot):
    async def setup_hook(self):
        for gear in LoadOrder.GEARS:
            await self.load_extension(gear)

def main():
    delay = MIN_DELAY
    while True:
        client = Exophose(command_prefix=Identity.PREFIX)
        started = time.monotonic()
        try:
            client.run(token=Env.API_TOKEN)
        except KeyboardInterrupt:
            raise
        except (Reconnect, OSError, TimeoutError):
            _log.exception("Connection to Stoat lost; restarting")

        if client.shutdown_requested:
            _log.info("Shutdown requested; exiting")
            return

        _log.warning("client.run() ended; restarting")
        if time.monotonic() - started >= HEALTHY_AFTER:
            delay = MIN_DELAY
        time.sleep(delay)
        delay = min(delay * 2, MAX_DELAY)

if __name__ == "__main__":
    main()
