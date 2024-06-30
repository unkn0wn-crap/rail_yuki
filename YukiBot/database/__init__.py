#MIT License
#Copyright (c) 2023, ©NovaNetworks

import motor.motor_asyncio

from YukiBot import MONGO_DB_URI

DBNAME = "YukiBot"

mongo = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DB_URI)
dbname = mongo[DBNAME]
