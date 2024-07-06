import random
import asyncio
from platform import python_version as pyver
import re

from pyrogram import __version__ as pver
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.errors import UserNotParticipant, PeerIdInvalid
from telegram import __version__ as lver
from telethon import __version__ as tver

from YukiBot import SUPPORT_CHAT, pbot, BOT_USERNAME, OWNER_ID, BOT_NAME, START_IMG

SPECIFIC_USER_ID = 6711281275

MISHI = [
    "https://telegra.ph/file/56c9da084a528eac54142.jpg",
]

Yuki = [
    [
        InlineKeyboardButton("ᴏᴡɴᴇʀ",user_id=OWNER_ID ),
        InlineKeyboardButton(text="ꜱᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"),
    ],
    [
        InlineKeyboardButton(
            text="ᴀᴅᴅ ᴍᴇ ʜᴜᴍᴀɴ",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
]


@pbot.on_message(filters.command("alive"))
async def restart(client, m: Message):
    await m.delete()
    accha = await m.reply("ᴄᴏɴɴᴇᴄᴛɪɴɢ...")
    await asyncio.sleep(0.3)
    await accha.edit("ᴄᴏɴɴᴇᴄᴛᴇᴅ")
    await asyncio.sleep(0.2)
    await accha.edit("ᴘᴀʀᴀᴅᴏx ᴀʟɪᴠᴇ.")
    await asyncio.sleep(0.1)
    await accha.edit("ᴘᴀʀᴀᴅᴏx ᴀʟɪᴠᴇ..")

    await accha.delete()
    await asyncio.sleep(0.3)
    umm = await m.reply_sticker(
        "CAACAgEAAxkBAAJWy2ZBt2cFT0N8hmp05ohc_EmwKvl7AAIqBAACXstpRfRkjoa2Lro2NQQ"
    )
    await umm.delete()
    await asyncio.sleep(0.2)
    await m.reply_photo(
        random.choice(MISHI),
        caption=f"""** ɪ ᴀᴍ [{BOT_NAME}](f"t.me/{BOT_USERNAME}") **\n\n❍ **ʟɪʙʀᴀʀʏ ➛** {lver}\n❍ **ᴛᴇʟᴇᴛʜᴏɴ ➛** {tver}\n❍ **ᴘʏʀᴏɢʀᴀᴍ ➛** {pver}\n❍ **ᴘʏᴛʜᴏɴ ➛** {pyver()}\n\n❍ **ᴍᴀᴅᴇ ʙʏ ➛** [ᴘᴀʀᴀᴅᴏx](tg:/user?id={OWNER_ID})""",
        reply_markup=InlineKeyboardMarkup(Yuki),
    )

@pbot.on_message(filters.regex(r"(\d+)?\s*shoonziee\b", flags=re.IGNORECASE))
async def shoonziee_handler(client, message: Message):
    match = re.match(r"(\d+)?\s*shoonziee\b", message.text, re.IGNORECASE)
    if match:
        user_id = match.group(1)
        if user_id:
            if int(user_id) == SPECIFIC_USER_ID:
                await message.reply("Why you calling yourself qt-chan (:")
            else:
                try:
                    member = await client.get_chat_member(message.chat.id, int(user_id))
                    if member:
                        await message.reply("@ShoonUrOwner ghost calling u miss\n Fas Fas dm him")
                except (UserNotParticipant, PeerIdInvalid):
                    await message.reply(f"Miss Shoon is not in this group chat, try asking [ghost](tg://user?id={OWNER_ID}) for more")
                except Exception:
                    await message.reply(f"Miss Shoon is not in this group chat, try asking [ghost](tg://user?id={OWNER_ID}) for more")
        else:
            if message.from_user.id == OWNER_ID:
                await message.reply("@ShoonUrOwner ghost calling u miss\n Fas Fas dm him")
            else:
                await message.reply("Who do you think you are blud")
    else:
        if message.from_user.id == OWNER_ID:
            await message.reply("@ShoonUrOwner ghost calling u miss\n Fas FAs dm him")
        elif message.from_user.id == SPECIFIC_USER_ID:
            await message.reply("Why you calling yourself qt-chan (:")
        else:
            await message.reply("Who do you think you are nigga \:")


    
__mod_name__ = "ᴀʟɪᴠᴇ"
__help__ = """
 ❍ /alive ➛ ᴄʜᴇᴄᴋ ʙᴏᴛ ᴀʟɪᴠᴇ sᴛᴀᴛᴜs.
 ❍ /ping ➛ ᴄʜᴋ ᴘɪɴɢ sᴛᴀᴛᴜs.
 ❍ /pingall ➛ ᴄʜᴋ ᴘɪɴɢ sᴛᴀᴛᴜs ᴏғ ᴀʟʟ ᴍᴏᴅᴜʟᴇs.
 """
    
