#MIT License
#Copyright (c) 2023, ©NovaNetworks

from async_pymongo import AsyncClient

from YukiBot import MONGO_DB_URI

DBNAME = "YukiBot"

mongo = AsyncClient(MONGO_DB_URI)
dbname = mongo[DBNAME]
