import asyncio
import re
from telethon import TelegramClient, events
from telethon.errors import MessageIdInvalidError

api_id = 4608923
api_hash = '0fc54e6096c9cd77cd1e1954b899676d'

async def main():
    client = TelegramClient('session_name', api_id, api_hash)
    await client.start()

    print('''
          Zoro Bot Fishing Auto  
          On it!!
                                 ~ paradox  ''')

    @client.on(events.NewMessage(from_users=5284997893))
    async def handle_ready(event):
        if "Are you ready?" in event.raw_text:
            try:
                await asyncio.sleep(1.2)
                await event.click(0)  # click the first button
            except (asyncio.TimeoutError, MessageIdInvalidError):
                pass
        
    @client.on(events.MessageEdited(from_users=5284997893))
    async def handle_catch(event):
        if "You caught" in event.raw_text:
            try:
                await asyncio.sleep(1.5)
                await client.send_message(5284997893, '/fish')  # send /fish message
            except (asyncio.TimeoutError, MessageIdInvalidError):
                pass

    @client.on(events.NewMessage(from_users=5284997893))
    async def handle_wait(event):
        match = re.search(r'You need to wait (\d+)m:(\d+)s for it to regenerate!', event.raw_text)
        if match:
            try:
                minutes = int(match.group(1))
                seconds = int(match.group(2))
                total_wait_time = minutes * 60 + seconds
                print(f'Waiting for {total_wait_time} seconds to regenerate...')
                await asyncio.sleep(total_wait_time)
                await client.send_message(5284997893, '/fish') 
                print('Sent /fish message')
            except Exception as e:
                print(f'An error occurred: {e}')

    @client.on(events.NewMessage(from_users=5284997893))
    async def handle_already_fishing(event):
        if "Do /stopfish" in event.raw_text:
            try:
                await asyncio.sleep(1.0)
                await client.send_message(5284997893, '/stopfish')
                print('Sent /stopfish message')
            except (asyncio.TimeoutError, MessageIdInvalidError):
                pass

    @client.on(events.NewMessage(from_users=5284997893))
    async def handle_stop_fishing(event):
        if "You stopped fishing!" in event.raw_text:
            try:
                await asyncio.sleep(0.8)
                await client.send_message(5284997893, '/fish')
                print('Sent /fish message after stopping fishing')
            except (asyncio.TimeoutError, MessageIdInvalidError):
                pass

    @client.on(events.NewMessage(from_users=6810396528))
    async def handle_paradox(event):
        if "paradox" in event.raw_text:
            try:
                await asyncio.sleep(1.0)
                await client.send_message(6810396528, 'Zoro Bot Fishing Auto is working!') 
            except (asyncio.TimeoutError, MessageIdInvalidError):
                pass

    await client.run_until_disconnected()

asyncio.run(main())
