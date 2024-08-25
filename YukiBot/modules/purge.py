import time

from telethon import events

from YukiBot import telethn,pbot
from YukiBot.modules.helper_funcs.telethn.chatstatus import (
    can_delete_messages,
    user_is_admin,
)
from pyrogram.enums import ChatMemberStatus


async def purge_messages(event):
    start = time.perf_counter()
    
    if event.from_id is None:
        return
    
    # Check if the user is an admin with delete message rights
    member = await event.client.get_chat_member(event.chat_id, event.sender_id)
    
    # Ensure the user is either an admin or in the sudo list and has delete rights
    if not (
        member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
        and member.privileges.can_delete_messages
    ) and event.from_id not in [1087968824]:  # This ID can be for SUDO
        await event.reply("❍ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴡɪᴛʜ ᴅᴇʟᴇᴛᴇ ʀɪɢʜᴛs ᴀʀᴇ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ")
        return

    # Check if the bot can delete messages
    if not await can_delete_messages(message=event):
        await event.reply("❍ ᴄᴀɴ'ᴛ sᴇᴇᴍ ᴛᴏ ᴘᴜʀɢᴇ ᴛʜᴇ ᴍᴇssᴀɢᴇ")
        return

    # Get the reply message to determine where to start purging
    reply_msg = await event.get_reply_message()
    if not reply_msg:
        await event.reply("❍ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ sᴇʟᴇᴄᴛ ᴡʜᴇʀᴇ ᴛᴏ sᴛᴀʀᴛ ᴘᴜʀɢɪɴɢ ғʀᴏᴍ.")
        return

    messages = []
    message_id = reply_msg.id
    delete_to = event.message.id

    messages.append(event.reply_to_msg_id)
    
    # Collect messages to delete in batches of 100
    for msg_id in range(message_id, delete_to + 1):
        messages.append(msg_id)
        if len(messages) == 100:
            await event.client.delete_messages(event.chat_id, messages)
            messages = []

    try:
        # Delete remaining messages
        await event.client.delete_messages(event.chat_id, messages)
    except:
        pass

    # Calculate and report the time taken to purge messages
    time_ = time.perf_counter() - start
    text = f"❍ ᴘᴜʀɢᴇᴅ ꜱᴜᴄᴄᴇssғᴜʟʟʏ ɪɴ {time_:0.2f} ꜱᴇᴄᴏɴᴅ(s)"
    await event.respond(text, parse_mode="markdown")


async def delete_messages(event):
    if event.from_id is None:
        return

    # Check if the user is an admin with delete message rights
    member = await event.client.get_chat_member(event.chat_id, event.sender_id)
    
    # Ensure the user is either an admin with delete rights or a sudo user
    if not (
        member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
        and member.privileges.can_delete_messages
    ) and event.from_id not in [1087968824]:  # SUDO User ID
        await event.reply("❍ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴡɪᴛʜ ᴅᴇʟᴇᴛᴇ ʀɪɢʜᴛs ᴀʀᴇ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ")
        return

    # Check if the bot can delete messages
    if not await can_delete_messages(message=event):
        await event.reply("❍ ᴄᴀɴ'ᴛ sᴇᴇᴍ ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴛʜɪs ?")
        return

    # Get the message to delete
    message = await event.get_reply_message()
    if not message:
        await event.reply("❍ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ sᴇʟᴇᴄᴛ ᴡʜᴀᴛ ᴛᴏ ᴅᴇʟᴇᴛᴇ.")
        return
    
    # Get chat and delete the messages
    chat = await event.get_input_chat()
    del_message = [message, event.message]
    await event.client.delete_messages(chat, del_message)


async def spurge_messages(event):
    if event.from_id is None:
        return
    
    # Check if the user is an admin with delete message rights
    member = await event.client.get_chat_member(event.chat_id, event.sender_id)
    
    # Ensure the user is either an admin with delete rights or a sudo user
    if not (
        member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
        and member.privileges.can_delete_messages
    ) and event.from_id not in [1087968824]:  # SUDO User ID
        await event.reply("❍ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴀʀᴇ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ")
        return

    # Check if the bot can delete messages
    if not await can_delete_messages(message=event):
        await event.reply("❍ ᴄᴀɴ'ᴛ sᴇᴇᴍ ᴛᴏ ᴘᴜʀɢᴇ ᴛʜᴇ ᴍᴇssᴀɢᴇs")
        return

    reply_msg = await event.get_reply_message()
    if not reply_msg:
        await event.reply("❍ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ sᴇʟᴇᴄᴛ ᴡʜᴇʀᴇ ᴛᴏ sᴛᴀʀᴛ ᴘᴜʀɢɪɴɢ ғʀᴏᴍ.")
        return

    messages = []
    message_id = reply_msg.id
    delete_to = event.message.id

    # Collect messages for deletion
    for msg_id in range(message_id, delete_to + 1):
        messages.append(msg_id)
        if len(messages) == 100:
            await event.client.delete_messages(event.chat_id, messages)
            messages = []

    # Delete remaining messages
    try:
        if messages:
            await event.client.delete_messages(event.chat_id, messages)
    except Exception as e:
        await event.reply(f"❍ ᴇʀʀᴏʀ ᴅᴜʀɪɴɢ ᴘᴜʀɢɪɴɢ: {str(e)}")


__help__ = """
 ❍ /del *➛* ᴅᴇʟᴇᴛᴇs ᴛʜᴇ ᴍᴇssᴀɢᴇ ʏᴏᴜ ʀᴇᴘʟɪᴇᴅ ᴛᴏ
 ❍ /purge *➛* ᴅᴇʟᴇᴛᴇs ᴀʟʟ ᴍᴇssᴀɢᴇs ʙᴇᴛᴡᴇᴇɴ ᴛʜɪs ᴀɴᴅ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴛᴏ ᴍᴇssᴀɢᴇ.
 ❍ /purge  <ɪɴᴛᴇɢᴇʀ x>* ➛* ᴅᴇʟᴇᴛᴇs ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ, ᴀɴᴅ x ᴍᴇssᴀɢᴇs ғᴏʟʟᴏᴡɪɴɢ ɪᴛ ɪғ ʀᴇᴘʟɪᴇᴅ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ.
 ❍ /spurge *➛* ᴅᴇʟᴇᴛᴇs ᴀʟʟ ᴍᴇssᴀɢᴇs ʙᴇᴛᴡᴇᴇɴ ᴛʜɪs ᴀɴᴅ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴛᴏ ᴍᴇssᴀɢᴇ.
"""

PURGE_HANDLER = purge_messages, events.NewMessage(pattern="^[!/]purge$")

DEL_HANDLER = delete_messages, events.NewMessage(pattern="^[!/]del$")
SPURGE_HANDLER = spurge_messages, events.NewMessage(pattern="^[!/]spurge$")
telethn.add_event_handler(*PURGE_HANDLER)
telethn.add_event_handler(*DEL_HANDLER)
telethn.add_event_handler(*SPURGE_HANDLER)

__mod_name__ = "ᴘᴜʀɢᴇ"

__command_list__ = ["del", "purge","spurge"]

__handlers__ = [PURGE_HANDLER, DEL_HANDLER,SPURGE_HANDLER]
    
