from pydantic_settings import BaseSettings
from typing import Optional
import os 

class Config(BaseSettings):
    # MONGO_URI: Optional[str] = "mongodb://172.17.0.2:27017"
    # MONGO_DB_NAME: Optional[str] = "template_db"

    MONGO_URI: Optional[str] = os.environ.get('MONGO_URI', None)
    MONGO_DB_NAME: Optional[str] = os.environ.get('MONGO_DB_NAME', None)

CONFIG = Config()