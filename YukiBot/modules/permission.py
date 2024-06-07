import logging
from telethon import events, functions, types
from YukiBot import telethn as bot  # Assuming 'telethn' is your bot instance in YukiBot

logging.basicConfig(level=logging.INFO)

@bot.on(events.ChatAction)
async def handler(event):
    if event.user_added and event.user_id == (await bot.get_me()).id:
        await event.reply("Thank you for adding me! Please grant me admin rights with ban permissions to ensure I can function properly.")

@bot.on(events.NewMessage(pattern='/grantpermissions'))
async def grant_permissions(event):
    if event.is_group and event.is_channel:
        try:
            participant = await bot(functions.channels.GetParticipantRequest(
                channel=event.chat_id,
                user_id=event.sender_id
            ))

            if not isinstance(participant.participant, (types.ChannelParticipantAdmin, types.ChannelParticipantCreator)):
                await event.reply("Only group admins can use this command.")
                return

            await bot(
                functions.channels.EditAdminRequest(
                    channel=event.chat_id,
                    user_id=event.sender_id,
                    admin_rights=types.ChatAdminRights(
                        add_admins=False,
                        invite_users=True,
                        change_info=True,
                        ban_users=True,
                        delete_messages=True,
                        pin_messages=True
                    ),
                    rank='admin'
                )
            )
            await event.reply("Admin rights granted with ban permissions!")
        except Exception as e:
            await event.reply(f"Failed to grant admin rights: {str(e)}")