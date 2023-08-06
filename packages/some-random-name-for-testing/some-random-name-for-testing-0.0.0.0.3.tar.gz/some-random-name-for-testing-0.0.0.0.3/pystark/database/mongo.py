import asyncio
from datetime import datetime
from pystark.utils import patch
from pystark.env import MONGO_URL
from pymongo.command_cursor import CommandCursor
from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticDatabase, AgnosticCollection


@patch(AgnosticCollection)
class AgnosticCollection(AgnosticCollection):
    async def get(self, document: dict) -> dict:
        return await self.find_one(document)

    async def mget(self, document: dict) -> list[dict]:
        ans = []
        async for doc in self.find(document):
            ans.append(doc)
        return ans

    async def set(self, document: dict) -> bool:
        a, b = {}, {}
        for i in document:
            if i in ["chat_id", "name"]:
                c = a
            else:
                c = b
            c[i] = document[i]
        ans = await self.get(a)
        if not ans:
            return await self.insert_one(document)
        else:
            return await self.update_one(a, {"$set": b})

    async def delete(self, document: dict) -> bool:
        return await self.find_one_and_delete(document)

    async def get_all(self) -> list[dict]:
        ans = []
        async for doc in self.find():
            ans.append(doc)
        return ans


class MongoDB:
    def __init__(self, url: str = MONGO_URL):
        self.client = AsyncIOMotorClient(url)
        self.client.get_io_loop = asyncio.get_running_loop
        self.db: AgnosticDatabase = self.client["pystark"]
        self.notes_col: AgnosticCollection = self.db["notes"]
        self.filters_col: AgnosticCollection = self.db["filters"]
        self.lists_col: AgnosticCollection = self.db["lists"]
        self.greetings_col: AgnosticCollection = self.db["greetings"]
        self.data_col: AgnosticCollection = self.db["data"]
        # self.chats_col: AgnosticCollection = self.db["chats"]
        self._default_dbs = ["admin", "local"]
        self._default_response = "value"

    # ---------------------------- Filters --------------------------- #

    async def get_all_filters(self, chat_id: int) -> dict[str, str]:
        return await self._col_get_all(self.filters_col, chat_id)

    async def get_filter(self, chat_id: int, name: str) -> str:
        return await self._col_get(self.filters_col, chat_id, name)

    async def set_filter(self, chat_id: int, name: str, value: str) -> bool:
        return await self._col_set(self.filters_col, chat_id, name, value)

    async def delete_filter(self, chat_id: int, name: str) -> bool:
        return await self._col_delete(self.filters_col, chat_id, name)

    async def delete_all_filters(self, chat_id: int) -> int:
        return await self._col_delete_all(self.filters_col, chat_id)

    # ---------------------------- Notes --------------------------- #

    async def get_all_notes(self, chat_id: int) -> dict[str, str]:
        return await self._col_get_all(self.notes_col, chat_id)

    async def get_note(self, chat_id: int, name: str) -> str:
        return await self._col_get(self.notes_col, chat_id, name)

    async def set_note(self, chat_id: int, name: str, value: str) -> bool:
        return await self._col_set(self.notes_col, chat_id, name, value)

    async def delete_note(self, chat_id: int, name: str) -> bool:
        return await self._col_delete(self.notes_col, chat_id, name)

    async def delete_all_notes(self, chat_id: int) -> int:
        return await self._col_delete_all(self.notes_col, chat_id)

    # ---------------------------- Lists --------------------------- #

    async def get_all_lists(self, chat_id: int) -> dict[str, str]:
        return await self._col_get_all(self.lists_col, chat_id)

    async def get_list(self, chat_id: int, name: str) -> str:
        return await self._col_get(self.lists_col, chat_id, name)

    async def set_list(self, chat_id: int, name: str, value: str) -> bool:
        return await self._col_set(self.lists_col, chat_id, name, value)

    async def delete_list(self, chat_id: int, name: str) -> bool:
        return await self._col_delete(self.lists_col, chat_id, name)

    async def delete_all_lists(self, chat_id: int) -> int:
        return await self._col_delete_all(self.lists_col, chat_id)

    # ---------------------------- Users --------------------------- #

    # async def get_all_users(self) -> list[int]:
    #     return [a["user_id"] for a in await self.users_col.get_all()]
    #
    # async def get_user(self, user_id: int) -> str:
    #     return await self.users_col.get({"user_id": user_id})
    #
    # async def set_user(self, user_id: int) -> bool:
    #     return await self.users_col.set({"user_id": user_id})
    #
    # async def count_users(self) -> int:
    #     return len(await self.users_col.get_all())
    #
    # async def delete_user(self, chat_id: int, name: str) -> bool:
    #     return await self._col_delete(self.users_col, chat_id, name)

    # ---------------------------- Chats --------------------------- #

    # async def get_all_chats(self) -> list[int]:
    #     return [a["chat_id"] for a in await self.chats_col.get_all()]
    #
    # async def get_chat(self, chat_id: int) -> str:
    #     return await self.chats_col.get({"chat_id": chat_id})
    #
    # async def set_chat(self, chat_id: int) -> bool:
    #     return await self.chats_col.set({"chat_id": chat_id})
    #
    # async def count_chats(self) -> int:
    #     return len(await self.chats_col.get_all())
    #
    # async def delete_chat(self, chat_id: int, name: str) -> bool:
    #     return await self._col_delete(self.chats_col, chat_id, name)

    # ---------------------------- Special --------------------------- #

    # ------------------------ Sudos ----------------------- #

    async def list_sudo(self) -> list[int]:
        data = await self.data_col.get({"name": "sudos"})
        if not data:
            await self.data_col.set({"name": "sudos", "value": []})
            return []
        return (await self.data_col.get({"name": "sudos"}))["value"]

    async def add_sudo(self, user_id: int) -> bool:
        sudos = await self.list_sudo()
        sudos.append(user_id)
        return await self.data_col.set({"name": "sudos", "value": sudos})

    async def delete_sudo(self, user_id: int) -> bool:
        sudos = await self.list_sudo()
        if user_id in sudos:
            sudos.remove(user_id)
        return await self.data_col.set({"name": "sudos", "value": sudos})

    # ------------------------ AFKs ----------------------- #

    async def set_afk(self, user_id: int, username: str, reason: str = None) -> bool:
        return await self.data_col.set({"user_id": user_id, "name": "afk", "value": reason, "time": datetime.now(), "username": username})

    async def get_afk(self, user_id: int) -> dict:
        data = await self.data_col.get({"user_id": user_id, "name": "afk"})
        return data

    async def get_all_afk(self) -> list[dict]:
        data = await self.data_col.mget({"name": "afk"})
        return data

    async def reset_afk(self, user_id: int) -> bool:
        return await self.data_col.delete({"user_id": user_id, "name": "afk"})

    # ------------------------ Replicate ----------------------- #

    async def get_replicate(self) -> dict:
        return await self.data_col.get({"name": "replicate"})

    async def set_replicate(self, first_name: str, last_name: str, bio: str, dp: bytes, video: bool) -> bool:
        return await self.data_col.set(
            {"name": "replicate", "first_name": first_name, "last_name": last_name, "bio": bio, "dp": dp, "video": video}
        )

    async def reset_replicate(self) -> bool:
        return await self.data_col.delete({"name": "replicate"})

    # ------------------------ Packs ----------------------- #

    async def get_pack(self, user_id: int, type: str) -> str:
        data = await self.data_col.get({"name": "packs", "user_id": user_id})
        if data:
            data = data.get(type)
        return data

    async def set_pack(self, user_id: int, value: str, type: str) -> bool:
        return await self.data_col.set(
            {"name": "packs", "user_id": user_id, type: value}
        )

    # ------------------------ AI ----------------------- #

    async def ai(self, id: int, delete: bool, user: bool) -> bool:
        if user:
            t = "users"
        else:
            t = "chats"
        q = await self.data_col.get({"name": "ai"})
        li = None
        if q:
            li = q.get(t)
        if not li:
            li = []
        if delete:
            if id in li:
                li.remove(id)
        else:
            if id not in li:
                li.append(id)
        return await self.data_col.set({"name": "ai", t: li})

    async def set_ai(self, id: int, user: bool = True) -> bool:
        return await self.ai(id, False, user)

    async def delete_ai(self, id: int, user: bool = True) -> bool:
        return await self.ai(id, True, user)

    async def get_all_ai(self) -> dict:
        return await self.data_col.get({"name": "ai"})

    # ---------------------------- Greetings --------------------------- #

    async def get_greetings(self, chat_id: int) -> dict:
        return await self.greetings_col.get({"chat_id": chat_id})

    async def set_greetings(
        self,
        chat_id: int,
        welcome: str = None,
        goodbye: str = None,
        welcome_on: bool = None,
        goodbye_on: bool = None,
    ) -> bool:
        doc = {"chat_id": chat_id}
        if welcome:
            doc["welcome"] = welcome
        if goodbye:
            doc["goodbye"] = goodbye
        if welcome_on:
            doc["welcome_on"] = welcome_on
        if goodbye_on:
            doc["goodbye_on"] = goodbye_on
        return await self.greetings_col.set(doc)

    async def delete_greetings(self, chat_id: int, name: str) -> bool:
        return await self._col_delete(self.greetings_col, chat_id, name)

    # ---------------------------- Other --------------------------- #

    async def documents(self):
        ...

    async def total_documents(self) -> int:
        ...

    # ------------------ Database and Collections --------------------- #

    async def database_names(self, remove: bool = True) -> list[str]:
        ans: list[str] = await self.client.list_database_names()
        if remove:
            ans = [f for f in ans if f not in self._default_dbs]
        return ans

    async def databases(self, remove: bool = True) -> list[dict]:
        cursor = await self.client.list_databases()
        ans = await self._iter_cursor(cursor)
        if remove:
            ans = [f for f in ans if f["name"] not in self._default_dbs]
        return ans

    @staticmethod
    async def collection_names(db: AgnosticDatabase) -> list[str]:
        return await db.list_collection_names()

    async def collections(self, db: AgnosticDatabase) -> list[dict]:
        cursor = await db.list_collections()
        return await self._iter_cursor(cursor)

    # ---------------------- Private Methods --------------------- #

    async def _col_get(self, col: AgnosticCollection, chat_id: int, name: str) -> str | None:
        x = await col.get(self._generic_dict(chat_id, name))
        if x:
            return x[self._default_response]
        return

    async def _col_set(self, col: AgnosticCollection, chat_id: int, name: str, value: str) -> bool:
        return await col.set(self._generic_dict(chat_id, name, value))

    async def _col_delete(self, col: AgnosticCollection, chat_id: int, name: str) -> bool:
        return await col.delete(self._generic_dict(chat_id, name))

    async def _col_get_all(self, col: AgnosticCollection, chat_id: int) -> dict[str, str]:
        ans = {}
        async for doc in col.find(self._generic_dict(chat_id)):
            ans[doc["name"]] = doc["value"]
        return ans

    async def _col_delete_all(self, col: AgnosticCollection, chat_id: int) -> int:
        res = await col.delete_many(self._generic_dict(chat_id))
        return res.deleted_count

    # ---------------------------- Cursor --------------------------- #

    async def _iter_cursor(self, cursor) -> list[dict]:
        if isinstance(cursor, CommandCursor):
            d = self._iter_cursor_sync(cursor)
        else:
            d = await self._iter_cursor_async(cursor)
        return d

    @staticmethod
    def _iter_cursor_sync(cursor) -> list[dict]:
        data = []
        try:
            while True:
                data.append(cursor.next())
        except StopIteration:
            pass
        return data

    @staticmethod
    async def _iter_cursor_async(cursor) -> list[dict]:
        data = []
        try:
            while True:
                data.append(await cursor.next())
        except StopAsyncIteration:
            pass
        return data

    @staticmethod
    def _generic_dict(chat_id: int, name: str = "", value: str = "") -> dict:
        ans = {"chat_id": chat_id}
        if name:
            ans["name"] = name
        if value:
            ans["value"] = value
        return ans

    # ---------------------------------------------------------------- #

    async def print(self):
        x = await self.database_names()
        print("Database Names: ", x)
        x = await self.databases()
        print("Databases Info: ", x)
        x = await self.collection_names(self.db)
        print("Collections Names in main database: ", x)
        x = await self.collections(self.db)
        print("Collections in main database: ", x)


mongo = MongoDB()
