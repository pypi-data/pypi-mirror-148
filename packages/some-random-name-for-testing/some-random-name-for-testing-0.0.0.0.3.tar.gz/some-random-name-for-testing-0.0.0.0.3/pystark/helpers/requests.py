import aiohttp
from aiohttp import ClientResponse


aio = aiohttp.ClientSession()


class Request:
    @staticmethod
    async def request(method: str, url: str, get_json: bool = True, **kwargs) -> dict[str] | ClientResponse:
        if method.lower() == "get":
            response = await aio.get(url, **kwargs)
        else:
            response = await aio.post(url, **kwargs)
        response.raise_for_status()
        if get_json:
            return await response.json()
        else:
            return response

    async def get(self, url: str, params: dict = None, get_json: bool = True, **kwargs):
        return await self.request("get", url, params=params, get_json=get_json, **kwargs)

    async def post(self, url: str, json: dict = None, data: str | dict = None, get_json: bool = True, **kwargs):
        return await self.request("post", url, json=json, data=data, get_json=get_json, **kwargs)


request = Request()
