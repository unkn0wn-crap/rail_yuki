from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from YukiBot import pbot as app
import logging

# ----------------------------------------
# Global variable to track copyright module state
copyright_module_enabled = False

# Define forbidden keywords
FORBIDDEN_KEYWORDS = ["porn", "xxx", "sex", "NCERT", "XII", "page", "Ans", "meiotic", "divisions", "System.in", "Scanner", "void", "nextInt"]

OWNER_ID = 6259443940

# Function to check if user is an admin or the owner
async def is_admin_or_owner(client, message):
    user_id = message.from_user.id

    # Check if the user is the bot owner
    if user_id == OWNER_ID:
        logging.info(f"User {user_id} is the bot owner.")
        return True

    try:
        # Check if the user is an admin or the creator of the group
        chat_member = await client.get_chat_member(message.chat.id, user_id)
        if chat_member.status in ["administrator", "creator"]:
            logging.info(f"User {user_id} is an admin or creator in the group.")
            return True
        else:
            logging.info(f"User {user_id} is not an admin or creator.")
            return False

    except Exception as e:
        logging.error(f"Error checking admin status: {e}")
        return False

# -------------------------------

@app.on_message(filters.command("copyright") & filters.group)
async def copyright_toggle(client, message):
    global copyright_module_enabled

    # Check if the user is an admin or the bot owner
    if not await is_admin_or_owner(client, message):
        await message.reply_text("❌ You don't have permission to do this!")
        return

    command = message.command[1] if len(message.command) > 1 else None

    if command == "enable":
        copyright_module_enabled = True
        await message.reply_text("📄 Copyright module enabled!")
    elif command == "disable":
        copyright_module_enabled = False
        await message.reply_text("📄 Copyright module disabled!")
    else:
        await message.reply_text("Usage: /copyright [enable|disable]")

# ----------------------------------------------------------
@app.on_message(filters.group & filters.text)
async def handle_message(client, message):
    global copyright_module_enabled

    if copyright_module_enabled:
        if any(keyword in message.text for keyword in FORBIDDEN_KEYWORDS):
            logging.info(f"Deleting message with ID {message.id}")
            await message.delete()
            user_mention = message.from_user.mention
            await message.reply_text(f"{user_mention}, please refrain from sending such content.")

# -----------------------------------------------------------
@app.on_message(filters.group & filters.document)
async def message_handler(client, message):
    global copyright_module_enabled

    if copyright_module_enabled:
        await delete_pdf_files(client, message)

async def delete_pdf_files(client, message):
    if message.document and message.document.mime_type == "application/pdf":
        user_mention = message.from_user.mention
        warning_message = f"Hey {user_mention}, please don't send PDF files to avoid copyright claims."
        await message.reply_text(warning_message)
        await message.delete()

# -----------------------------------------------------------
@app.on_edited_message(filters.group & ~filters.me)
async def delete_edited_messages(client, edited_message):
    global copyright_module_enabled

    if copyright_module_enabled:
        await edited_message.delete()

# -----------------------------------------------------------
def delete_long_messages(_, m):
    return len(m.text.split()) > 400

@app.on_message(filters.group & filters.private & delete_long_messages)
async def delete_and_reply(_, msg):
    global copyright_module_enabled

    if copyright_module_enabled:
        await msg.delete()
        user_mention = msg.from_user.mention
        await app.send_message(msg.chat.id, f"{user_mention}, please keep your message short.")
