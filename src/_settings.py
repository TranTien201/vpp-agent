import os
import time

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    # Common
    OPENAI_API_KEY: str

    class Config:
        extra = "ignore"


settings = Settings(_env_file=".env")