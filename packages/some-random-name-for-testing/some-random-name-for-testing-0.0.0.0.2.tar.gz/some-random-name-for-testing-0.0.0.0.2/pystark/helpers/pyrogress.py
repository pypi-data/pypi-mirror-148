import asyncio
import humanize
from pyrogram.errors import FloodWait, MessageNotModified


async def pyrogress(current, total, message, process):
    new_current = humanize.naturalsize(current, binary=True)
    new_total = humanize.naturalsize(total, binary=True)
    # if int(float(new_current.split()[0])) % 10 != 0:
    #     return
    try:
        percentage = round((current * 100) / total, 2)
        try:
            await message.edit(f"**{process}** \n\n**Progress :** {new_current}/{new_total} | {percentage}℅")
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except MessageNotModified:  # Sometimes pyrogram returns same i think
            pass
    except ZeroDivisionError:
        try:
            await message.edit(f"**{process}** \n\n**Progress :** {new_current}")
        except FloodWait as e:
            await asyncio.sleep(e.value)
