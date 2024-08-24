from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.enums import ChatMemberStatus
import logging

# -------------------------------
# In-memory dictionary to track enabled groups
COPYRIGHT_ENABLED = {}

# -------------------------------
def time_formatter(milliseconds: float) -> str:
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"

def size_formatter(bytes: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            break
        bytes /= 1024.0
    return f"{bytes:.2f} {unit}"

# -----------------------------------------------------------
FORBIDDEN_KEYWORDS = ["porn", "xxx", "sex", "NCERT", "XII", "page", "Ans", "meiotic", "divisions", "System.in", "Scanner", "void", "nextInt"]

# Check if the user is an admin
async def is_admin(client: Client, chat_id: int, user_id: int):
    member = await client.get_chat_member(chat_id, user_id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]

# Enable or disable copyright protection in the group
@app.on_message(filters.command(["copyright"]) & filters.group)
async def copyright_handler(client: Client, message: Message):
    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply_text("Sorry, this command is for admins only.")

    if len(message.command) == 1:
        return await message.reply_text("Usage: /copyright [enable|disable]")

    action = message.command[1].lower()
    chat_id = message.chat.id

    if action == "enable":
        COPYRIGHT_ENABLED[chat_id] = True
        await message.reply_text("Copyright protection has been enabled.")
    elif action == "disable":
        COPYRIGHT_ENABLED.pop(chat_id, None)
        await message.reply_text("Copyright protection has been disabled.")
    else:
        await message.reply_text("Usage: /copyright [enable|disable]")

# -----------------------------------------------------------
@app.on_message(filters.group)
async def handle_message(client, message):
    chat_id = message.chat.id
    # If copyright protection is not enabled for the chat, return
    if not COPYRIGHT_ENABLED.get(chat_id, False):
        return

    if any(keyword in message.text for keyword in FORBIDDEN_KEYWORDS):
        logging.info(f"Deleting message with ID {message.id}")
        await message.delete()
        user_mention = message.from_user.mention
        await message.reply_text(f"{user_mention}, please do not send inappropriate content.")
    elif message.caption and any(keyword in message.caption for keyword in FORBIDDEN_KEYWORDS):
        logging.info(f"Deleting message with ID {message.id}")
        await message.delete()
        user_mention = message.from_user.mention
        await message.reply_text(f"{user_mention}, please do not send inappropriate content.")

# -----------------------------------------------------------
@app.on_edited_message(filters.group & ~filters.me)
async def delete_edited_messages(client, edited_message):
    chat_id = edited_message.chat.id
    # If copyright protection is not enabled for the chat, return
    if not COPYRIGHT_ENABLED.get(chat_id, False):
        return

    await edited_message.delete()

# ------------------------------------------------------------
def delete_long_messages(_, m):
    return len(m.text.split()) > 400

@app.on_message(filters.group & delete_long_messages)
async def delete_and_reply(_, msg):
    chat_id = msg.chat.id
    # If copyright protection is not enabled for the chat, return
    if not COPYRIGHT_ENABLED.get(chat_id, False):
        return

    await msg.delete()
    user_mention = msg.from_user.mention
    await app.send_message(msg.chat.id, f"{user_mention}, please keep your message short.")

# -----------------------------------------------------------
async def delete_pdf_files(client, message):
    if message.document and message.document.mime_type == "application/pdf":
        user_mention = message.from_user.mention
        warning_message = f"Hey {user_mention}, please don't send PDF files due to copyright concerns."
        await message.reply_text(warning_message)
        await message.delete()

@app.on_message(filters.group & filters.document)
async def message_handler(client, message):
    chat_id = message.chat.id
    # If copyright protection is not enabled for the chat, return
    if not COPYRIGHT_ENABLED.get(chat_id, False):
        return

    await delete_pdf_files(client, message)
