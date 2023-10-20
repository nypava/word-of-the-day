import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()

mongo_key = os.getenv("mongo_key")

# Create a mongo db instance
client = MongoClient(mongo_key)
words = client.wotd.words

class Database:
    @staticmethod
    def insert_vocab(word:str, pronunciation:str, meaning:str, context:str, facts:str):
        """
        Insert new vocabulary to database.
        """
        vocab_schema = {
            "word": word,
            "pronunciation": pronunciation,
            "meaning": meaning,
            "context": context,
            "facts": facts
        }
        
        words.insert_one(vocab_schema)