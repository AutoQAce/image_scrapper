# Configuration settings (development, testing, production)
import os
import os

from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path=Path("./.env"))

class Config:
    """Base configuration class"""
    MONGO_URI=f"mongodb+srv://{os.environ.get('DB_USERNAME')}:{os.environ.get('DB_PASSWORD')}@cluster0.qm6mxz1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    DATABASE_NAME = "image_scrap"
    COLLECTION_NAME = "image_scrap_data"

class TestConfig(Config):
    "Test Environment Configuration class"
    MONGO_URI = "TO_BE_DEFINED"
    DATABASE_NAME = "TO_BE_DEFINED"
    COLLECTION_NAME = "TO_BE_DEFINED"
