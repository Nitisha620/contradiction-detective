import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")

    APP_ENV: str = os.getenv("APP_ENV", "development")

    REQUEST_TIMEOUT:int = int(
        os.getenv("REQUEST_TIMEOUT", "120000")
    )

settings = Settings()