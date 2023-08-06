import inspect
import functools
from pyrogram import filters as f
from pystark.types import PrettyDict
from pyrogram.handlers import MessageHandler
from pyrogram.methods.decorators.on_message import OnMessage
from pyrogram.errors import PeerIdInvalid, BotInlineDisabled
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pystark.env import CMD_PREFIXES, BOT_CMD_PREFIXES, SUDO_USERS, OWNER_ID


command_data = PrettyDict({"total_commands": 0, "all_commands": {}, "sudo_commands": [], "plugins_cmds": {}, "help_strings": {}})
bot_command_data = PrettyDict({"total_commands": 0, "all_commands": {}, "sudo_commands": [], "plugins_cmds": {}, "help_strings": {}})


class Command(OnMessage):
    @staticmethod
    def cmd(
        cmd: str | list[str] = None,
        description: str = None,
        group: int = 0,
        owner_only: bool = False,
        sudo_only: bool = True,
        private_only: bool = False,
        group_only: bool = False,
        channel_only: bool = False,
        regex: str = None,
        filters=None,
    ):
        return _command(
            is_bot=False,
            cmd=cmd,
            description=description,
            group=group,
            owner_only=owner_only,
            sudo_only=sudo_only,
            private_only=private_only,
            group_only=group_only,
            channel_only=channel_only,
            regex=regex,
            filters=filters,
        )

    @staticmethod
    def botcmd(
        cmd: str | list[str] = None,
        description: str = None,
        group: int = 0,
        owner_only: bool = False,
        sudo_only: bool = True,
        private_only: bool = False,
        group_only: bool = False,
        channel_only: bool = False,
        regex: str = None,
        filters=None,
    ):
        return _command(
            is_bot=True,
            cmd=cmd,
            description=description,
            group=group,
            owner_only=owner_only,
            sudo_only=sudo_only,
            private_only=private_only,
            group_only=group_only,
            channel_only=channel_only,
            regex=regex,
            filters=filters,
        )

    command = cmd  # alias
    bot_command = botcmd  # alias


def _command(
    is_bot: bool,
    cmd: str | list[str] = None,
    description: str = None,
    group: int = 0,
    owner_only: bool = False,
    sudo_only: bool = True,
    private_only: bool = False,
    group_only: bool = False,
    channel_only: bool = False,
    regex: str = None,
    filters=None,
):
    """This decorator is used to handle messages. Mainly used to create commands. All arguments are  optional.
    You can also use the alias ``Stark.cmd`` instead of ``Stark.command``.

    Parameters:

        cmd (str | list[str], optional): Command(s) that triggers your function. Defaults to None, which is helpful you only want to use filters argument.

        description (str,  optional): Command description to create Bot Menu. Defaults to None. [Read More](/topics/bot-menu)

        group (int, optional): Define a group for this handler. Defaults to 0. [Read More](https://docs.pyrogram.org/topics/more-on-updates#handler-groups)

        owner_only (bool, optional): Allow only owner to use this command. Defaults to False.

        sudo_only (bool, optional): Allow only sudos to use this command. Includes owner as sudo automatically. Defaults to False.

        private_only (bool, optional): Only handle messages for private chats. Bot will ignore messages in groups and channels. Defaults to False.

        group_only (bool, optional): Only handle messages for groups. Bot will ignore messages in private chats and channels. Defaults to False.

        channel_only (bool, optional): Only handle messages for channels. Bot will ignore messages in private chats and groups. Defaults to False.

        filters (pyrogram.filters, optional): Extra filters to apply in your function. Import ``filters`` from pyrogram or pystark to use this. See example below.

    Examples:

        ```python
        from pystark import Stark

        # The normal way. Bot will reply to command ``/greet`` sent anywhere and by anyone.
        @Stark.command('greet', description='Greet the user')

        # or
        @Stark.cmd('greet', 'Greet the user')

        # Bot will reply only to owner, that is, the user whose id is set as OWNER_ID in environment variables.
        # Others will be ignored.
        @Stark.command('greet', owner_only=True)

        # Bot will reply only to sudo users or owner, that is, users set as SUDO_USERS or OWNER_ID in environment variables.
        # Others will be ignored.
        @Stark.command('greet', sudo_only=True)

        # Bot will reply only if message is sent in private chat (aka pm).
        # Messages in groups and channels will be ignored.
        @Stark.command('greet', private_only=True)

        # Bot will reply only if message is sent in groups.
        # Messages in groups and private chats will be ignored.
        @Stark.command('greet', group_only=True)

        # Bot will reply only if message is sent in channels.
        # Messages in private chats and groups will be ignored.
        @Stark.command('greet', channel_only=True)


        # Filter all messages.

        # Use positive integer to execute after executing another function in default group that also filtered this message.
        @Stark.command(group=1)

        # or Use negative integer to execute before executing another function in default group that also filtered this message.
        @Stark.command(group=-1)

        # Don't use this as other functions won't work.
        @Stark.command()


        # Filter other type of messages using filters.

        # Import filters from pyrogram or pystark.
        from pystark import filters

        # Filter only media messages.
        @Stark.command(filters=filters.media)

        # Filter only text messages.
        @Stark.command(filters=filters.text)

        # Filter only messages sent by 'StarkProgrammer'.
        @Stark.command(filters=filters.user('StarkProgrammer'))

        # Filter only messages sent in 'StarkBotsChat'
        @Stark.command(filters=filters.chat('StarkBotsChat'))

        # Filter only messages with the word 'baby'.
        @Stark.command(filters=filters.regex('baby'))

        # Filter all media messages sent by bots.
        @Stark.command(filters=filters.bot & filters.media)

        # Filter all messages sent by bots except media messages.
        @Stark.command(filters=filters.bot & ~filters.media)

        # Filter either media messages or text messages.
        @Stark.command(filters=filters.text | filters.media)
        ```
    """
    if not cmd:
        sudo_only = False
    if isinstance(cmd, str):
        cmd = [cmd]
    if (owner_only or sudo_only) and cmd:
        command_data["sudo_commands"] += cmd
    if cmd and not filters:
        filters = None
    # else:
    #     filters = filters & ~f.edited
    prefixes = BOT_CMD_PREFIXES if is_bot else CMD_PREFIXES
    data = bot_command_data if is_bot else command_data
    if not cmd and not filters:
        filters_ = f.all
    elif cmd and filters:
        for c in cmd:
            if c not in data["all_commands"]:
                data["total_commands"] += 1
                data["all_commands"][c] = ""
        if cmd and regex:
            filters_ = (f.command(cmd, prefixes=prefixes) | f.regex(regex)) & filters
        else:
            filters_ = f.command(cmd, prefixes=prefixes) & filters
    elif filters:
        if regex:
            filters_ = f.regex(regex) & filters
        else:
            filters_ = filters
    else:
        for c in cmd:
            if c not in data["all_commands"]:
                data["total_commands"] += 1
                data["all_commands"][c] = ""
        if cmd and regex:
            filters_ = f.command(cmd, prefixes=prefixes) | f.regex(regex)
        else:
            filters_ = f.command(cmd, prefixes=prefixes)
    if cmd and description:
        for c in cmd:
            data["all_commands"][c] = description
    if sudo_only:
        filters_ = filters_ & f.user(SUDO_USERS)
    elif owner_only:
        filters_ = filters_ & f.user(OWNER_ID)
    if private_only:
        filters_ = filters_ & f.private
    if group_only:
        filters_ = filters_ & f.group
    if channel_only:
        filters_ = filters_ & f.channel

    def decorator(func):
        plug = inspect.getsourcefile(func)
        if "decorators" in plug:
            plug = func.__filepath__
        if "plugins" in plug:
            x = "plugins"
        else:
            x = "assistant"
        plug = plug.rsplit(x, 1)[1][1:-3]
        plug = plug.replace("\\", "/")
        if cmd:
            if "/" not in plug:
                plug = "others/"+plug
            directory, plug = plug.split("/", 1)
            if not data["plugins_cmds"].get(directory):
                data["plugins_cmds"][directory] = {}

            if data["plugins_cmds"][directory].get(plug):
                data["plugins_cmds"][directory][plug].append(cmd)
            else:
                data["plugins_cmds"][directory][plug] = [cmd]
            # data["help_strings"][cmd[0]] = get_doc(func)

        @functools.wraps(func)
        async def wrapper(*args):
            msg = args[1]
            try:
                await func(msg)
            except PeerIdInvalid:
                if cmd:
                    await msg.tell(
                        "Please PM me so I really know you!",
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("Start Me", url=f"https://t.me/{args[0].username[1:]}?start=")]
                        ])
                    )
                else:
                    await msg.tell("PEER_ID_INVALID")
            except BotInlineDisabled:
                await msg.tell("Inline Mode is currently disabled. Please turn it on using @BotFather!")

        if not hasattr(func, "handlers"):
            wrapper.handlers = []
        wrapper.handlers.append((MessageHandler(wrapper, filters_), group))

        return wrapper

    return decorator
