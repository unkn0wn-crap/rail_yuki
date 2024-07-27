from gpytranslate import SyncTranslator
from telegram import ParseMode, Update
from telegram.ext import CallbackContext
from YukiBot import pbot as app
from YukiBot import dispatcher
from YukiBot.modules.disable import DisableAbleCommandHandler
from pyrogram.types import InputMediaVideo
import random
trans = SyncTranslator()


def totranslate(update: Update, context: CallbackContext) -> None:
    message = update.effective_message
    reply_msg = message.reply_to_message
    if not reply_msg:
        message.reply_text(
            "❍ ʀᴇᴘʟʏ ᴛᴏ ᴍᴇssᴀɢᴇs ᴏʀ ᴡʀɪᴛᴇ ᴍᴇssᴀɢᴇs ғʀᴏᴍ ᴏᴛʜᴇʀ ʟᴀɴɢᴜᴀɢᴇs ғᴏʀ ᴛʀᴀɴsʟᴀᴛɪɴɢ ɪɴᴛᴏ ᴛʜᴇ ɪɴᴛᴇɴᴅᴇᴅ ʟᴀɴɢᴜᴀɢᴇ\n\n"
            "❍ ᴇxᴀᴍᴘʟᴇ ➛ `/tr ᴇɴ-ʜɪ` ᴛᴏ ᴛʀᴀɴsʟᴀᴛᴇ ғʀᴏᴍ ᴇɴɢʟɪsʜ ᴛᴏ ʜɪɴᴅɪ\n"
            "❍ ᴜsᴇ ➛ `/tr en` ғᴏʀ ᴀᴜᴛᴏᴍᴀᴛɪᴄ ᴅᴇᴛᴇᴄᴛɪᴏɴ ᴀɴᴅ ᴛʀᴀɴsʟᴀᴛɪɴɢ ɪᴛ ɪɴᴛᴏ ᴇɴɢʟɪsʜ.",
            parse_mode="markdown",
            disable_web_page_preview=True,
        )
        return
    if reply_msg.caption:
        to_translate = reply_msg.caption
    elif reply_msg.text:
        to_translate = reply_msg.text
    try:
        args = message.text.split()[1].lower()
        if "//" in args:
            source = args.split("//")[0]
            dest = args.split("//")[1]
        else:
            source = trans.detect(to_translate)
            dest = args
    except IndexError:
        source = trans.detect(to_translate)
        dest = "en"
    translation = trans(to_translate, sourcelang=source, targetlang=dest)
    reply = (
        f"✦ <b>ᴛʀᴀɴsʟᴀᴛᴇᴅ ғʀᴏᴍ {source} ᴛᴏ {dest}</b> ✦\n\n"
        f"๏ <b>{translation.text}</b>"
    )

    message.reply_text(reply, parse_mode=ParseMode.HTML)


__help__ = """
 ❍ /tr  /tl (ʟᴀɴɢᴜᴀɢᴇ ᴄᴏᴅᴇ) ➛ ᴀs ʀᴇᴘʟʏ ᴛᴏ ᴀ ʟᴏɴɢ ᴍᴇssᴀɢᴇ

 ❍ /tr en* ➛* ᴛʀᴀɴsʟᴀᴛᴇs sᴏᴍᴇᴛʜɪɴɢ ᴛᴏ ᴇɴɢʟɪsʜ
 
 ❍ /tr hi-en* ➛* ᴛʀᴀɴsʟᴀᴛᴇs ʜɪɴᴅɪ ᴛᴏ ᴇɴɢʟɪsʜ

✿ *ʟᴀɴɢᴜᴀɢᴇ ᴄᴏᴅᴇs* ✿

❍ `af,am,ar,az,be,bg,bn,bs,ca,ceb,co,cs,cy,da,de,el,en,eo,es,
et,eu,fa,fi,fr,fy,ga,gd,gl,gu,ha,haw,hi,hmn,hr,ht,hu,hy,
id,ig,is,it,iw,ja,jw,ka,kk,km,kn,ko,ku,ky,la,lb,lo,lt,lv,mg,mi,mk,
ml,mn,mr,ms,mt,my,ne,nl,no,ny,pa,pl,ps,pt,ro,ru,sd,si,sk,sl,
sm,sn,so,sq,sr,st,su,sv,sw,ta,te,tg,th,tl,tr,uk,ur,uz,
vi,xh,yi,yo,zh,zh_CN,zh_TW,zu`
"""
__mod_name__ = "ᴛʀᴀɴs"

TRANSLATE_HANDLER = DisableAbleCommandHandler(["tr", "tl"], totranslate, run_async=True)

dispatcher.add_handler(TRANSLATE_HANDLER)

__command_list__ = ["tr", "tl"]
__handlers__ = [TRANSLATE_HANDLER]
from platform import python_version as y

from pyrogram import __version__ as z
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import __version__ as o
from telethon import __version__ as s

from YukiBot import OWNER_ID, dispatcher
from YukiBot import pbot as client

Mukesh = "https://graph.org/file/f97e3c200cd88a366bc21.jpg"

@client.on_message(filters.command(["bot_repo", "source"]))
async def repo(client, message):
    await message.reply_photo(
        photo=Mukesh,
        caption=f"""** {message.from_user.mention()}, Aʀᴀ Aʀᴀ\n\n ɪ ᴀᴍ [{dispatcher.bot.first_name}](t.me/{dispatcher.bot.username})** 🄿🄰🅁🄰🄳🄾🅇**
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "ᴏᴡɴᴇʀ",user_id=OWNER_ID
                    ),
                    InlineKeyboardButton(
                        "ʀᴇᴘᴏ",
                        callback_data="gib_source",
                    ),
                ]
            ]
        ),
    )


@app.on_callback_query(filters.regex("gib_source"))
async def gib_repo_callback(_, callback_query):
    await callback_query.edit_message_media(
        media=InputMediaVideo("https://graph.org/file/61ee71457fa11ff75e9a6.mp4", has_spoiler=True),
        reply_markup=InlineKeyboardMarkup(
            [
                [close_button]
            ]
        ),
        )
close_button = InlineKeyboardButton("ᴀʀᴀ ᴀʀᴀ ~", callback_data="help_back")
