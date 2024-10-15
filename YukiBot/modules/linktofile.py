from YukiBot import pbot as bot
from pyrogram import filters, types
import pymongo
import string
import random

# MongoDB connection setup
MONGO_URI = "mongodb+srv://arnavgupta0078:arnav@cluster3301.ojyvd.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "LinkToShare"
COLLECTION_NAME = "tokens"

# Connect to the MongoDB client
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

link = 'yukii_onna_bot.t.me?start=getfile-{}'

def gen_token(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def get_user_token_and_index(user_id):
    user_data = collection.find_one({'user_id': user_id})
    if user_data:
        tokens_with_count = [(key, len(value)) for key, value in user_data.items() if key not in ['_id', 'user_id']]
        return tokens_with_count
    return []

def get_file_ids_by_token(token):
    for user_data in db.find():
        if token in user_data:
            user_id = user_data['user_id']
            file_ids = user_data[token]
            return user_id, file_ids
    return None, None

def get_user_tokens(user_id):
    user_data = collection.find_one({'user_id': user_id})
    if user_data:
        tokens = [key for key in user_data.keys() if key not in ['_id', 'user_id']]
        return tokens
    return []

def delete_file(user_id, token, index):
    result = collection.update_one(
        {'user_id': user_id, token: {'$exists': True}},
        {'$unset': {f"{token}.{index}": ""}}
    )
    # Remove any 'None' values from the list after deletion
    collection.update_one(
        {'user_id': user_id, token: {'$exists': True}},
        {'$pull': {token: None}}
    )
    return result.modified_count == 1

def delete_token(user_id, token):
    result = collection.update_one(
        {'user_id': user_id},
        {'$unset': {token: ""}}
    )
    return result.modified_count > 0

@bot.on_message(filters.command(['clearfile','cfile']))
async def clear_file(_, message):
     m = message
     r = message.reply_to_message

     usage = "❌ Give the token with number `/cfile token 0`"

     if len(message.command) == 3:
          token = m.text.split()[1]
          try:
             file_id = int(m.text.split()[2])-1
          except ValueError:
             return await m.reply_text(
               text=usage
) 
     else:
         return await m.reply_text(
             text=usage
         )

     user_id = m.from_user.id

     if delete_file(user_id, token, file_id):
          return await m.reply_text(
               f"⛔ File deleted from token {token}"
                                       )
     else:
          return await m.reply_text(
                "❌ File doesn't exsit in Token."
              )             


@bot.on_message(filters.command(['cleartoken','deltoken']))
async def clear_token(_, message):
     m = message
     if len(message.command) != 2:
          return await m.reply_text("Ok! but where token to delete?")
     else:
          user_id = m.from_user.id
          if delete_token(user_id, m.text.split()[1]):
              return await m.reply_text(
                  "Token deleted!"
                                       )
          else:
              return await m.reply_text(
                  "Token doesn't exsit in database."
              )         

@bot.on_message(filters.command(["ctoken","checkt"]))
async def CheckToken(bot, message):

     if not message.from_user:
         return
     user_id = message.from_user.id
     if not len(message.text.split()) == 2:
           return await message.reply_text("Can you provide me token?\n```Example\n/checkt token```")
     token = message.text.split()[1]
     if not token in get_user_tokens(user_id):
          return await message.reply("Token Seems like invalid 🤔")
     button = types.InlineKeyboardMarkup([[types.InlineKeyboardButton("✨ Click here", url=link.format(token))]])
     return await message.reply_text(
         text="Click the below button to Get the all file's..",
         reply_markup=button
     )


@bot.on_message(filters.command(['gettokens', 'gettk']))
async def GetTokens(_, message):
    user_id = message.from_user.id
    tokens = get_user_token_and_index(user_id)
    String = f"**🌟 Stored tokens in {message.from_user.mention}**:\n"
    
    if tokens:
        for i, (token, file_count) in enumerate(tokens):
            String += f"{i+1}. `{token}`: **{file_count} files**\n"
    else:
        String += "No tokens found."

    return await message.reply_text(
        text=String, quote=True
    )

@bot.on_message(filters.command(['addfile', 'getlink']))
async def Getlink(_, message):
    user_id = message.from_user.id
    reply = message.reply_to_message
    file = (reply.document or reply.video) if reply and (reply.document or reply.video) else None

    if not file:
        return await message.reply('Please reply to a document or video file.')

    file_id = file.file_id
    user_data = {'user_id': user_id}

    if len(message.text.split()) == 2:
        token = message.text.split(None, 1)[1]
        existing_user = collection.find_one(user_data)
        if existing_user and token in existing_user:
            collection.update_one(
                user_data, {'$push': {token: file_id}}
            )
            return await message.reply(
                f'**Successfully added file to token.**\n**🌟 Token**: `{token}`',
                reply_markup=types.InlineKeyboardMarkup(
                    [[types.InlineKeyboardButton('Click here', url=link.format(token))]]
                )
            )
        else:
            return await message.reply('Sorry, that is not a valid token.')

    # Generate a new token if no token was specified
    token = gen_token()
    collection.update_one(
        {'user_id': user_id},
        {'$set': {token: [file_id]}},
        upsert=True
    )

    return await message.reply(
        f'**Successfully generated new token and added file.**\n**🌟 Token**: `{token}`',
        reply_markup=types.InlineKeyboardMarkup(
            [[types.InlineKeyboardButton('Click here', url=link.format(token))]]
        )
    )









from YukiBot import pbot as bot
#from YukiBot import DATABASE
#from YukiBot.helpers.decorator import devs_only
from pyrogram import filters, types
from YukiBot.modules.no_sql import YukiDb


import string
import config
import random



db = YukiDb['LINK_TO_FILE']

link = 'yukii_onna_bot.t.me?start=getfile-{}'    



__mod_name__ = "Fɪʟs Sᴛᴏʀᴇ"

__help__ = f"""
 **File Store bot**:

➩ /getlink: 
to upload a file and get a new token
also you can upload a file to a specific token like `/getlink token` with reply to document or video.

➩ /clearfile:
to remove a specific file from token using the index and token `/cfile token 0`

➩ /cleartoken:
To remove a token from user that means all file in the token removd from db.

➩ /checktoken:
Use it with query `/checktoken token` to get link for share.

➩ /gettokens:
to show your all saved tokens in db.

Also you can share files through inline.

Example: `@yukii_onna_bot fs token`
"""




@bot.on_message(filters.command(['gettokens', 'gettk']))
async def GetTokens(_, message):
    user_id = message.from_user.id
    tokens = await get_user_token_and_index(user_id)  # Await the function
    String = f"**🌟 Stored tokens in {message.from_user.mention}**:\n"

    if tokens:  # Check if tokens are present
        for i, (token, file_count) in enumerate(tokens):
            String += f"{i+1}. `{token}`: **{file_count} files**\n"
    else:
        String += "No tokens found."

    return await message.reply_text(
        text=String, quote=True
    )





@bot.on_message(filters.command(['addfile', 'getlink']))
async def Getlink(_, message):
       user_id = message.from_user.id
       reply = message.reply_to_message
       file = (reply.document or reply.video) if reply and (reply.document or reply.video) else False

       if file:

            file_id = file.file_id
            user_json = {'user_id': user_id}
            if db.find_one(user_json) and len(message.text.split()) == 2:
                 token = message.text.split(None, 1)[1]
                 ignore = ['_id', 'user_id']
                 user_tokens = [ token for token in db.find_one(user_json) if token not in ignore]
                 if token in user_tokens:
                     db.update_one(
                        user_json, {'$push': {token: file_id}})

                     return await message.reply(
                         f'**Successfully file added in token.**\n**🌟 Token**: `{token}`',
                   reply_markup=types.InlineKeyboardMarkup(
                       [[types.InlineKeyboardButton('Click here', url=link.format(token))]]
                   ))
                 else:
                     return await message.reply(
                         'Sorry. itz not a valid token 🤔')
            else:
                token = gen_token()
                db.update_one(
                   {'user_id': user_id},
                   {'$set': {token: [file_id]}},
                   upsert=True
                )                
                return await message.reply(
                   f'**Successfully new token generated and added file.**\n**🌟 Token**: `{token}`',
                    reply_markup=types.InlineKeyboardMarkup(
                        [[types.InlineKeyboardButton('click here', url=link.format(token))]]
                    ))
       else:
          return await message.reply(
       'Reply to the document file.'
   )