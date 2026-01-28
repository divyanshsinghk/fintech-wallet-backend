from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    MONGODB_URI: str = os.getenv("MONGODB_URI")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME")

settings = Settings()
