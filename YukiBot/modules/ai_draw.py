import random, uuid
from YukiBot import pbot as pgram
from YukiBot import aiohttpsession as session, BOT_USERNAME
from pyrogram import filters, types, enums, errors



@pgram.on_message(filters.command(['draw', 'imagine']))
async def Draw(bot, message): # Hey I'm @nandha (:
    m = message
    if len(m.text.split()) < 2:
        return await m.reply_text("ɢɪᴠᴇ ᴘʀᴏᴍᴛ ʙʟᴜᴅ !")
    url=f"https://image.pollinations.ai/prompt/{m.text.split(maxsplit=1)[1]}{random.randint(1, 10000)}"
    async with session.get(url) as response:
        image_data = await response.read()
        image = str(uuid.uuid4()) + ".jpg"
        with open(image, "wb") as file: file.write(image_data);
        await m.reply_photo(
          image, caption=f"By @{bot.me.username}"
        )



__mod_name__ = "ᴀɪ-ᴅʀᴀᴡ"

__help__ = f"""
 *Aɪ-ᴅʀᴀᴡ*:

ɢᴇɴᴇʀᴀᴛᴇ ᴀɪ ɪᴍᴀɢᴇs ʙʏ @yukii_onna_bot
Usᴇ `/draw sexy girl`
"""