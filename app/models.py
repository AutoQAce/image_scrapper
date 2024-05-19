from app.config import Config
import pymongo
from pymongo.errors import PyMongoError
import logging

# Configure logging (You should have this already set up in your app/utils/logging.py)
from app.utils.logging import setup_logging
setup_logging()

# MongoDB Connection Details
MONGO_URI = Config.MONGO_URI
DATABASE_NAME = Config.DATABASE_NAME
COLLECTION_NAME = Config.COLLECTION_NAME

class ImageScraperModel:
    """
    A model class to interact with MongoDB for storing image scraping data.
    """

    def __init__(self, mongo_uri=MONGO_URI):
        """
        Initializes the ImageScraperModel.

        Args:
            mongo_uri (str, optional): The MongoDB connection URI. Defaults to MONGO_URI.
        """
        try:
            self.client = pymongo.MongoClient(mongo_uri)
            self.db = self.client[DATABASE_NAME]
            self.collection = self.db[COLLECTION_NAME]
            logging.info("Connected to MongoDB successfully.")
        except PyMongoError as e:
            logging.error(f"Error connecting to MongoDB: {e}")
            raise  # Re-raise the exception for the caller to handle

    def insert_image_data(self, img_data):
        """
        Inserts image data into the MongoDB collection.

        Args:
            img_data (list): A list of dictionaries containing image data.
        """
        try:
            self.collection.insert_many(img_data)
            logging.info(f"Inserted {len(img_data)} image records.")
        except PyMongoError as e:
            logging.error(f"Error inserting image data: {e}")
            raise