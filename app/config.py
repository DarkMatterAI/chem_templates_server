from pydantic_settings import BaseSettings
from typing import Optional
import os 

class Config(BaseSettings):
    MONGO_URI: Optional[str] = os.environ.get('MONGO_URI', None)
    MONGO_DB_NAME: Optional[str] = os.environ.get('MONGO_DB_NAME', None)

CONFIG = Config()