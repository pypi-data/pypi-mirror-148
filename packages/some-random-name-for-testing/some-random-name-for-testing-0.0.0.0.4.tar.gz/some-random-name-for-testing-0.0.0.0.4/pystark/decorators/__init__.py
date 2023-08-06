# PyStark2 - Python add-on extension to Pyrogram
# Copyright (C) 2022 Stark Bots <https://github.com/StarkBotsIndustries>
#
# This file is part of PyStark2.
#
# PyStark2 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyStark2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyStark2. If not, see <https://www.gnu.org/licenses/>.


from .admins import Admins
from .inline import Inline
from .extras import Extras
from .command import Command
from .callback import Callback
from pyrogram.methods import Methods


class Mechanism(Methods, Command, Inline, Callback, Admins, Extras):
    pass
