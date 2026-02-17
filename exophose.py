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
from stoat.ext.commands import Bot
from Utilities.constants import Env, LoadOrder

client = Bot(command_prefix=Env.PREFIX)

for GEAR in LoadOrder.GEARS:
    client.load_extension(GEAR)

client.run(token=Env.API_TOKEN)