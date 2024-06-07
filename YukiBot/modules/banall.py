import os
from time to sleep

from telethon import *
from telethon.errors import *
from telethon.errors import FloodWaitError, UserNotParticipantError
from telethon.tl import *
from telethon.tl import functions, types
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import *
from telethon.tl.types import (
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
    ChatBannedRights,
)

from YukiBot import *
from YukiBot import LOGGER
from YukiBot.events import register

BOT_ID = 7134066784
OWNER_ID = 6259443940
CMD_HELP = "/ !"

# ================================================

async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):
        return isinstance(
            (
                await telethn(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerUser):
        return True

@register(pattern="^/banall$")
async def _(event):
    if event.sender_id != OWNER_ID:
        return await event.respond("⌥ ᴏɴʟʏ ᴛʜᴇ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.")

    chat = await event.get_chat()
    admin = chat.admin_rights.ban_users
    creator = chat.creator
    if event.is_private:
        return await event.respond(
            "⌥ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs ᴀɴᴅ ᴄʜᴀɴɴᴇʟs."
        )

    is_admin = False
    try:
        YukiBot = await telethn(GetParticipantRequest(event.chat_id, event.sender_id))
    except UserNotParticipantError:
        is_admin = False
    else:
        if isinstance(
            YukiBot.participant,
            (
                ChannelParticipantAdmin,
                ChannelParticipantCreator,
            ),
        ):
            is_admin = True
    if not is_admin:
        return await event.respond("⌥ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ʙᴀɴᴀʟʟ")

    if not admin and not creator:
        await event.reply("⌥ `ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ᴘᴇʀᴍɪssɪᴏɴs!`")
        return

    done = await event.reply("⌥ sᴇᴀʀᴄʜɪɴɢ ᴘᴀʀᴛɪᴄɪᴘᴀɴᴛ ʟɪsᴛs...")
    p = 0
    async for i in telethn.iter_participants(event.chat_id, aggressive=True):
        rights = ChatBannedRights(until_date=None, view_messages=True)
        try:
            await telethn(functions.channels.EditBannedRequest(event.chat_id, i, rights))
        except FloodWaitError as ex:
            LOGGER.warn(f"⌥ sʟᴇᴇᴘɪɴɢ ғᴏʀ {ex.seconds} sᴇᴄᴏɴᴅs")
            sleep(ex.seconds)
        except Exception as ex:
            await event.reply(str(ex))
        else:
            p += 1

    if p == 0:
        await done.edit("⌥ ɴᴏ ᴜsᴇʀs ғᴏᴜɴᴅ ᴛᴏ ʙᴀɴ ɪɴ ᴛʜɪs ᴄʜᴀᴛ")
        return
    required_string = "⌥ sᴜᴄᴇssғᴜʟʟʏ ʙᴀɴɴᴇᴅ **{}** ᴜsᴇʀs"
    await event.reply(required_string.format(p))

@register(pattern="^/muteall$")
async def _(event):
    if event.sender_id != OWNER_ID:
        return await event.respond("⌥ ᴏɴʟʏ ᴛʜᴇ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.")

    chat = await event.get_chat()
    admin = chat.admin_rights.ban_users
    creator = chat.creator
    if event.is_private:
        return await event.respond(
            "⌥ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs ᴀɴᴅ ᴄʜᴀɴɴᴇʟs."
        )

    is_admin = False
    try:
        YukiBot = await telethn(GetParticipantRequest(event.chat_id, event.sender_id))
    except UserNotParticipantError:
        is_admin = False
    else:
        if isinstance(
            YukiBot.participant,
            (
                ChannelParticipantAdmin,
                ChannelParticipantCreator,
            ),
        ):
            is_admin = True
    if not is_admin:
        return await event.respond("⌥ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴍᴜᴛᴇᴀʟʟ")

    if not admin and not creator:
        await event.reply("⌥ `ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ᴘᴇʀᴍɪssɪᴏɴs!`")
        return

    done = await event.reply("⌥ ᴡᴏʀᴋɪɴɢ ...")
    p = 0
    async for i in telethn.iter_participants(event.chat_id, aggressive=True):
        rights = ChatBannedRights(
            until_date=None,
            send_messages=True,
        )
        try:
            await telethn(
                functions.channels.EditBannedRequest(event.chat_id, i, rights)
            )
        except FloodWaitError as ex:
            LOGGER.warn(f"⌥ sʟᴇᴇᴘɪɴɢ ғᴏʀ {ex.seconds} sᴇᴄᴏɴᴅs")
            sleep(ex.seconds)
        except Exception as ex:
            await event.reply(str(ex))
        else:
            p += 1

    if p == 0:
        await done.edit("⌥ ɴᴏ ᴜsᴇʀs ғᴏᴜɴᴅ ᴛᴏ ᴍᴜᴛᴇ ɪɴ ᴛʜɪs ᴄʜᴀᴛ")
        return
    required_string = "⌥ sᴜᴄᴇssғᴜʟʟʏ ᴍᴜᴛᴇᴅ **{}** ᴜsᴇʀs"
    await event.reply(required_string.format(p))

@register(pattern="^/users$")
async def get_users(show):
    if not show.is_group:
        return
    if not await is_register_admin(show.input_chat, show.sender_id):
        return
    info = await telethn.get_entity(show.chat_id)
    title = info.title or "ᴛʜɪs ᴄʜᴀᴛ"
    mentions = f"⌥ ᴜsᴇʀs ɪɴ {title} \n"
    async for user in telethn.iter_participants(show.chat_id):
        mentions += (
            f"\nᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs  {user.id}"
            if user.deleted
            else f"\n⌥ [{user.first_name}](tg://user?id={user.id}) ✦ {user.id}"
        )

    with open("userslist.txt", "w+") as file:
        file.write(mentions)
    await telethn.send_file(
        show.chat_id,
        "userslist.txt",
        caption=f"⌥ ᴜsᴇʀs ɪɴ {title}",
        reply_to=show.id,
    )

    os.remove("userslist.txt")