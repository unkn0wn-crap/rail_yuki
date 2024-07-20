import time, re
from YukiBot import BOT_USERNAME
from pyrogram.enums import MessageEntityType
from pyrogram import filters
from pyrogram.types import Message
from YukiBot import pbot as app
from YukiBot.Love.readable_time import get_readable_time
from YukiBot.Love.afkdb import add_afk, is_afk, remove_afk
import random 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


POLICE = [

"https://graph.org/file/28337379488b8e6af5f54.jpg",
"https://graph.org/file/8c77f65576497f0e3f70d.jpg",
"https://graph.org/file/a1b46e87326e3cf5c868d.jpg",
"https://graph.org/file/606a34cd8f6f454d58378.jpg",
"https://graph.org/file/86390ff86341dbbe98f91.jpg",
"https://graph.org/file/2f68563873477a328ccc2.jpg",
"https://graph.org/file/dbf93aa1c20e4382e64db.jpg",
"https://graph.org/file/7d69d63e399131c050885.jpg",
"https://graph.org/file/602f47667830361f0eb64.jpg",
"https://graph.org/file/777f3ab8abefa835b1059.jpg",
"https://graph.org/file/9beced7d1a18d744cc18a.jpg",
"https://graph.org/file/1867b0db4fcfa20284a6b.jpg",

    "https://graph.org/file/109a941700ce02944afc6.jpg",
    "https://graph.org/file/dd197a3fad2715816528a.jpg",
    "https://graph.org/file/273c4e8811f5249135ae7.jpg",
    "https://graph.org/file/84486beb0429c04806f6c.jpg",
    "https://graph.org/file/609b50e4a4aa03c708247.jpg",
    "https://graph.org/file/6b0a1052c7b64b403a22c.jpg",
    "https://graph.org/file/7ee808520d792c083cdeb.jpg",
    "https://graph.org/file/4db798283a5c3db91c6f6.jpg",
    "https://graph.org/file/bcee30973b23ebd52afcb.jpg",
    "https://graph.org/file/2c402620225d9e117ec54.jpg",
    "https://graph.org/file/7e5229934d9c7858554ab.jpg",
    "https://graph.org/file/adbbf7189416318f40678.jpg",
    "https://graph.org/file/462224ce506163b529e99.jpg",
    "https://graph.org/file/b086290a5c467914d26f6.jpg",
    "https://graph.org/file/df23aa7226f168f2a3a17.jpg",
    "https://graph.org/file/f2ee0e5aa200d8b49a4d1.jpg",
    "https://graph.org/file/d59b342693f4f967de270.jpg",
    "https://graph.org/file/0d10617aa97ece8b7c636.jpg",
    "https://graph.org/file/c37b606a7e940779b7d02.jpg",
    "https://graph.org/file/03a6541f04ad09c048d61.jpg",
    "https://graph.org/file/30696cb28b54f5193e6c4.jpg",
    "https://graph.org/file/d0dd3367dc8cc6db8bd14.jpg",
    "https://graph.org/file/f6effebdf17d142ed52af.jpg",
    "https://graph.org/file/734d7f06f06d892c609fe.jpg",
    "https://graph.org/file/2d6127fef949f898a47ae.jpg",

"https://graph.org/file/7f861f26f80097d869086.jpg",

"https://graph.org/file/07a99f24e310f972c66d6.jpg"
]

@app.on_message(filters.command(["afk"], prefixes=["/", "!"]))
async def active_afk(_, message: Message):
    if message.sender_chat:
        return
    user_id = message.from_user.id
    verifier, reasondb = await is_afk(user_id)
    if verifier:
        await remove_afk(user_id)
        try:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            data = reasondb["data"]
            reasonafk = reasondb["reason"]
            seenago = get_readable_time((int(time.time() - timeafk)))
            if afktype == "text":
                send = await message.reply_text(
                    f"**༗ {message.from_user.first_name}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}",
                    disable_web_page_preview=True,
                )
            if afktype == "text_reason":
                send = await message.reply_text(
                    f"**༗ {message.from_user.first_name}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\n● ʀᴇᴀsᴏɴ ➾ `{reasonafk}`",
                    disable_web_page_preview=True,
                )
            if afktype == "animation":
                if str(reasonafk) == "None":
                    send = await message.reply_animation(
                        data,
                        caption=f"**༗ {message.from_user.first_name}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}",
                    )
                else:
                    send = await message.reply_animation(
                        data,
                        caption=f"**༗ {message.from_user.first_name}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\n● ʀᴇᴀsᴏɴ ➾ `{reasonafk}`",
                    )
            if afktype == "photo":
                if str(reasonafk) == "None":
                    send = await message.reply_photo(
                        photo=f"downloads/{user_id}.jpg",
                        caption=f"**༗ {message.from_user.first_name}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}",
                    )
                else:
                    send = await message.reply_photo(
                        photo=f"downloads/{user_id}.jpg",
                        caption=f"**༗ {message.from_user.first_name}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\n● ʀᴇᴀsᴏɴ ➾ `{reasonafk}`",
                    )
        except Exception:
            send = await message.reply_text(
                f"**༗ {message.from_user.first_name}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ",
                disable_web_page_preview=True,
            )

    if len(message.command) == 1 and not message.reply_to_message:
        details = {
            "type": "text",
            "time": time.time(),
            "data": None,
            "reason": None,
        }
    elif len(message.command) > 1 and not message.reply_to_message:
        _reason = (message.text.split(None, 1)[1].strip())[:100]
        details = {
            "type": "text_reason",
            "time": time.time(),
            "data": None,
            "reason": _reason,
        }
    elif len(message.command) == 1 and message.reply_to_message.animation:
        _data = message.reply_to_message.animation.file_id
        details = {
            "type": "animation",
            "time": time.time(),
            "data": _data,
            "reason": None,
        }
    elif len(message.command) > 1 and message.reply_to_message.animation:
        _data = message.reply_to_message.animation.file_id
        _reason = (message.text.split(None, 1)[1].strip())[:100]
        details = {
            "type": "animation",
            "time": time.time(),
            "data": _data,
            "reason": _reason,
        }
    elif len(message.command) == 1 and message.reply_to_message.photo:
        await app.download_media(
            message.reply_to_message, file_name=f"{user_id}.jpg"
        )
        details = {
            "type": "photo",
            "time": time.time(),
            "data": None,
            "reason": None,
        }
    elif len(message.command) > 1 and message.reply_to_message.photo:
        await app.download_media(
            message.reply_to_message, file_name=f"{user_id}.jpg"
        )
        _reason = message.text.split(None, 1)[1].strip()
        details = {
            "type": "photo",
            "time": time.time(),
            "data": None,
            "reason": _reason,
        }
    elif len(message.command) == 1 and message.reply_to_message.sticker:
        if message.reply_to_message.sticker.is_animated:
            details = {
                "type": "text",
                "time": time.time(),
                "data": None,
                "reason": None,
            }
        else:
            await app.download_media(
                message.reply_to_message, file_name=f"{user_id}.jpg"
            )
            details = {
                "type": "photo",
                "time": time.time(),
                "data": None,
                "reason": None,
            }
    elif len(message.command) > 1 and message.reply_to_message.sticker:
        _reason = (message.text.split(None, 1)[1].strip())[:100]
        if message.reply_to_message.sticker.is_animated:
            details = {
                "type": "text_reason",
                "time": time.time(),
                "data": None,
                "reason": _reason,
            }
        else:
            await app.download_media(
                message.reply_to_message, file_name=f"{user_id}.jpg"
            )
            details = {
                "type": "photo",
                "time": time.time(),
                "data": None,
                "reason": _reason,
            }
    else:
        details = {
            "type": "text",
            "time": time.time(),
            "data": None,
            "reason": None,
        }

    await add_afk(user_id, details)    
    await message.reply_photo(
        photo=random.choice(POLICE),
        caption=f"༗ {message.from_user.first_name} ɪs ɴᴏᴡ ᴀғᴋ !"
    )




chat_watcher_group = 1


@app.on_message(
    ~filters.me & ~filters.bot & ~filters.via_bot,
    group=chat_watcher_group,
)
async def chat_watcher_func(_, message):
    if message.sender_chat:
        return
    userid = message.from_user.id
    user_name = message.from_user.first_name
    if message.entities:
        possible = ["/afk", f"/afk@{BOT_USERNAME}"]
        message_text = message.text or message.caption
        for entity in message.entities:
            if entity.type == MessageEntityType.BOT_COMMAND:
                if (message_text[0 : 0 + entity.length]).lower() in possible:
                    return

    msg = ""
    replied_user_id = 0


    
    verifier, reasondb = await is_afk(userid)
    if verifier:
        await remove_afk(userid)
        try:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            data = reasondb["data"]
            reasonafk = reasondb["reason"]
            seenago = get_readable_time((int(time.time() - timeafk)))
            if afktype == "text":
                msg += f"**༗ {user_name[:25]}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\n"
            if afktype == "text_reason":
                msg += f"**༗ {user_name[:25]}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\n● ʀᴇᴀsᴏɴ ➾ `{reasonafk}`\n\n"
            if afktype == "animation":
                if str(reasonafk) == "None":
                    send = await message.reply_animation(
                        data,
                        caption=f"**༗ {user_name[:25]}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\n"
                    )
                else:
                    send = await message.reply_animation(
                        data,
                        caption=f"**༗ {user_name[:25]}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\n● ʀᴇᴀsᴏɴ ➾ `{reasonafk}`\n\n", 
                      
                     )
            if afktype == "photo":
                if str(reasonafk) == "None":
                    send = await message.reply_photo(
                        photo=f"downloads/{userid}.jpg",
                        caption=f"**༗ {user_name[:25]}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\n"
                    )
                else:
                    send = await message.reply_photo(
                        photo=f"downloads/{userid}.jpg",
                        caption=f"**༗ {user_name[:25]}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴡᴀs ᴀᴡᴀʏ ғᴏʀ {seenago}\n\n● ʀᴇᴀsᴏɴ ➾ `{reasonafk}`\n\n",
                    )
        except:
            msg += f"**༗ {user_name[:25]}** ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ\n\n"


    if message.reply_to_message:
        try:
            replied_first_name = message.reply_to_message.from_user.first_name
            replied_user_id = message.reply_to_message.from_user.id
            verifier, reasondb = await is_afk(replied_user_id)
            if verifier:
                try:
                    afktype = reasondb["type"]
                    timeafk = reasondb["time"]
                    data = reasondb["data"]
                    reasonafk = reasondb["reason"]
                    seenago = get_readable_time((int(time.time() - timeafk)))
                    if afktype == "text":
                        msg += (
                            f"**༗ {replied_first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n"
                        )
                    if afktype == "text_reason":
                        msg += f"**༗ {replied_first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n● ʀᴇᴀsᴏɴ ➾ `{reasonafk}`\n\n"
                    if afktype == "animation":
                        if str(reasonafk) == "None":
                            send = await message.reply_animation(
                                data,
                                caption=f"**༗ {replied_first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n"  
                            )
                        else:
                            send = await message.reply_animation(
                                data,
                                caption=f"**༗ {replied_first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n● ʀᴇᴀsᴏɴ ➾ `{reasonafk}`\n\n"  
                            )
                    if afktype == "photo":
                        if str(reasonafk) == "None":
                            send = await message.reply_photo(
                                photo=f"downloads/{replied_user_id}.jpg",
                                caption=f"**༗ {replied_first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n" 
                            )
                        else:
                            send = await message.reply_photo(
                                photo=f"downloads/{replied_user_id}.jpg",
                                caption=f"**༗ {replied_first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n● ʀᴇᴀsᴏɴ ➾ `{reasonafk}`\n\n"  
                            )
                except Exception:
                    msg += f"**༗ {replied_first_name}** ɪs ᴀғk"
        except:
            pass

    if message.entities:
        entity = message.entities
        j = 0
        for x in range(len(entity)):
            if (entity[j].type) == MessageEntityType.MENTION:
                found = re.findall("@([_0-9a-zA-Z]+)", message.text)
                try:
                    get_user = found[j]
                    user = await app.get_users(get_user)
                    if user.id == replied_user_id:
                        j += 1
                        continue
                except:
                    j += 1
                    continue
                verifier, reasondb = await is_afk(user.id)
                if verifier:
                    try:
                        afktype = reasondb["type"]
                        timeafk = reasondb["time"]
                        data = reasondb["data"]
                        reasonafk = reasondb["reason"]
                        seenago = get_readable_time((int(time.time() - timeafk)))
                        if afktype == "text":
                            msg += (
                                f"**༗ {user.first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n"
                            )
                        if afktype == "text_reason":
                            msg += f"**༗ {user.first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n● ʀᴇᴀsᴏɴ ➾ `{reasonafk}`\n\n"
                        if afktype == "animation":
                            if str(reasonafk) == "None":
                                send = await message.reply_animation(
                                    data,
                                    caption=f"**༗ {user.first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n",  
                                )
                            else:
                                send = await message.reply_animation(
                                    data,
                                    caption=f"**༗ {user.first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n● ʀᴇᴀsᴏɴ ➾ `{reasonafk}`\n\n",  
                                )
                        if afktype == "photo":
                            if str(reasonafk) == "None":
                                send = await message.reply_photo(
                                    photo=f"downloads/{user.id}.jpg",
                                    caption=f"**༗ {user.first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n",  
                                )
                            else:
                                send = await message.reply_photo(
                                    photo=f"downloads/{user.id}.jpg",
                                    caption=f"**༗ {user.first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n● ʀᴇᴀsᴏɴ ➾ `{reasonafk}`\n\n",  
                                )
                    except:
                        msg += f"**༗ {user.first_name[:25]}** ɪs ᴀғᴋ\n\n"
            elif (entity[j].type) == MessageEntityType.TEXT_MENTION:
                try:
                    user_id = entity[j].user.id
                    if user_id == replied_user_id:
                        j += 1
                        continue
                    first_name = entity[j].user.first_name
                except:
                    j += 1
                    continue
                verifier, reasondb = await is_afk(user_id)
                if verifier:
                    try:
                        afktype = reasondb["type"]
                        timeafk = reasondb["time"]
                        data = reasondb["data"]
                        reasonafk = reasondb["reason"]
                        seenago = get_readable_time((int(time.time() - timeafk)))
                        if afktype == "text":
                            msg += f"**༗ {first_name[:25]}** is ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n"
                        if afktype == "text_reason":
                            msg += f"**༗ {first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n● ʀᴇᴀsᴏɴ ➾ `{reasonafk}`\n\n"
                        if afktype == "animation":
                            if str(reasonafk) == "None":
                                send = await message.reply_animation(
                                    data,
                                    caption=f"**༗ {first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n",  
                                )
                            else:
                                send = await message.reply_animation(
                                    data,
                                    caption=f"**༗ {first_name[:25]}** ɪs AFK sɪɴᴄᴇ {seenago}\n\n● ʀᴇᴀsᴏɴ ➾ `{reasonafk}`\n\n",  
                                )
                        if afktype == "photo":
                            if str(reasonafk) == "None":
                                send = await message.reply_photo(
                                    photo=f"downloads/{user_id}.jpg",
                                    caption=f"**༗ {first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n",  
                                )
                            else:
                                send = await message.reply_photo(
                                    photo=f"downloads/{user_id}.jpg",
                                    caption=f"**༗ {first_name[:25]}** ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n\n● ʀᴇᴀsᴏɴ ➾ `{reasonafk}`\n\n",  
                                )
                    except:
                        msg += f"**༗ {first_name[:25]}** ɪs ᴀғᴋ\n\n"
            j += 1
    if msg != "":
        try:
            send = await message.reply_text(msg, disable_web_page_preview=True)
        except:
            return

__mod_name__ = "ᴀғᴋ"

__help__ = """

⬤ /afk <reason> *➾* ᴍᴀʀᴋ ʏᴏᴜʀsᴇʟғ ᴀs ᴀғᴋ.
⬤ brb, !afk <reason> *➾* sᴀᴍᴇ ᴀs ᴛʜᴇ ᴀғᴋ ᴄᴏᴍᴍᴀɴᴅ.
"""

