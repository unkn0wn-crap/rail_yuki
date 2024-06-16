import html
import json
import re
import requests
from telegram import (
    CallbackQuery,
    Chat,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    Update,
    User,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.utils.helpers import mention_html
from typing import Optional

import YukiBot.modules.sql.chatbot_sql as sql
from YukiBot import BOT_ID, BOT_NAME, BOT_USERNAME, dispatcher
from YukiBot.modules.helper_funcs.chat_status import user_admin, user_admin_no_reply
from YukiBot.modules.log_channel import gloggable

@user_admin_no_reply
@gloggable
def mukeshrm(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"rm_chat\((.+?)\)", query.data)
    if match:
        chat_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat
        sql.rem_mukesh(chat_id)
        update.effective_message.edit_text(
            f"❍ <b>{html.escape(chat.title)}</b>\n"
            f"❍ ᴀɪ ᴅɪꜱᴀʙʟᴇᴅ\n"
            f"❍ <b>ᴀᴅᴍɪɴ ➛</b> {mention_html(user.id, html.escape(user.first_name))}\n",
            parse_mode=ParseMode.HTML
        )

@user_admin_no_reply
@gloggable
def mukeshadd(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"add_chat\((.+?)\)", query.data)
    if match:
        chat_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat
        sql.set_mukesh(chat_id)
        update.effective_message.edit_text(
            f"❍ <b>{html.escape(chat.title)}</b>\n"
            f"❍ ᴀɪ ᴇɴᴀʙʟᴇᴅ\n"
            f"❍ <b>ᴀᴅᴍɪɴ ➛</b> {mention_html(user.id, html.escape(user.first_name))}\n",
            parse_mode=ParseMode.HTML
        )

@user_admin
@gloggable
def mukesh(update: Update, context: CallbackContext):
    message = update.effective_message
    msg = "❍ ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴩᴛɪᴏɴ ᴛᴏ ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ ᴄʜᴀᴛʙᴏᴛ"
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="ᴇɴᴀʙʟᴇ", callback_data=f"add_chat({message.chat_id})"),
                InlineKeyboardButton(text="ᴅɪsᴀʙʟᴇ", callback_data=f"rm_chat({message.chat_id})"),
            ],
        ]
    )
    message.reply_text(
        text=msg,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )

def mukesh_message(context: CallbackContext, message):
    reply_message = message.reply_to_message
    if message.text.lower() == "mukesh":
        return True
    elif BOT_USERNAME in message.text.upper():
        return True
    elif reply_message:
        if reply_message.from_user.id == BOT_ID:
            return True
    else:
        return False

def chatbot(update: Update, context: CallbackContext):
    message = update.effective_message
    chat_id = update.effective_chat.id
    bot = context.bot
    if sql.is_mukesh(chat_id):
        return

    if message.text and not message.document:
        if not mukesh_message(context, message):
            return
        bot.send_chat_action(chat_id, action="typing")
        url = f"https://mukesh-api.vercel.app/chatbot/{message.text}"
        try:
            response = requests.get(url).json()["results"]
            message.reply_text(response)
        except Exception as e:
            message.reply_text(f"Error: {e}")

CHATBOTK_HANDLER = CommandHandler("chatbot", mukesh, run_async=True)
ADD_CHAT_HANDLER = CallbackQueryHandler(mukeshadd, pattern=r"add_chat\(.+\)", run_async=True)
RM_CHAT_HANDLER = CallbackQueryHandler(mukeshrm, pattern=r"rm_chat\(.+\)", run_async=True)
CHATBOT_HANDLER = MessageHandler(
    Filters.text
    & (~Filters.regex(r"^#[^\s]+") & ~Filters.regex(r"^!") & ~Filters.regex(r"^\/")),
    chatbot,
    run_async=True,
)

dispatcher.add_handler(ADD_CHAT_HANDLER)
dispatcher.add_handler(CHATBOTK_HANDLER)
dispatcher.add_handler(RM_CHAT_HANDLER)
dispatcher.add_handler(CHATBOT_HANDLER)

__mod_name__ = "ᴄʜᴀᴛ-ʙᴏᴛ"
__help__ = """
 ❍ /chatbot ➛ ᴀɪ ᴄʜᴀᴛʙᴏᴛ [ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ]
 """

__handlers__ = [
    ADD_CHAT_HANDLER,
    CHATBOTK_HANDLER,
    RM_CHAT_HANDLER,
    CHATBOT_HANDLER,
]