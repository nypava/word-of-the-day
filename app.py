from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import schedule, time
from telebot import TeleBot
from utils import Scraper
from dotenv import load_dotenv
from database import Database
import os

# Load environment variables from .env file
load_dotenv()

bot_token = os.getenv("bot_token")
channel_id = os.getenv("channel_id")
bot_username = os.getenv("bot_username")

# Create a Telegram bot instance
bot = TeleBot(bot_token)

def send_post():
    """
    Scrape and post a message to the channel.
    """
    # Scrape vocabulary data
    vocab_datas = Scraper()
    vocab_datas.generate()

    # Insert vocabulary data into the database
    Database.insert_vocab(vocab_datas.word, 
                          vocab_datas.pronunciation, 
                          vocab_datas.meaning, 
                          vocab_datas.context,
                          vocab_datas.facts)
    
    post_text = f"<b>{vocab_datas.word}</b>\n<i>{vocab_datas.pronunciation}</i>\n\n{vocab_datas.meaning}\n{vocab_datas.example.replace('//', '•')}"

    # Create inline keyboard buttons
    buttons = InlineKeyboardMarkup([
                       [
                           InlineKeyboardButton("More ↪️", url=f"https://t.me/{bot_username}?start=word_{vocab_datas.word}")
                       ]
    ])

    # Send the post to the channel
    bot.send_audio(channel_id, 
                   caption=post_text, 
                   audio=vocab_datas.podcast, 
                   parse_mode="HTML", 
                   reply_markup=buttons)
    
schedule.every().day.at("12:00").do(send_post)

while True:
    schedule.run_pending()
    time.sleep(1)