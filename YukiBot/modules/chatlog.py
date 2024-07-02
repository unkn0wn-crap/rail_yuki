import random
from pyrogram import Client
from pyrogram.types import Message
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputMediaVideo, Message

# Define LOGGER_ID directly
LOGGER_ID = -1002092954715
#
from YukiBot import pbot as app

@app.on_message(filters.new_chat_members, group=2)
async def join_watcher(_, message):    
    chat = message.chat
#    link = await app.export_chat_invite_link(message.chat.id)
#                 f"⌥ ɢʀᴏᴜᴘ ʟɪɴᴋ ➥ [ʜᴇʀᴇ]({link})\n"  

    bot_user = await app.get_me()
    for members in message.new_chat_members:
        if members.id == bot_user.id:
            count = await app.get_chat_members_count(chat.id)

            msg = (
                f"|| ʙᴏᴛ ᴀᴅᴅᴇᴅ ɪɴ ᴀ #ɴᴇᴡ_ɢʀᴏᴜᴘ ||\n\n"
                f"⌥ ɢʀᴏᴜᴘ ɴᴀᴍᴇ ➥ {message.chat.title}\n"
                f"⌥ ɢʀᴏᴜᴘ ɪᴅ ➥ {message.chat.id}\n"
                f"⌥ ɢʀᴏᴜᴘ ᴜsᴇʀɴᴀᴍᴇ ➥ @{message.chat.username}\n"
                f"⌥ ɢʀᴏᴜᴘ ᴍᴇᴍʙᴇʀs ➥ {count}\n\n"
                f"⌥ ᴀᴅᴅᴇᴅ ʙʏ ➥ {message.from_user.mention}"
            )
            await app.send_message(LOGGER_ID, msg)  # Send message to log group



@app.on_message(filters.left_chat_member)
async def on_left_chat_member(_, message: Message):
    if (await app.get_me()).id == message.left_chat_member.id:
        remove_by = message.from_user.mention if message.from_user else "𝐔ɴᴋɴᴏᴡɴ 𝐔sᴇʀ"
        title = message.chat.title
        username = f"@{message.chat.username}" if message.chat.username else "𝐏ʀɪᴠᴀᴛᴇ 𝐂ʜᴀᴛ"
        chat_id = message.chat.id
        left = (
            f"⌥ <b>ʙᴏᴛ #ʟᴇғᴛ_ɢʀᴏᴜᴘ</b> \n\n"
            f"⌥ ɢʀᴏᴜᴘ ɴᴀᴍᴇ ➥ {title}\n\n"
            f"⌥ ɢʀᴏᴜᴘ ɪᴅ ➥ {chat_id}\n\n"
            f"⌥ ʙᴏᴛ ʀᴇᴍᴏᴠᴇᴅ ʙʏ ➥ {remove_by}\n\n"
        )
        await app.send_message(LOGGER_ID, left)  # Send message to log group


@app.on_message(filters.new_chat_members, group=3)
async def _greet(_, message):    
    chat = message.chat

    for member in message.new_chat_members:
        count = await app.get_chat_members_count(chat.id)

        msg = (
            f"⌥ ʜᴇʏ {message.from_user.mention} ᴡᴇʟᴄᴏᴍᴇ ʜᴜᴍᴀɴ \n\n"
            f"⌥ ɢʀᴏᴜᴘ ɴᴀᴍᴇ ➥ {message.chat.title}\n"
            f"⌥ ɢʀᴏᴜᴘ ᴜsᴇʀɴᴀᴍᴇ ➥ @{message.chat.username}\n\n"
            f"⌥ ʏᴏᴜʀ ɪᴅ ➥ {member.id}\n"
            f"⌥ ʏᴏᴜʀ ᴜsᴇʀɴᴀᴍᴇ ➥ @{member.username}\n\n"
            f"⌥ ʏᴏᴜ ᴀʀᴇ {count}ᵀᴴ ᴍᴇᴍʙᴇʀ ᴏғ ᴛʜᴇ ɢʀᴏᴜᴘ."
        )
        await app.send_message(chat.id, msg)  # Send welcome message to the group
