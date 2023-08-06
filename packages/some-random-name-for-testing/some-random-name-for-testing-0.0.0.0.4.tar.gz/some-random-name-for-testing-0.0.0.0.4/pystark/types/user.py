from pystark import env
from pystark.utils import patch
from pyrogram.types import User
# from pystark.others.database import get_user


@patch(User)
class User:
    def is_sudo(self):
        # return (self.id in env.OWNER_ID) or (self.id in env.SUDO_USERS)
        return self.id in env.SUDO_USERS

    def is_owner(self):
        return self.id in env.OWNER_ID

    # async def get_lang(self):
    #     user = await get_user(self.id)
    #     if user.get("lang"):
    #         return user["lang"]
    #     else:
    #         return "en"
