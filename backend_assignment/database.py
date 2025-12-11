from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

client = AsyncIOMotorClient(settings.DATABASE_URL)
db = client[settings.MONGO_INITDB_DATABASE]

def get_database():
    return db
