import os
from .logger import logger
from dotenv import load_dotenv
from pystark import settings as s
from importlib import import_module


load_dotenv(".env")

# API_ID = os.environ.get("API_ID", "").strip()
# API_HASH = os.environ.get("API_HASH", "").strip()
# BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()
BOT_SESSION = os.environ.get("BOT_SESSION", "").strip()
SESSIONS = os.environ.get("SESSIONS", "").strip()
if SESSIONS:
    SESSIONS = SESSIONS.split(" ")
OWNER_ID = os.environ.get("OWNER_ID", "").strip().split(" ")
LOG_CHAT = os.environ.get("LOG_CHAT", "").strip()
# SONGS_CHAT = os.environ.get("SONGS_CHAT", "").strip()
SUDO_USERS = os.environ.get("SUDO_USERS", "").strip().split(" ")
MONGO_URL = os.environ.get("MONGO_URL", "").strip()
ARQ = os.environ.get("ARQ", "").strip()
CMD_PREFIXES = list(os.environ.get("CMD_PREFIXES", "").strip())
while "" in CMD_PREFIXES:
    CMD_PREFIXES.remove("")
if not CMD_PREFIXES:
    CMD_PREFIXES = ["."]

BOT_CMD_PREFIXES = list(os.environ.get("BOT_CMD_PREFIXES", "").strip())
while "" in BOT_CMD_PREFIXES:
    BOT_CMD_PREFIXES.remove("")
if not BOT_CMD_PREFIXES:
    BOT_CMD_PREFIXES = ["/"]

# if not API_ID:
#     logger.critical("No API_ID found. Exiting...")
#     raise SystemExit
# if not API_HASH:
#     logger.critical("No API_HASH found. Exiting...")
#     raise SystemExit
if not SESSIONS:
    logger.critical("No session (SESSIONS) found. Exiting...")
    raise SystemExit
if not BOT_SESSION:
    logger.critical("No BOT_SESSION found. Exiting...")
    raise SystemExit
if not LOG_CHAT:
    LOG_CHAT = 0

# try:
#     API_ID = int(API_ID)
# except ValueError:
#     logger.critical("API_ID is not a valid integer. Exiting...")
#     raise SystemExit

owners = []
for o in OWNER_ID:
    if isinstance(o, str) and o.isdigit():
        owners.append(int(o))
    else:
        owners.append(o)
OWNER_ID = owners

sudos = []
for o in SUDO_USERS:
    if o.isdigit():
        sudos.append(int(o))
    else:
        sudos.append(o)
SUDO_USERS = sudos

# LOG_CHAT = -1001567003949  # Stark Bots Logs
try:
    LOG_CHAT = int(LOG_CHAT)
except ValueError:
    logger.critical("LOG_CHAT is not a valid integer. Exiting...")
    raise SystemExit

# try:
#     SONGS_CHAT = int(SONGS_CHAT)
# except ValueError:
#     logger.critical("SONGS_CHAT is not a valid integer. Exiting...")
#     raise SystemExit


default = None


def get_settings():
    global default
    if default:
        return default
    if os.path.exists('settings.py'):
        mod = __import__("settings")
    else:
        # logger.warn("Settings file not found. Default values will be used.")
        mod = import_module('pystark.settings')
    if "DIRECTORY" in mod.__dict__:
        dire = getattr(mod, "DIRECTORY")
        if "PLUGINS" not in mod.__dict__:
            setattr(mod, "PLUGINS", f"{dire}/plugins")
        if "BOT_PLUGINS" not in mod.__dict__:
            setattr(mod, "BOT_PLUGINS", f"{dire}/assistant")
        if "LOCALIZATION" not in mod.__dict__:
            setattr(mod, "LOCALIZATION", f"{dire}/localization")
    if CMD_PREFIXES:
        setattr(mod, "CMD_PREFIXES", CMD_PREFIXES)
    if BOT_CMD_PREFIXES:
        setattr(mod, "BOT_CMD_PREFIXES", BOT_CMD_PREFIXES)
    for i in dir(s):
        if not i.isupper():
            continue
        try:
            getattr(mod, i)
        except AttributeError:
            setattr(mod, i, getattr(s, i))
    prefixes = getattr(mod, "CMD_PREFIXES")
    if not isinstance(prefixes, list):
        setattr(mod, "CMD_PREFIXES", [prefixes])

    os.environ["TIMEZONE"] = getattr(mod, 'TIMEZONE')
    default = mod  # Cache
    return mod


class Settings:
    DIRECTORY: str
    PLUGINS: str | list[str]
    BOT_PLUGINS: str | list[str]
    SET_BOT_MENU: bool
    CMD_PREFIXES: list[str]
    BOT_CMD_PREFIXES: list[str]
    # ADDONS: list[str]
    LOCALIZATION: str
    START: str
    HELP: str
    ABOUT: str
    TIMEZONE: str
    START_IN_GROUPS: str


settings: Settings = get_settings()
