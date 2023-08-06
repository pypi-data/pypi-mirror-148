from pystark.utils import patch
from pyrogram.types import Chat
from pyrogram.types import ChatMember
# from pystark.others.database import get_chat


@patch(Chat)
class Chat:
    async def get_admins(self) -> list[ChatMember]:
        return await self.get_members(filter="administrators")

    # async def get_lang(self):
    #     chat = await get_chat(self.id)
    #     if chat.get("lang"):
    #         return chat["lang"]
    #     else:
    #         return "en"
