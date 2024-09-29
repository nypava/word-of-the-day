from imageio.v2 import save
from pymongo import MongoClient
from bson.raw_bson import RawBSONDocument
from dotenv import load_dotenv

class Database:
    def __init__(self, mongo_token) -> None:
        client = MongoClient(mongo_token)
        self.vocabulary_db = client.db.vocabulary
        self.saved_db = client.db.saved
        self.word_db = client.db.words

    def add_vocal(
        self,
        word:str, 
        pronunciation:str, 
        meaning:str, 
        context:str, 
        facts:str,
        podcast: str,
        questions: dict,
    ) -> None:

        vocab_data = {
            "word": word,
            "pronunciation": pronunciation,
            "meaning": meaning,
            "context": context,
            "facts": facts,
            "podcast": podcast,
            "questions": questions
        }
    
        self.vocabulary_db.insert_one(vocab_data)
        return
    
    def get_vocal(self, word:str) -> dict:
        return self.vocabulary_db.find_one({"word": word}) #type: ignore
    
    def add_save(self, user_id:int, word:str, message_url:str) -> None:
        saved_data = self.get_save(user_id) 
        words = saved_data if saved_data else [] #type: ignore
        words.append({"word": word, "message_url": message_url})

        self.saved_db.update_one(
            {"user_id": user_id}, 
            {
                "$setOnInsert": {"user_id": user_id},
                "$set": {"words": words}, 
            },
            upsert=True
        )

    def get_save(self, user_id:int) -> list|None:
        return self.saved_db.find_one({"user_id": user_id})["words"] #type: ignore

    def remove_save(self, user_id:int, word:str) -> None:
        words = self.get_save(user_id) 
        
        for index in range(len(words)):  #type: ignore
            if word == words[index]["word"]: #type: ignore
                words.remove(words[index]) #type: ignore
                break
        
        self.saved_db.update_one(
            {"user_id": user_id}, 
            {
                "$setOnInsert": {"user_id": user_id},
                "$set": {"words": words}, 
            },
            upsert=True
        )

    def exist_save(self, user_id:int, word:str) -> bool:
        if not self.get_save(user_id):
            return False

        for i in self.get_save(user_id): #type: ignore
            if i["word"] == word:
                return True

        return False
