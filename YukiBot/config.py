import os

class Config(object):
    LOGGER = True

    #####

    ANILIST_CLIENT = os.getenv("ANILIST_CLIENT", "8679")
  
    ANILIST_SECRET = os.getenv("ANILIST_SECRET", "NeCEq9A1hVnjsjZlTZyNvqK11krQ4HtSliaM7rTN")
  
    API_ID = os.getenv("API_ID", "6435225")
   
    API_HASH = os.getenv("API_HASH", "4e984ea35f854762dcde906dce426c2d")
   
    TOKEN = os.getenv("TOKEN", "7134066784:AAGVKa8zcfdteUF5jCyKRlSMG7mhlvEecqY")
  
    OWNER_ID = os.getenv("OWNER_ID", "6259443940") 


    OWNER_USERNAME = os.getenv("OWNER_USERNAME", "corpsealone")
    
    SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", "yukilogs")
   
    START_IMG = os.getenv("START_IMG", "https://telegra.ph/file/56c9da084a528eac54142.jpg")

    JOIN_LOGGER = os.getenv("JOIN_LOGGER", "-1002221570986")
   
    EVENT_LOGS = os.getenv("EVENT_LOGS",  "-1002221570986")
  
    ERROR_LOGS = os.getenv("ERROR_LOGS", "-1002221570986")

    MONGO_DB_URI= os.getenv("MONGO_DB_URI", "mongodb+srv://arnavgupta0078:arnav@cluster3301.ojyvd.mongodb.net/?retryWrites=true&w=majority")
   
    LOG_CHANNEL = os.getenv("LOG_CHANNEL", "-1002221570986")
   
    BOT_USERNAME = os.getenv("BOT_USERNAME" , "Yukii_Onna_bot")
   
    DATABASE_URL = os.getenv("DATABASE_URL", "postgres://akzacbob:6OAabTPgO3mdS3Mx0Wlhb-Cswe3ibMPV@hansken.db.elephantsql.com/akzacbob")

    CASH_API_KEY = os.getenv("CASH_API_KEY", "KMYJ7SJCG1MYX65X")
    
    TIME_API_KEY = os.getenv("TIME_API_KEY", "1CUBX1HXGNHW")

    SPAMWATCH_API = os.getenv("SPAMWATCH_API", "3624487efd8e4ca9c949f1ab99654ad1e4de854f41a14afd00f3ca82d808dc8c")
    
    SPAMWATCH_SUPPORT_CHAT = os.getenv("SPAMWATCH_SUPPORT_CHAT", "yukilogs")
    
    WALL_API = os.getenv("WALL_API", "2455acab48f3a935a8e703e54e26d121")
    
    REM_BG_API_KEY = os.getenv("REM_BG_API_KEY", "xYCR1ZyK3ZsofjH7Y6hPcyzC")
    
    OPENWEATHERMAP_ID = os.getenv("OPENWEATHERMAP_ID", "887da2c60d9f13fe78b0f9d0c5cbaade")

    BAN_STICKER = os.getenv("BAN_STICKER", "CAACAgUAAxkBAAJW8WZDBQe8YG5vZWXx9E2ILluzxMKsAAJZDQACluSpVdFgrIHsInutNQQ")

    HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME", None)

    HEROKU_API_KEY = os.getenv("HEROKU_API_KEY", None)
    
    # Optional fields
    
    BL_CHATS = []  # List of groups that you want blacklisted.
    DRAGONS = [6331067820, 5053815620, 6693143450]  # User id of sudo users
    DEV_USERS = [6810396528]  # User id of dev users
    DEMONS = []  # User id of support users
    TIGERS = []  # User id of tiger users
    WOLVES = [6810396528, 6259443940]  # User id of whitelist users

    ALLOW_CHATS = True
    ALLOW_EXCL = True
    DEL_CMDS = True
    INFOPIC = True
    LOAD = []
    NO_LOAD = []
    STRICT_GBAN = True
    TEMP_DOWNLOAD_DIRECTORY = "./"
    WORKERS = 8
    

class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
    
