from pymongo import MongoClient
from app.config import settings
from pymongo import MongoClient
from app.config import settings


print("DB NAME =", settings.DATABASE_NAME)

client = MongoClient(settings.MONGODB_URI)
db = client[settings.DATABASE_NAME]

def get_session():
    return client.start_session()

users_collection = db["users"]
wallets_collection = db["wallets"]
transactions_collection = db["transactions"]
idempotency = db["idempotency_keys"]

