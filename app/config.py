import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")


settings = Settings()
