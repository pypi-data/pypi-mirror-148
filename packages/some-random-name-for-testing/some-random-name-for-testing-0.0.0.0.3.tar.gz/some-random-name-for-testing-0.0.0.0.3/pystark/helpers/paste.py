from .requests import request


async def paste(text: str, bin: str = "haste"):
    if bin.endswith("bin"):
        bin = bin[:-3]
    if bin == "space":
        base = "https://spaceb.in/"
        path = "api/v1/documents"
        res = await request(base+path, data={"content": text, "extension": "txt"})
        link = base+res["payload"]["id"]
    elif bin == "neko":
        base = "https://nekobin.com/"
        path = "api/documents"
        res = await request(base+path, json={"content": text})
        link = base+res["result"]["key"]
    elif bin == "bat":
        base = "https://batbin.me/"
        path = "api/v2/paste"
        res = await request(base+path, data=text)
        if res["success"]:
            link = base+res["message"]
        else:
            link = res["message"]
    else:
        # if not bin == "haste":
        #     logger.log(f"'{bin}' not found. Using 'haste'")
        base = "https://hastebin.com/"
        path = "documents"
        res = await request(base+path, data=text)
        link = base+res["key"]
    return link
