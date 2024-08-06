import html
import os
import re

import requests
from telegram import (
    MAX_MESSAGE_LENGTH,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    Update,
)
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler
from telegram.utils.helpers import escape_markdown, mention_html
from telethon import events
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import ChannelParticipantsAdmins
# from YukiBot.modules.alive import Yuki
import YukiBot.modules.sql.userinfo_sql as sql
from YukiBot import (
    DEMONS,
    DEV_USERS,
    DRAGONS,
    INFOPIC,
    OWNER_ID,
    TIGERS,
    WOLVES,
    dispatcher,
    telethn,
    BOT_NAME,
    BOT_USERNAME
)

from YukiBot.__main__ import STATS, TOKEN, USER_INFO
from YukiBot.modules.disable import DisableAbleCommandHandler
from YukiBot.modules.helper_funcs.chat_status import sudo_plus
from YukiBot.modules.helper_funcs.extraction import extract_user
from YukiBot.modules.sql.global_bans_sql import is_user_gbanned
from YukiBot.modules.sql.users_sql import get_user_num_chats

ALLOWED_USERS = set(DEMONS) | set(DEV_USERS) | set(DRAGONS) | set(INFOPIC) | {OWNER_ID} | set(TIGERS) | set(WOLVES)

def no_by_per(totalhp, percentage):
    """
    rtype: num of `percentage` from total
    eg: 1000, 10 -> 10% of 1000 (100)
    """
    return totalhp * percentage / 100


def get_percentage(totalhp, earnedhp):
    """
    rtype: percentage of `totalhp` num
    eg: (1000, 100) will return 10%
    """

    matched_less = totalhp - earnedhp
    per_of_totalhp = 100 - matched_less * 100.0 / totalhp
    per_of_totalhp = str(int(per_of_totalhp))
    return per_of_totalhp


def hpmanager(user):
    total_hp = (get_user_num_chats(user.id) + 10) * 10

    if not is_user_gbanned(user.id):

        # Assign new var `new_hp` since we need `total_hp` in
        # end to calculate percentage.
        new_hp = total_hp

        # if no username decrease 25% of hp.
        if not user.username:
            new_hp -= no_by_per(total_hp, 25)
        try:
            dispatcher.bot.get_user_profile_photos(user.id).photos[0][-1]
        except IndexError:
            # no profile photo ==> -25% of hp
            new_hp -= no_by_per(total_hp, 25)
        # if no /setme exist ==> -20% of hp
        if not sql.get_user_me_info(user.id):
            new_hp -= no_by_per(total_hp, 20)
        # if no bio exsit ==> -10% of hp
        if not sql.get_user_bio(user.id):
            new_hp -= no_by_per(total_hp, 10)


        # fbanned users will have (2*number of fbans) less from max HP
        # Example: if HP is 100 but user has 5 diff fbans
        # Available HP is (2*5) = 10% less than Max HP
        # So.. 10% of 100HP = 90HP

    # Commenting out fban health decrease cause it wasnt working and isnt needed ig.
    # _, fbanlist = get_user_fbanlist(user.id)
    # new_hp -= no_by_per(total_hp, 2 * len(fbanlist))

    # Bad status effects:
    # gbanned users will always have 5% HP from max HP
    # Example: If HP is 100 but gbanned
    # Available HP is 5% of 100 = 5HP

    else:
        new_hp = no_by_per(total_hp, 5)

    return {
        "earnedhp": int(new_hp),
        "totalhp": int(total_hp),
        "percentage": get_percentage(total_hp, new_hp),
    }


def make_bar(per):
    done = min(round(per / 10), 10)
    return "■" * done + "□" * (10 - done)


def get_id(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    chat = update.effective_chat
    msg = update.effective_message
    user_id = extract_user(msg, args)

    if user_id:

        if msg.reply_to_message and msg.reply_to_message.forward_from:

            user1 = message.reply_to_message.from_user
            user2 = message.reply_to_message.forward_from

            msg.reply_text(
                f"⌬<b> ᴛᴇʟᴇɢʀᴀᴍ ɪᴅ </b>⌬\n\n"
                f"⌬ {html.escape(user2.first_name)} ➛ <code>{user2.id}</code>.\n"
                f"⌬ {html.escape(user1.first_name)} ➛ <code>{user1.id}</code>.",
                parse_mode=ParseMode.HTML,
            )

        else:

            user = bot.get_chat(user_id)
            msg.reply_text(
                f"⌬ {html.escape(user.first_name)}'s ɪᴅ ɪs <code>{user.id}</code>.",
                parse_mode=ParseMode.HTML,
            )

    else:

        if chat.type == "private":
            msg.reply_text(
                f"⌬ ʏᴏᴜʀ ᴜsᴇʀ ɪᴅ ɪs ➛ <code>{chat.id}</code>.", parse_mode=ParseMode.HTML
            )

        else:
            msg.reply_text(
                f"⌬ ᴛʜɪs ɢʀᴏᴜᴩ's ɪᴅ ɪs ➛ <code>{chat.id}</code>.", parse_mode=ParseMode.HTML
            )


@telethn.on(
    events.NewMessage(
        pattern="/ginfo",from_users=(TIGERS or []) + (DRAGONS or []) + (DEMONS or [])
    ),
)
async def group_info(event) -> None:
    chat = event.text.split(" ", 1)[1]
    try:
        entity = await event.client.get_entity(chat)
        totallist = await event.client.get_participants(
            entity, filter=ChannelParticipantsAdmins
        )
        ch_full = await event.client(GetFullChannelRequest(channel=entity))
    except:
        await event.reply(
            "⌬ ᴄᴀɴ'ᴛ ғᴏʀ sᴏᴍᴇ ʀᴇᴀsᴏɴ, ᴍᴀʏʙᴇ ɪᴛ ɪs ᴀ ᴘʀɪᴠᴀᴛᴇ ᴏɴᴇ ᴏʀ ᴛʜᴀᴛ ɪ ᴀᴍ ʙᴀɴɴᴇᴅ ᴛʜᴇʀᴇ."
        )
        return
    msg = f"**⌬ ɪᴅ** ➛ `{entity.id}`"
    msg += f"\n**⌬ ᴛɪᴛʟᴇ** ➛ `{entity.title}`"
    msg += f"\n**⌬ ᴅᴄ** ➛ `{entity.photo.dc_id}`"
    msg += f"\n**⌬ ᴠɪᴅᴇᴏ ᴩғᴩ** ➛ `{entity.photo.has_video}`"
    msg += f"\n**⌬ sᴜᴩᴇʀɢʀᴏᴜᴩ** ➛ `{entity.megagroup}`"
    msg += f"\n**⌬ ʀᴇsᴛʀɪᴄᴛᴇᴅ** ➛ `{entity.restricted}`"
    msg += f"\n**⌬ sᴄᴀᴍ** ➛ `{entity.scam}`"
    msg += f"\n**⌬ sʟᴏᴡᴍᴏᴅᴇ** ➛`{entity.slowmode_enabled}`"
    if entity.username:
        msg += f"\n**⌬ ᴜsᴇʀɴᴀᴍᴇ**➛ @{entity.username}"
    msg += "\n\n**Ⰶ ᴍᴇᴍʙᴇʀ sᴛᴀᴛs Ⰶ**"
    msg += f"\n⌬ ᴀᴅᴍɪɴs ➛ `{len(totallist)}`"
    msg += f"\n⌬ ᴜsᴇʀs ➛`{totallist.total}`"
    msg += "\n\n**⌬ ᴀᴅᴍɪɴs ʟɪsᴛ ⌬**"
    for x in totallist:
        msg += f"\n⌬ [{x.id}](tg://user?id={x.id})"
    msg += f"\n\n**⌬ ᴅᴇsᴄʀɪᴩᴛɪᴏɴ** ➛\n`{ch_full.full_chat.about}`"
    await event.reply(msg)


def gifid(update: Update, context: CallbackContext):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.animation:
        update.effective_message.reply_text(
            f"⌬ ɢɪғ ɪᴅ ➛\n<code>{msg.reply_to_message.animation.file_id}</code>",
            parse_mode=ParseMode.HTML,
        )
    else:
        update.effective_message.reply_text("⌬ ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ɢɪғ ᴛᴏ ɢᴇᴛ ɪᴛs ɪᴅ.")


def info(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    chat = update.effective_chat
    user_id = extract_user(update.effective_message, args)

    if user_id:
        user = bot.get_chat(user_id)

    elif not message.reply_to_message and not args:
        user = message.from_user

    elif not message.reply_to_message and (
        not args
        or (
            len(args) >= 1
            and not args[0].startswith("@")
            and not args[0].isdigit()
            and not message.parse_entities([MessageEntity.TEXT_MENTION])
        )
    ):
        message.reply_text("⌬ ɪ ᴄᴀɴ'ᴛ ᴇxᴛʀᴀᴄᴛ ᴀ ᴜsᴇʀ ғʀᴏᴍ ᴛʜɪs")
        return

    else:
        return

    rep = message.reply_text("⌬ <code>ᴇxᴛʀᴀᴄᴛɪɴɢ ɪɴғᴏʀᴍᴀᴛɪᴏɴ...\n</code>", parse_mode=ParseMode.HTML)

    text = (
        f" ⌬ ᴜsᴇʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ⌬\n•─────────[×]─────────•\n\n"
        f"⌥ <b>ᴜsᴇʀ ɪᴅ ➛</b> <code>{user.id}</code>\n"
        f"⌥ <b>ғɪʀsᴛ ɴᴀᴍᴇ ➛</b> {html.escape(user.first_name)}"
    )

    if user.last_name:
        text += f"\n⌥ <b>ʟᴀsᴛ ɴᴀᴍᴇ ➛</b> {html.escape(user.last_name)}"

    if user.username:
        text += f"\n⌥ <b>ᴜsᴇʀɴᴀᴍᴇ ➛</b> @{html.escape(user.username)}"

    text += f"\n⌥ <b>ʟɪɴᴋ ➛</b> {mention_html(user.id, 'link')}"

    if chat.type != "private" and user_id != bot.id:
        _stext = "\n⌥ <b>ᴩʀᴇsᴇɴᴄᴇ ➛</b> <code>{}</code>"

        status = status = bot.get_chat_member(chat.id, user.id).status
        if status:
            if status in {"left", "kicked"}:
                text += _stext.format("ɴᴏᴛ ʜᴇʀᴇ")
            elif status == "member":
                text += _stext.format("ᴅᴇᴛᴇᴄᴛᴇᴅ")
            elif status in {"administrator", "creator"}:
                text += _stext.format("ᴀᴅᴍɪɴ")
    if user_id not in [bot.id, 777000, 1087968824]:
        userhp = hpmanager(user)
        text += f"\n\n⌥ <b>ʜᴇᴀʟᴛʜ ➛</b> <code>{userhp['earnedhp']}/{userhp['totalhp']}</code>\n[<i>{make_bar(int(userhp['percentage']))} </i>{userhp['percentage']}%]"

    disaster_level_present = False

    if user.id == OWNER_ID:
        text += "\n\n⌥ ᴛʜᴇ ᴅɪsᴀsᴛᴇʀ ʟᴇᴠᴇʟ ᴏғ ᴛʜɪs ᴜsᴇʀ ɪs <b>ɢᴏᴅ</b>.\n"
        disaster_level_present = True
    elif user.id in DEV_USERS:
        text += "\n\n⌥ ᴛʜɪs ᴜsᴇʀ ɪs ᴀ ᴍᴇᴍʙᴇʀ ᴏғ <b>🄿🄰🅁🄰🄳🄾🅇</b>.\n"
        disaster_level_present = True
    elif user.id in DRAGONS:
        text += "\n\n⌥ ᴛʜᴇ ᴅɪsᴀsᴛᴇʀ ʟᴇᴠᴇʟ ᴏғ ᴛʜɪs ᴜsᴇʀ ɪs <b>ᴅʀᴀɢᴏɴ</b>.\n"
        disaster_level_present = True
    elif user.id in DEMONS:
        text += "\n\n⌥ ᴛʜᴇ ᴅɪsᴀsᴛᴇʀ ʟᴇᴠᴇʟ ᴏғ ᴛʜɪs ᴜsᴇʀ ɪs <b>ᴅᴇᴍᴏɴ</b>.\n"
        disaster_level_present = True
    elif user.id in TIGERS:
        text += "\n\n⌥ ᴛʜᴇ ᴅɪsᴀsᴛᴇʀ ʟᴇᴠᴇʟ ᴏғ ᴛʜɪs ᴜsᴇʀ ɪs <b>ᴛɪɢᴇʀ</b>.\n"
        disaster_level_present = True
    elif user.id in WOLVES:
        text += "\n\n⌥ ᴛʜᴇ ᴅɪsᴀsᴛᴇʀ ʟᴇᴠᴇʟ ᴏғ ᴛʜɪs ᴜsᴇʀ ɪs <b>ᴡᴏʟғ</b>.\n"
        disaster_level_present = True

    if disaster_level_present:
        text += ' \n⌥ 🄿🄰🅁🄰🄳🄾🅇'.format(
            bot.username
        )

    try:
        user_member = chat.get_member(user.id)
        if user_member.status == "administrator":
            result = requests.post(
                f"https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={chat.id}&user_id={user.id}"
            )
            result = result.json()["result"]
            if "custom_title" in result.keys():
                custom_title = result["custom_title"]
                text += f"\n\n⌥ ᴛɪᴛʟᴇ ➛\n<b>{custom_title}</b>"
    except BadRequest:
        pass

    for mod in USER_INFO:
        try:
            mod_info = mod.__user_info__(user.id).strip()
        except TypeError:
            mod_info = mod.__user_info__(user.id, chat.id).strip()
        if mod_info:
            text += "\n\n" + mod_info

    if INFOPIC:
        try:
            profile = context.bot.get_user_profile_photos(user.id).photos[0][-1]
            _file = bot.get_file(profile["file_id"])
            _file.download(f"{user.id}.png")

            message.reply_photo(
                photo=open(f"{user.id}.png", "rb"),
                caption=(text),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="ᴀᴅᴅ ᴍᴇ ʜᴜᴍᴀɴ",
                                url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                            ),
                        ],
                    ]
                ),
                parse_mode=ParseMode.HTML,
            )

            os.remove(f"{user.id}.png")
        # Incase user don't have profile pic, send normal text
        except IndexError:
            message.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="ᴀᴅᴅ ᴍᴇ ʜᴜᴍᴀɴ",
                                url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                            ),
                        ],
                    ]
                ),
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
    else:
        message.reply_text(
            text,
            parse_mode=ParseMode.HTML,
        )

    rep.delete()


def about_me(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    user_id = extract_user(message, args)

    if user_id:
        user = bot.get_chat(user_id)
    else:
        user = message.from_user

    info = sql.get_user_me_info(user.id)

    if info:
        update.effective_message.reply_text(
            f"⌥ *{user.first_name}*\n{escape_markdown(info)}",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    elif message.reply_to_message:
        username = message.reply_to_message.from_user.first_name
        update.effective_message.reply_text(
            f"⌥ {username} ʜᴀsɴ'ᴛ sᴇᴛ ᴀɴ ɪɴғᴏ ᴍᴇssᴀɢᴇ ᴀʙᴏᴜᴛ ᴛʜᴇᴍsᴇʟᴠᴇs ʏᴇᴛ!"
        )
    else:
        update.effective_message.reply_text("⌬ ᴛʜᴇʀᴇ ɪsɴ'ᴛ ᴏɴᴇ ᴜsᴇ /setme ᴛᴏ sᴇᴛ ᴏɴᴇ.")


def set_about_me(update: Update, context: CallbackContext):
    message = update.effective_message
    user_id = message.from_user.id
    if user_id in [777000, 1087968824]:
        message.reply_text("⌬ ᴇʀʀᴏʀ ᴜɴᴀᴜᴛʜᴏʀɪsᴇᴅ")
        return
    bot = context.bot
    if message.reply_to_message:
        repl_message = message.reply_to_message
        repl_user_id = repl_message.from_user.id
        if repl_user_id in [bot.id, 777000, 1087968824] and (user_id in DEV_USERS):
            user_id = repl_user_id
    text = message.text
    info = text.split(None, 1)
    if len(info) == 2:
        if len(info[1]) < MAX_MESSAGE_LENGTH // 4:
            sql.set_user_me_info(user_id, info[1])
            if user_id in [777000, 1087968824]:
                message.reply_text("⌬ ᴀᴜᴛʜᴏʀɪsᴇᴅ  .. ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴜᴘᴅᴀᴛᴇᴅ!")
            elif user_id == bot.id:
                message.reply_text("⌬ ɪ ʜᴀᴠᴇ ᴜᴘᴅᴀᴛᴇᴅ ᴍʏ ɪɴғᴏ ᴡɪᴛʜ ᴏɴᴇ ʏᴏᴜ ᴘʀᴏᴠɪᴅᴇᴅ!")
            else:
                message.reply_text("⌬ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴜᴘᴅᴀᴛᴇᴅ!")
        else:
            message.reply_text(
                "⌬ ᴛʜᴇ ɪɴғᴏ ɴᴇᴇᴅs ᴛᴏ ʙᴇ ᴜɴᴅᴇʀ {} ᴄʜᴀʀᴀᴄᴛᴇʀs! ʏᴏᴜ ʜᴀᴠᴇ {}.".format(
                    MAX_MESSAGE_LENGTH // 4, len(info[1])
                )
            )

######## botSTATS
def restricted(func):
    def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in ALLOWED_USERS:
            update.effective_message.reply_text("You don't have permission to use this command. Now go sleep")
            return
        return func(update, context, *args, **kwargs)
    return wrapper

@restricted
def stats(update: Update, context: CallbackContext):
    stats = f"<b>sᴛᴀᴛs ᴏғ ʏᴜᴋɪ 妖</b>\n\n" + "\n".join(
        [mod.__stats__() for mod in STATS]
    )
    result = re.sub(r"(\d+)", r"<code>\1</code>", stats)
    update.effective_message.reply_text(result, parse_mode=ParseMode.HTML)


def about_bio(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message

    user_id = extract_user(message, args)
    if user_id:
        user = bot.get_chat(user_id)
    else:
        user = message.from_user

    info = sql.get_user_bio(user.id)

    if info:
        update.effective_message.reply_text(
            "*{}*:\n{}".format(user.first_name, escape_markdown(info)),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    elif message.reply_to_message:
        username = user.first_name
        update.effective_message.reply_text(
            f"⌥ {username} ʜᴀsɴ'ᴛ ʜᴀᴅ ᴀ ᴍᴇssᴀɢᴇ sᴇᴛ  ᴀʙᴏᴜᴛ ᴛʜᴇᴍsᴇʟᴠᴇs ʏᴇᴛ!\n⌬ sᴇᴛ ᴏɴᴇ ᴜsɪɴɢ /setbio"
        )
    else:
        update.effective_message.reply_text(
            "ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ʜᴀᴅ ᴀ ʙɪᴏ sᴇᴛ ᴀʙᴏᴜᴛ ʏᴏᴜsᴇʟғ ʏᴇᴛ!"
        )


def set_about_bio(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    bot = context.bot

    if message.reply_to_message:
        repl_message = message.reply_to_message
        user_id = repl_message.from_user.id

        if user_id == message.from_user.id:
            message.reply_text(
                "ʜᴀ,ʏᴏᴜ ᴄᴀɴ'ᴛ sᴇᴛ ʏᴏᴜʀ ᴏᴡɴ ʙɪᴏ! ʏᴏᴜ'ʀᴇ ᴀᴛ ᴛʜᴇ  ᴍᴇʀᴄʏ ᴏғ ᴏᴛʜᴇʀs ʜᴇʀᴇ "
            )
            return

        if user_id in [777000, 1087968824] and sender_id not in DEV_USERS:
            message.reply_text("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪsᴇᴅ")
            return

        if user_id == bot.id and sender_id not in DEV_USERS:
            message.reply_text(
                "ᴜᴍᴍ... ʏᴇᴀʜ, ɪ ᴏɴʟʏ ᴛʀᴜsᴛ ɢʜᴏsᴛ ᴛᴏ sᴇᴛ ᴍʏ ʙɪᴏ."
            )
            return

        text = message.text
        bio = text.split(
            None, 1
        )  # use python's maxsplit to only remove the cmd, hence keeping newlines.

        if len(bio) == 2:
            if len(bio[1]) < MAX_MESSAGE_LENGTH // 4:
                sql.set_user_bio(user_id, bio[1])
                message.reply_text(
                    "⌥ ᴜᴘᴅᴀᴛᴇᴅ {}'s ʙɪᴏ!".format(repl_message.from_user.first_name)
                )
            else:
                message.reply_text(
                    "⌥ ʙɪᴏ ɴᴇᴇᴅs ᴛᴏ ʙᴇ ᴜɴᴅᴇʀ {} ᴄʜᴀʀᴀᴄᴛᴇʀs! ʏᴏᴜ ᴛʀɪᴇᴅ ᴛᴏ sᴇᴛ {}.".format(
                        MAX_MESSAGE_LENGTH // 4, len(bio[1])
                    )
                )
    else:
        message.reply_text("ʀᴇᴘʟʏ ᴛᴏ sᴏᴍᴇᴏɴᴇ ᴛᴏ sᴇᴛ ᴛʜᴇɪʀ ʙɪᴏ!")


def __user_info__(user_id):
    bio = html.escape(sql.get_user_bio(user_id) or "")
    me = html.escape(sql.get_user_me_info(user_id) or "")
    result = ""
    if me:
        result += f"<b>⌥ ᴀʙᴏᴜᴛ ᴜsᴇʀ ➛</b>\n⌥ {me}\n"
    if bio:
        result += f"<b>⌥ ᴏᴛʜᴇʀs sᴀʏ ᴛʜᴀᴛ ➛</b>\n⌥ {bio}\n"
    result = result.strip("\n")
    return result


__help__ = """
✿ *ɪᴅ * ✿
 ⌥ /id* ➛* ɢᴇᴛ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ɢʀᴏᴜᴘ ɪᴅ. ɪғ ᴜsᴇᴅ ʙʏ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ, ɢᴇᴛs ᴛʜᴀᴛ ᴜsᴇʀ's ɪᴅ.
 ⌥ /gifid *➛* ʀᴇᴘʟʏ ᴛᴏ ᴀ ɢɪғ ᴛᴏ ᴍᴇ ᴛᴏ ᴛᴇʟʟ ʏᴏᴜ ɪᴛs ғɪʟᴇ ɪᴅ.

✿ *sᴇʟғ ᴀᴅᴅᴇᴅ ɪɴғᴏʀᴍᴀᴛɪᴏɴ* ✿
 ⌥ /setme  <ᴛᴇxᴛ>* ➛* ᴡɪʟʟ sᴇᴛ ʏᴏᴜʀ ɪɴғᴏ
 ⌥ /me *➛* ᴡɪʟʟ ɢᴇᴛ ʏᴏᴜʀ ᴏʀ ᴀɴᴏᴛʜᴇʀ ᴜsᴇʀ's ɪɴғᴏ.
 
✿ *ᴇxᴀᴍᴘʟᴇs* ✿
 ⌥ /setme ➛ ɪ ᴀᴍ ᴀ ᴡᴏʟғ.
 ⌥ /me ➛ @username(ᴅᴇғᴀᴜʟᴛs ᴛᴏ ʏᴏᴜʀs ɪғ ɴᴏ ᴜsᴇʀ sᴘᴇᴄɪғɪᴇᴅ)

✿ *ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴏᴛʜᴇʀs ᴀᴅᴅ ᴏɴ ʏᴏᴜ* ✿
 ⌥ /bio *➛* ᴡɪʟʟ ɢᴇᴛ ʏᴏᴜʀ ᴏʀ ᴀɴᴏᴛʜᴇʀ ᴜsᴇʀ's ʙɪᴏ. ᴛʜɪs ᴄᴀɴɴᴏᴛ ʙᴇ sᴇᴛ ʙʏ ʏᴏᴜʀsᴇʟғ.
 ⌥ /setbio <ᴛᴇxᴛ>*:* ᴡʜɪʟᴇ ʀᴇᴘʟʏɪɴɢ, ᴡɪʟʟ sᴀᴠᴇ ᴀɴᴏᴛʜᴇʀ ᴜsᴇʀ's ʙɪᴏ 
 
✿ *ᴇxᴀᴍᴘʟᴇs* ✿
 ⌥ /bio ➛ @username(ᴅᴇғᴀᴜʟᴛs ᴛᴏ ʏᴏᴜʀs ɪғ ɴᴏᴛ sᴘᴇᴄɪғɪᴇᴅ).`
 ⌥ /setbio ➛ ᴛʜɪs ᴜsᴇʀ ɪs ᴀ ᴡᴏʟғ` (ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴇ ᴜsᴇʀ)

✿ *ᴏᴠᴇʀᴀʟʟ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ʏᴏᴜ* ✿
 ⌥ /info *➛* ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴀ ᴜsᴇʀ. 
 ⌥ /myinfo *➛* sʜᴏᴡs ɪɴғᴏ ᴀʙᴏᴜᴛ ᴛʜᴇ ᴜsᴇʀ ᴡʜᴏ sᴇɴᴛ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.
"""

SET_BIO_HANDLER = DisableAbleCommandHandler("setbio", set_about_bio, run_async=True)
GET_BIO_HANDLER = DisableAbleCommandHandler("bio", about_bio, run_async=True)

STATS_HANDLER = CommandHandler("stats", stats, run_async=True)
ID_HANDLER = DisableAbleCommandHandler("id", get_id, run_async=True)
GIFID_HANDLER = DisableAbleCommandHandler("gifid", gifid, run_async=True)
INFO_HANDLER = DisableAbleCommandHandler(("info", "book"), info, run_async=True)

SET_ABOUT_HANDLER = DisableAbleCommandHandler("setme", set_about_me, run_async=True)
GET_ABOUT_HANDLER = DisableAbleCommandHandler("me", about_me, run_async=True)

dispatcher.add_handler(STATS_HANDLER)
dispatcher.add_handler(ID_HANDLER)
dispatcher.add_handler(GIFID_HANDLER)
dispatcher.add_handler(INFO_HANDLER)
dispatcher.add_handler(SET_BIO_HANDLER)
dispatcher.add_handler(GET_BIO_HANDLER)
dispatcher.add_handler(SET_ABOUT_HANDLER)
dispatcher.add_handler(GET_ABOUT_HANDLER)

__mod_name__ = "ɪɴꜰᴏ"
__command_list__ = ["setbio", "bio", "setme", "me", "info"]
__handlers__ = [
    ID_HANDLER,
    GIFID_HANDLER,
    INFO_HANDLER,
    SET_BIO_HANDLER,
    GET_BIO_HANDLER,
    SET_ABOUT_HANDLER,
    GET_ABOUT_HANDLER,
    STATS_HANDLER,
]
