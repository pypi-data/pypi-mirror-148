import os
import asyncio
from .user import User
from .chat import Chat
from ..client import Stark
from pystark.utils import patch
from pyrogram.errors import MessageTooLong
from pyrogram.types import Message, MessageEntity


@patch(Message)
class Message(Message):
    _client: Stark
    from_user: User
    chat: Chat

    async def tell(
        self,
        text: str,
        format: str | tuple = None,
        del_in: int = 0,
        quote: bool = True,
        parse_mode: str | None = object,
        entities: list["MessageEntity"] = None,
        disable_web_page_preview: bool = True,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        schedule_date: int = None,
        reply_markup=None
    ) -> "Message":
        try:
            langs_data = self._client.langs_data
            if text in langs_data["en"]:
                text = langs_data["en"][text]
                if format:
                    if isinstance(format, str):
                        format = (format,)
                    text = text.format(*format)
            if self.from_user.is_self:
                reply = await self.edit(
                    str(text),
                    parse_mode=parse_mode,
                    entities=entities,
                    disable_web_page_preview=disable_web_page_preview,
                    reply_markup=reply_markup,
                )
            else:
                reply = await self.reply(
                    str(text),
                    quote=quote,
                    parse_mode=parse_mode,
                    entities=entities,
                    disable_notification=disable_notification,
                    reply_to_message_id=reply_to_message_id,
                    schedule_date=schedule_date,
                    disable_web_page_preview=disable_web_page_preview,
                    reply_markup=reply_markup,
                )
        except MessageTooLong:
            reply = await self.reply(
                "Sending as document...",
                quote=quote,
                parse_mode=parse_mode,
                entities=entities,
                disable_notification=disable_notification,
                reply_to_message_id=reply_to_message_id,
                schedule_date=schedule_date,
                disable_web_page_preview=disable_web_page_preview,
                reply_markup=reply_markup,
            )
            file = f'{reply.message_id}.txt'
            with open(file, 'w+', encoding="utf-8") as f:
                f.write(text)
            await reply.delete()
            reply = await self.reply_document(
                document=file,
                caption="Output",
                quote=quote,
                parse_mode=parse_mode,
                caption_entities=entities,
                disable_notification=disable_notification,
                reply_to_message_id=reply_to_message_id,
                schedule_date=schedule_date,
                reply_markup=reply_markup,
            )
            os.remove(file)
        if del_in:
            await asyncio.sleep(del_in)
            await reply.delete()
        return reply

    @property
    def args(self, split: str = " ") -> list[str]:
        """List arguments passed in a message. Removes first word (the command itself)

        Parameters:

            split (str, optional): Define how to split the arguments, defaults to whitespace.

        Example:

            If text is `/start reply user`, return value would be `["reply", "user"]`
        """
        args: list[str] = self.text.markdown.split(split)
        args.pop(0)
        if args:
            args[0] = args[0].strip()
            if "\n" in args[0]:
                wtf = args[0]
                f, s = wtf.split("\n", 1)
                args[0] = f
                args.insert(1, s)
        return args

    @property
    def input(self) -> str | None:
        """Input passed in a message. Removes first word (the command itself)

        Example:

            If text is `/start reply user`, return value would be `reply user`
        """
        i = self.text.markdown.split(" ", 1)
        if len(i) > 1 and i[1]:
            return i[1]
        return

    @property
    def ref(self) -> int | str | None:
        """Returns the referred user's id or username. To get the full user, use method `get_ref_user`

        Useful to get the referent user's id or username for a command.
        If command was replied to a message, the replied message's user id is returned.
        Otherwise, the first argument of command is returned (which isn't guaranteed to be an actual user or an id).

        **Example**:

            If command `/ban` was replied to a user's message, user id (`message.reply_to_message.from_user.id`) is returned.

            If command `/ban 12345678` was sent, user id (integer) `12345678` is returned.

            If command `/ban StarkProgrammer` was sent, username (string) `StarkProgrammer` is returned.

            If command `/ban 87654321 12345678` was sent, user id (integer) `87654321` is returned but `12345678` is ignored because it's not the first argument.

            If command `/ban` was sent with no arguments and was also not a reply to any message, None is returned.

            If command `/ban ok` was sent, "ok" is returned which isn't an actual user but will not raise exception.
        """
        if self.reply_to_message:
            return self.reply_to_message.from_user.id
        args = self.args
        if not args:
            return
        return args[0] if not args[0].isdigit() else int(args[0])

    async def get_ref_user(self) -> User | None:
        """Returns the full referred user. To get only user id or username, use property `ref` as it's faster.

        Useful to get the referent of a command.
        If command was replied to a message, the replied message's user is returned.
        Otherwise, the first argument of command is used to get the user.

        !!! note

            If command is not replied then first argument of command is considered user id or username. It's on you to handle PeerIdInvalid and UsernameInvalid

        **Example**:

            If command `/ban` was replied to a user's message, user (`message.reply_to_message.from_user`) is returned.

            If command `/ban 12345678` was sent, the user instance of user with id `12345678` is returned.

            If command `/ban StarkProgrammer` was sent, the user instance of user with username `StarkProgrammer` is returned.

            If command `/ban 87654321 12345678` was sent, the user instance of user with id `87654321` is returned but `12345678` is ignored because it's not the first argument.

            If command `/ban` was sent with no arguments and was also not a reply to any message, None is returned.
        """
        if self.reply_to_message:
            return self.reply_to_message.from_user
        args = self.args
        if not args:
            return
        user = args[0] if not args[0].isdigit() else int(args[0])
        user = await self._client.get_users(user)
        return user

    async def get_ref_chat(self) -> Chat | None:
        args = self.args
        if not args:
            return
        chat = args[0] if not args[0].isdigit() else int(args[0])
        chat = await self._client.get_chat(chat)
        return chat

    async def get_aor(self) -> str:
        """Get arg or reply text"""
        if self.reply_to_message:
            return self.reply_to_message.text.markdown
        else:
            return self.input

    # async def extract_data(self, string: str = "", replace: bool = True, user=None) -> (str, InlineKeyboardMarkup):
    #     if not string:
    #         if self.reply_to_message:
    #             string = self.reply_to_message.text.markdown if self.reply_to_message.text else self.reply_to_message.caption.markdown
    #         else:
    #             string = self.text.markdown.split(" ", 1)[-1]
    #     text, buttons = await extract_msg_data(string)
    #     if not user:
    #         user = self.from_user
    #     if replace:
    #         if "{first}" in text:
    #             text = text.replace("{first}", user.first_name)
    #         if "{last}" in text:
    #             if user.last_name:
    #                 text = text.replace("{last}", user.last_name)
    #             else:
    #                 if "{last} " in text:
    #                     text = text.replace("{last} ", "")
    #                 elif " {last}" in text:
    #                     text = text.replace(" {last}", "")
    #                 else:
    #                     text = text.replace("{last} ", "")
    #         if "{fullname}" in text:
    #             if user.last_name:
    #                 name = user.first_name + " " + user.last_name
    #             else:
    #                 name = user.first_name
    #             text = text.replace("{fullname}", name)
    #         if "{username}" in text:
    #             text = text.replace("{username}", "@"+user.username if user.username else user.mention)
    #         if "{mention}" in text:
    #             text = text.replace("{mention}", user.mention)
    #         if "{chatid}" in text:
    #             text = text.replace("{chatid}", str(self.chat.id))
    #         if "{userid}" in text:
    #             text = text.replace("{userid}", str(user.id))
    #         if "{id}" in text:  # {userid} alias
    #             text = text.replace("{id}", str(user.id))
    #         if "{chatname}" in text:
    #             text = text.replace("{chatname}", self.chat.title)
    #         if "{chat}" in text:  # {chatname} alias
    #             text = text.replace("{chat}", self.chat.title)
    #         if "{count}" in text:
    #             chat = await self._client.get_chat(self.chat.id)
    #             text = text.replace("{count}", str(chat.members_count))
    #         # if "{rules}" in text:
    #         #     if buttons:
    #         #         buttons = buttons.inline_keyboard.copy()
    #         #         buttons.insert()
    #     return text, buttons

    @property
    def client(self):
        return self._client

    @property
    def c(self):
        return self._client
