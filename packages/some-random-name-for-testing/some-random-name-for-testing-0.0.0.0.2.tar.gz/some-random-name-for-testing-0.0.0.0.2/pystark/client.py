# PyStark2 - Python add-on extension to Pyrogram
# Copyright (C) 2021-2022 Stark Bots <https://github.com/StarkBotsIndustries>
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


import os
import sys
import struct
import logging
import asyncio
import importlib
import importlib.util
from pystark import env
from pytgcalls import PyTgCalls
from pystark.logger import logger
from pystark.database import mongo
from pystark.types import PrettyDict
from pyrogram import Client, idle, raw
from pystark.utils import get_all_langs
from pystark.decorators import Mechanism
from pystark.constants import __version__
from inspect import getmembers, isfunction
from pystark.env import SUDO_USERS, settings, SESSIONS
from pytgcalls.pytgcalls_session import PyTgCallsSession
from pystark.decorators.command import command_data, bot_command_data
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import ApiIdInvalid, AccessTokenInvalid, AuthKeyDuplicated, AuthKeyUnregistered, UserDeactivated


__printed__ = False
__buttons__ = {}


class Stark(Client, Mechanism):
    __support__ = "StarkBotsChat"
    __updates__ = "pystark"
    __channel__ = "StarkBots"
    __data__ = {"total_plugins": 0, "all_plugins": {}}
    langs_data = []
    call: "Calls" = None
    bot: "Stark"
    buttons = {}
    # back_button_text = "<= Back <="
    id = 0
    name = ""
    username = ""
    sudos = []

    def __init__(self, session: str = None, is_bot: bool = False, **kwargs):
        global __printed__
        if not __printed__:
            print(f'Welcome to PyStark [v{__version__}]')
            print('Copyright (C) 2022 Stark Bots <https://github.com/StarkBotsIndustries> \n')
            self.log(f"Initializing the UserBot")
            __printed__ = True
        self.sep = "\\" if sys.platform.startswith("win") else "/"
        self.is_bot = is_bot
        if not session:
            if not SESSIONS or not SESSIONS[0]:
                self.log("No session passed to Stark class", "warn")
                raise SystemExit
            session = SESSIONS[0]
        name = "bot" if is_bot else "user"
        super().__init__(
            name=name,
            session_string=session,
            in_memory=True,
            **kwargs
        )

    def run(self, start: bool = True):
        """Main method of `Stark` class which loads plugins and activates/runs your bot."""
        t = 'Assistant' if self.is_bot else 'UserBot'
        self.log(f"Starting the {t}")
        if start:
            self._start()
        self._set_info()
        self.sudos = asyncio.get_event_loop().run_until_complete(self.load_sudos())
        self.log(f"Loading {t} Modules")
        if self.is_bot:
            plugs = f"{settings.BOT_PLUGINS}"
        else:
            plugs = f"{settings.PLUGINS}"
        self.load_modules(plugs)
        self.langs_data = {"en": get_all_langs()["en"]}
        global __buttons__
        if not __buttons__:
            __buttons__ = self._buttons_cache()
        self.buttons = __buttons__
        logger.info(f"{self.username} is now running...")

    def _start(self):
        try:
            super().start()
            return
        except ApiIdInvalid:
            logger.critical("API_ID and API_HASH combination is incorrect.")
        except AccessTokenInvalid:
            logger.critical("BOT_TOKEN is invalid.")
        except (AuthKeyUnregistered, AuthKeyDuplicated, struct.error):
            logger.critical("Your SESSION is invalid. Please terminate it and generate a new one.")
        except UserDeactivated:
            logger.critical(f"Account deleted. Time for me to rest.")
        except KeyboardInterrupt:
            logger.critical("Keyboard Interrupt. Exiting..")
        logger.info("For support visit @{}".format(self.__support__))
        raise SystemExit

    # def stop(self):
    #     asyncio.get_event_loop().run_until_complete(super().stop())

    @staticmethod
    def list_modules(directory):
        """List all modules in a directory"""
        if not os.path.exists(directory):
            Stark.log(f"No directory named '{directory}' found")
            return
        if "/." not in directory:
            directory = directory.replace('.', '/')
        plugs = []
        for path, _, files in os.walk(directory):
            for name in files:
                if name.endswith(".py"):
                    file = os.path.join(path, name)[:-3].replace("\\", "/").replace("/", ".")
                    plugs.append(file)
        return plugs

    def load_modules(self, plugins: str):
        """Load all modules from a directory or a single module as pyrogram handlers"""
        # if plugins.endswith(".py"):  # Absolute Path
        #     # C Drive can't have relative path to D: Drive in Windows so needs absolute path
        #     plugins, file = plugins.rsplit(self.sep, 1)
        #     modules: list[str] = [file[:-3]]
        # else:
        modules: list[str] = self.list_modules(plugins)
        # plugins = plugins.replace("\\", ".").replace("/", ".")
        if not modules:
            return
        data = {"total_plugins": 0, "all_plugins": {}}
        for module in modules:
            # module = module.replace("\\", "/")
            # module = module.replace("/", ".")
            # if module.endswith(".py"):
            #     module = module[:-3]
            # plugins = plugins.replace("/", ".")
            # # plugins+"."+
            mod = importlib.import_module(module)
            funcs = [func for func, _ in getmembers(mod, isfunction)]
            real_plugs = []
            for func in funcs:
                try:
                    for handler, group in getattr(mod, func).handlers:
                        self.add_handler(handler, group)
                    real_plugs.append(func)
                except AttributeError:
                    pass
                try:
                    method = getattr(mod, func).pytgcalls
                    getattr(self.call, "_on_event_update").add_handler(method, func)
                    real_plugs.append(func)
                except AttributeError:
                    pass
            module = module.replace(".", "/")
            if "plugins" in module:
                x = "plugins"
            else:
                x = "assistant"
            module = module.split(x+"/", 1)[-1]
            if real_plugs:
                data["total_plugins"] += 1
                data["all_plugins"][module] = {"path": mod.__file__, "doc": mod.__doc__}
                # , ", ".join(real_plugs)
                # [{}]
                logger.info("Loaded plugin - {}.py".format(module))
        self.__data__ = data

    @staticmethod
    def log(message, level: str | int = logging.INFO):
        """Log messages to console.

        | String       | Integer  |
        |:------------:|:--------:|
        | **debug**    | 10       |
        | **info**     | 20       |
        | **warning**  | 30       |
        | **error**    | 40       |
        | **critical** | 50       |

        Parameters:

            message (Any): Item to print to console.
            level (optional): Logging level as string or int.
        """
        if isinstance(level, str):
            level = level.lower()
        if level in ["critical", 50]:
            level = logging.CRITICAL
        elif level in ["error", 40]:
            level = logging.ERROR
        elif level in ["warning", "warn", 30]:
            level = logging.WARNING
        elif level in ["info", 20]:
            level = logging.INFO
        elif level in ["debug", 10]:
            level = logging.DEBUG
        logger.log(level, message)

    @property
    def data(self) -> dict:
        dictionary = self.__data__.copy()
        if self.is_bot:
            dictionary.update(bot_command_data)
        else:
            dictionary.update(command_data)
        return dictionary

    @property
    def total_plugins(self) -> int:
        """Number of total plugins loaded."""
        return self.data["total_plugins"]

    @property
    def all_plugins(self) -> dict:  # not "plugins" to prevent clash with pyrogram's "plugins" attribute
        """Dictionary of all plugins and their respective absolute paths.

        Example:

        ```python
        {
            "basic": {
                "path": "C:\\Users\\....\\plugins\\basic.py",
                "doc": "Docstrings"
            },
            "sample": {
                "path": "D:\\Bots\\...\\sample.py",
                "doc": None
            },
        },
        ```
        """
        return self.data["all_plugins"]

    @property
    def total_commands(self) -> int:
        """Number of total commands loaded."""
        return self.data["total_commands"]

    @property
    def all_commands(self) -> dict:
        """Dictionary of all commands and their descriptions if present else None.

        Example:

        ```python
        {
            "start": "Start the bot"
            "help": "Get help"
            "about": "About this bot"
        },
        ```
        """
        return self.data["all_commands"]

    @property
    def sudo_commands(self) -> list[str]:
        """List of all sudo commands available. Includes `owner_only` commands too."""
        return self.data["sudo_commands"]

    # @property
    # def langs(self) -> dict:
    #     """Returns all languages and corresponding file names if localization is set up otherwise None"""
    #     return {f: self.langs_data[f]["language"] for f in self.langs_data}

    @property
    def plugins_cmds(self) -> dict:
        return self.data["plugins_cmds"]

    # async def log_tg(self, text):
    #     """Log a text message to your log chat as defined in environment variable [LOG_CHAT](/start/variables#log_chat)
    #
    #     Parameters:
    #         text: Text that needs to be logged.
    #     """
    #     await self.send_message(env.LOG_CHAT, text)
    #     # No exceptions are handled for now.

    def _set_info(self):
        client = self.get_me()
        self.id = client.id
        self.username = "@"+client.username if client.username else client.first_name
        self.name = client.first_name

    @property
    def help_strings(self):
        return self.data["help_strings"]

    async def load_sudos(self):
        if self.id not in env.OWNER_ID:
            env.OWNER_ID.append(self.id)
        sudos = await mongo.list_sudo()
        listed = env.SUDO_USERS + env.OWNER_ID
        for i in listed:
            if i not in sudos:
                await mongo.add_sudo(i)
        sudos = await mongo.list_sudo()
        for s in sudos:
            if s not in SUDO_USERS:
                SUDO_USERS.append(s)
        return SUDO_USERS.copy()

    async def create_input_document(self, chat_id: int, path: str):
        media = await self.invoke(
            raw.functions.messages.UploadMedia(
                peer=await self.resolve_peer(chat_id),
                media=raw.types.InputMediaUploadedDocument(
                    mime_type=self.guess_mime_type(path) or "application/zip",
                    file=await self.save_file(path),
                    attributes=[
                        raw.types.DocumentAttributeFilename(
                            file_name=os.path.basename(path)
                        )
                    ],
                ),
            )
        )
        input_doc = raw.types.InputDocument(
            id=media.document.id,
            access_hash=media.document.access_hash,
            file_reference=media.document.file_reference,
        )
        return input_doc

    async def add_to_pack(self, chat_id: int, path: str, pack: str, emoji: str):
        i = await self.create_input_document(chat_id, path)
        await self.invoke(
            raw.functions.stickers.AddStickerToSet(
                stickerset=raw.types.InputStickerSetShortName(short_name=pack),
                sticker=raw.types.InputStickerSetItem(document=i, emoji=emoji)
            )
        )

    async def create_pack(
        self,
        chat_id: int,
        user_id: int,
        path: str,
        title: str,
        pack: str,
        emoji: str,
        type: str
    ):
        i = await self.create_input_document(chat_id, path)
        animated = None
        video = None
        if type == "video":
            video = True
        if type == "animated":
            animated = True
        await self.invoke(
            raw.functions.stickers.CreateStickerSet(
                user_id=await self.resolve_peer(user_id),
                title=title,
                short_name=pack,
                stickers=[raw.types.InputStickerSetItem(document=i, emoji=emoji)],
                videos=video,
                animated=animated
            )
        )

    def _buttons_cache(self):
        back_button_text = "<= Back <="
        main: dict = PrettyDict({"back": {}, "plugin": {}, "dirs": {}})
        rows = 2
        plugins_cmds: dict[str, dict[str, str]] = command_data["plugins_cmds"]
        main["back_to_help_button"] = [InlineKeyboardButton(back_button_text, callback_data="help")]
        for directory in plugins_cmds:
            for plugin in plugins_cmds[directory]:
                # b = [InlineKeyboardButton(name[0], callback_data="help+cmd+"+name[0]+"+plugin="+plugin) for name in plugins_cmds[directory][plugin]]
                # bc = [b[i:i + rows] for i in range(0, len(b), rows)]
                back_plug = [InlineKeyboardButton(back_button_text, callback_data="help+"+directory)]
                main["back"][plugin] = InlineKeyboardMarkup([back_plug])
                # bc.append(back_plug)
                # main["plugin"][plugin] = InlineKeyboardMarkup(bc)
                pref = env.CMD_PREFIXES[0]
                li = []
                for name in plugins_cmds[directory][plugin]:
                    x = f"`{pref}{name[0]}`"
                    if len(name) > 1:
                        aliases = [f"`{pref}{f}`" for f in name[1:]]
                        x += f" [alias -  {' | '.join(aliases)}]"
                    li.append(x)
                main["plugin"][plugin] = "**Commands**\n\n"+"\n".join(li)
            b = [InlineKeyboardButton(self.button_title(name), callback_data="help+plugin+"+name) for name in plugins_cmds[directory]]
            bc = [b[i:i + rows] for i in range(0, len(b), rows)]
            bc.append(main["back_to_help_button"])
            main["dirs"][directory] = InlineKeyboardMarkup(bc)
        b = []
        special = None
        for name in plugins_cmds:
            button = InlineKeyboardButton(self.button_title(name), callback_data="help+"+name)
            if name.lower() == "others":
                special = button
            else:
                b.append(button)
        b.append(special)
        bc = [b[i:i + rows] for i in range(0, len(b), rows)]
        main["all"] = InlineKeyboardMarkup(bc)

        # b = [InlineKeyboardButton(self.button_title(name), callback_data="help+plugin+"+name) for name in plugins_cmds]
        # bc = [b[i:i + rows] for i in range(0, len(b), rows)]
        # main["all"] = InlineKeyboardMarkup(bc)
        return main

    @staticmethod
    def button_title(text: str):
        text = text.replace("\\", "/")
        text = text.split("/")[-1].title().replace("_", " ")
        # So id in a word is not replaced
        if text.startswith("id "):
            text = text.replace("id ", "ID ")
        elif text.endswith(" id"):
            text = text.replace(" id", " ID")
        elif " id " in text:
            text = text.replace(" id ", " ID ")
        if text.lower() == "tts":
            text = "TTS"
        if text.lower() == "afk":
            text = "AFK"
        if text.lower() == "vc":
            text = "VC"
        return text

    @staticmethod
    def activate(user: "Stark" = None, bot: "Stark" = None):
        try:
            if not user:
                user = Stark()
            if not bot:
                bot = Stark(is_bot=True)
            user = [user] if not isinstance(user, list) else user
            for i in user:
                call = Calls(i)
                i.call = call
                i.bot = bot
                call.start()
                i.run(start=False)
            bot.run()
            idle()
        finally:
            logger.info("UserBot and Assistant have stopped working. For issues, visit <https://t.me/StarkBotsChat>")


__printed_2__ = False


class Calls(PyTgCalls):
    c: Stark

    def __init__(
        self,
        app: Stark,
        cache_duration: int = 120,
        overload_quiet_mode: bool = False,
        multi_thread: bool = False,
    ):
        app.__class__.__module__ = 'pyrogram.client'
        self.c = app
        global __printed_2__
        if not __printed_2__:
            logger.info("Initializing Laky-64's PyTgCalls <https://github.com/pytgcalls/pytgcalls>")
            __printed_2__ = True
        super().__init__(
            app=app,
            cache_duration=cache_duration,
            overload_quiet_mode=overload_quiet_mode,
            multi_thread=multi_thread
        )

    @staticmethod
    def stream_end():
        def decorator(func):
            setattr(func, "pytgcalls", "STREAM_END_HANDLER")
            return func
        return decorator


PyTgCallsSession.notice_displayed = True
