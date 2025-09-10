
import os


class Settings():
    signing_key =  os.getenv("SIGNING_KEY")
    database_url = os.getenv("DATABASE_URL") or "sqlite:///./database.db"