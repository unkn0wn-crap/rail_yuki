# [ import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden
from YukiBot import pbot as app

#--------------------------
MUST_JOIN = "Blyat_u"
#------------------------

PDOX = [
    "https://telegra.ph/file/75d1f57a0b12e993ba95c.jpg",
]

async def check_user_join_channel(user_id):
    try:
        await app.get_chat_member(MUST_JOIN, user_id)
        return True
    except UserNotParticipant:
        return False

@app.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(app: Client, msg: Message):
    if not await check_user_join_channel(msg.from_user.id):
        if MUST_JOIN.isalpha():
            link = "https://t.me/" + MUST_JOIN
        else:
            chat_info = await app.get_chat(MUST_JOIN)
            link = chat_info.invite_link
        try:
            await msg.reply_photo(
                random.choice(PDOX), caption=f"𓂀 sᴜᴘ, ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜsᴇ ᴍᴇ, ᴛʜᴇɴ ʏ ɴᴏᴛ ᴊᴏɪɴ @Blyat_u. ɪᴛ ᴡᴏᴜʟᴅ ʙᴇ ɢʀᴇᴀᴛ ",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ", url="https://t.me/paradoxdump"),
                            InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/paradoxdump"),
                        ],
                    ]
                )
            )
            await msg.stop_propagation()
        except ChatWriteForbidden:
            pass
        return
]
