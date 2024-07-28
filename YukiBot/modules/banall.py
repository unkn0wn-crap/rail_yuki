import os
from time import sleep
from telethon import functions, types
from telethon.errors import FloodWaitError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import (
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
    ChatBannedRights,
    ChannelParticipantsSearch
)
from YukiBot import telethn, LOGGER
from YukiBot.events import register

OWNER_IDS = [6259443940, 5053815620, 6810396528]
is_banning = False

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

# Ban All
@register(pattern="^/banall$")
async def ban_all(event):
    global is_banning
    if event.sender_id not in OWNER_IDS:
        return await event.respond("⌥ ᴏɴʟʏ ᴛʜᴇ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.")

    chat = await event.get_chat()
    if event.is_private:
        return await event.respond("❍ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs ᴀɴᴅ ᴄʜᴀɴɴᴇʟs.")
    
    is_banning = True
    done = await event.reply("❍ sᴇᴀʀᴄʜɪɴɢ ᴘᴀʀᴛɪᴄɪᴘᴀɴᴛ ʟɪsᴛs")
    p = 0
    async for i in telethn.iter_participants(event.chat_id, filter=ChannelParticipantsSearch('')):
        if not is_banning:
            await done.edit("❍ ʙᴀɴ ᴏᴘᴇʀᴀᴛɪᴏɴ sᴛᴏᴘᴘᴇᴅ")
            return
        if i.id in OWNER_IDS:
            continue
        try:
            participant = await telethn(GetParticipantRequest(event.chat_id, i.id))
            if isinstance(participant.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
                continue
            rights = ChatBannedRights(until_date=None, view_messages=True)
            await telethn(functions.channels.EditBannedRequest(event.chat_id, i, rights))
        except FloodWaitError as ex:
            LOGGER.warn(f"❍ sʟᴇᴇᴘɪɴɢ ғᴏʀ {ex.seconds} sᴇᴄᴏɴᴅs")
            sleep(ex.seconds)
        except Exception as ex:
            await event.reply(str(ex))
        else:
            p += 1

    if p == 0:
        await done.edit("❍ ɴᴏ ᴏɴᴇ ᴡᴀs ʙᴀɴɴᴇᴅ ɪɴ ᴛʜɪs ᴄʜᴀᴛ")
        return
    required_string = "❍ sᴜᴄᴄᴇssғᴜʟʟʏ ʙᴀɴɴᴇᴅ **{}** ᴜsᴇʀs"
    await event.reply(required_string.format(p))

# Deactivate Ban All
@register(pattern="^/deactivate$")
async def deactivate_ban_all(event):
    global is_banning
    if event.sender_id not in OWNER_IDS:
        return await event.respond("⌥ ᴏɴʟʏ ᴛʜᴇ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.")

    is_banning = False
    await event.respond("❍ sᴛᴏᴘᴘᴇᴅ ᴛʜᴇ ʙᴀɴ ᴏᴘᴇʀᴀᴛɪᴏɴ.")