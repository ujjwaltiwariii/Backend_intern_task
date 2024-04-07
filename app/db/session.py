# from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from app.utils.config import get_settings,logger
settings=get_settings()

db_client:AsyncIOMotorClient=None


def get_client()->AsyncIOMotorClient:
    global db_client
    if db_client is None:
        init_db()
    return db_client

def init_db()->AsyncIOMotorClient:
    global db_client
    try:
        db_client = AsyncIOMotorClient(settings.uri)
        # client.admin.command('ping')
        logger.info("Connected to MongoDB")
        # print(client.start_session)
    except Exception as e:
        logger.error(f"Unable to connect to MongoDB: {e}")

def close_db():
    global db_client
    if db_client is not None:
        db_client.close()
        logger.info("Connection to MongoDB closed")
        
    
    

    
