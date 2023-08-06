# PyStark - Python add-on extension to Pyrogram
# Copyright (C) 2021-2022 Stark Bots <https://github.com/StarkBotsIndustries>
#
# This file is part of PyStark.
#
# PyStark is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyStark is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyStark. If not, see <https://www.gnu.org/licenses/>.

import functools
from pystark import env
from pystark.logger import logger
from pyrogram import filters as f
from pyrogram.types import CallbackQuery
from pyrogram.handlers import CallbackQueryHandler
from pyrogram.methods.decorators.on_callback_query import OnCallbackQuery


class Callback(OnCallbackQuery):
    @staticmethod
    def callback(
        query: str | list[str] = None,
        startswith: bool = False,
        owner_only: bool = False,
        sudo_only: bool = True,
        group: int = 0,
        filters=None
    ):
        # ToDo:
        #   case_sensitive argument
        if isinstance(query, list):
            cmd_filter = f.create(lambda _, __, query_: query_.data.lower() in query)
        elif isinstance(query, str):
            query = query.lower()
            if not startswith:
                cmd_filter = f.create(lambda _, __, query_: query_.data.lower() == query)
            else:
                cmd_filter = f.create(lambda _, __, query_: query_.data.lower().startswith(query))
        elif not query:
            cmd_filter = None
        else:
            logger.warn(f'Callback query cannot be of type {type(query)} - {query}]')
            return
        if filters:
            filters_ = cmd_filter & filters
        else:
            filters_ = cmd_filter
        if sudo_only:
            filters_ = filters_ & f.user(env.SUDO_USERS)
        elif owner_only:
            filters_ = filters_ & f.user(env.OWNER_ID)

        def decorator(func):
            @functools.wraps(func)
            async def wrapper(*args):
                q = args[1]  # type: CallbackQuery
                if q.from_user.id in env.SUDO_USERS:
                    await func(*args)
                else:
                    await q.answer("You can't use this userbot. I'm sorry!", show_alert=True)

            if not hasattr(func, "handlers"):
                wrapper.handlers = []
            wrapper.handlers.append((CallbackQueryHandler(wrapper, filters_), group))

            return wrapper

        return decorator

    cb = callback  # alias
