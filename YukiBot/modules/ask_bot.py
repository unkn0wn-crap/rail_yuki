import requests

from pyrogram import filters, Client
from pyrogram.types import Message, InputMediaPhoto
from YukiBot import pbot as app
from pyrogram.errors import MediaCaptionTooLong
from pyrogram import Client, filters
import requests
from requests.exceptions import RequestException, ChunkedEncodingError

# Telegram bot token
#API_ID = "6435225"
#API_HASH = "4e984ea35f854762dcde906dce426c2d"
#BOT_TOKEN = "5527818445:AAE7TLprBfyUuQvYZsaOesQ0F-9C2sl2I80"

# Create the bot client
#app = Client("ask_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Command to handle /ask queries
@app.on_message(filters.command(["ask"]))
async def ask_query(client, message):
    # Get the user's query
    query = message.text.split(" ", 1)
    if len(query) < 2:
        await message.reply("Please provide a query. Usage: /ask what is string theory")
        return

    user_query = query[1]

    # Make the API request with the appropriate headers
    api_url = f"https://apis-awesome-tofu.koyeb.app/api/gemini?prompt={user_query}"
    headers = {
        "accept": "application/json"
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=10)  # Added timeout
        response.raise_for_status()  # Check for HTTP errors

        # Extract the response from the JSON
        api_response = response.json().get("reply", "No reply found.")
        # Send the formatted response
        await message.reply(api_response)

    except ChunkedEncodingError:
        await message.reply("There was a problem connecting to the API. Please try again.")
    except RequestException as e:
        await message.reply(f"An error occurred: \n Contact @yukiLOGS")
    except Exception as e:
        await message.reply(f"Something unexpected happened (well i know it is expexted)")


__mod_name__ = "ᴀɪ-ɢᴘᴛX"

__help__ = """

 ⬤ /ask *➥* ʀᴇᴘʟʏ ᴛo ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ 💭
 """