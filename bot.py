from telebot.types import CallbackQuery, Message, InputPollOption
from telebot import TeleBot
from utils.word_scraper import WordScraper
from utils.video_editor import VideoEditor
from utils.video_scraper import VideoScraper
from utils.question_gen import question_generator
from utils.bot.button import *
from utils.database.database import Database
from dotenv import load_dotenv
from json import load
import schedule, os, time
import threading 

load_dotenv()

bot_token = os.getenv("bot_token")
channel_id = os.getenv("channel_id")
mongo_token = os.getenv("mongo_token")
gemini_key = os.getenv("gemini_key")

bot = TeleBot(str(bot_token))
database = Database(mongo_token)

username = bot.get_me().username

with open("./utils/bot/text.json", "r+") as file:
    texts = load(file)

@bot.callback_query_handler(func=lambda call:True)
def save_handler(callback: CallbackQuery):
    callback_data = callback.data
    user_id = callback.from_user.id

    if "save" in str(callback_data):
        word = str(callback_data).split("_")[-1]
        message_url = f"https://t.me/{callback.message.chat.username}/{callback.message.id}"
    
        if database.exist_save(user_id, word):
            database.remove_save(user_id, word)
            bot.answer_callback_query(callback.id, texts["word_removed"].format(word), show_alert=True) 
            return
            
        database.add_save(user_id, word, message_url)
        bot.answer_callback_query(callback.id, texts["word_added"].format(word, username), show_alert=True) 
    elif "list_words" in str(callback_data):
        if not database.get_save(user_id): 
            bot.send_message(user_id, texts["word_empty"], parse_mode="MarkdownV2")
            bot.answer_callback_query(callback.id, "")
            return

        list_words_str = ""
        for word_data in database.get_save(user_id): #type: ignore
            list_words_str += f"• [{word_data["word"]}]({word_data["message_url"]}) \n" 
        
        list_words_str += texts["words_list"]
        bot.send_message(user_id, list_words_str, parse_mode="MarkdownV2", disable_web_page_preview=True)  
        bot.answer_callback_query(callback.id, "")

@bot.message_handler(commands=["start"])
def start_handler(message: Message):
    user_id = int(message.from_user.id) #type: ignore
    
    if len(str(message.text).split()) == 1:
        bot.send_message(user_id, texts["welcome_message"], parse_mode="MarkdownV2", reply_markup=start_button)
        return
    
    splitted_text = (str(message.text).split()[-1]).split("_")

    if splitted_text[0] == "word":
        word_data:dict = database.get_vocal(splitted_text[-1])
        bot.send_audio(user_id, audio=word_data["podcast"])
        bot.send_message(user_id, texts["more_info"].format(word_data["context"], word_data["facts"]), parse_mode="HTML" )

    elif splitted_text[0] == "quiz":
        questions = database.get_vocal(splitted_text[-1])["questions"]

        for question in questions.keys():
            bot.send_poll(
                user_id, 
                question=question,
                options=[InputPollOption(questions[question]["choices"][i]) for i in range(4)],
                correct_option_id=questions[question]["answer"], 
                type="quiz"
            )

@bot.message_handler(commands=["list_saved"])
def list_saved(message: Message):
    user_id = message.from_user.id #type: ignore
    list_words_str = ""

    if not database.get_save(user_id): 
        bot.send_message(user_id, texts["word_empty"], parse_mode="MarkdownV2")
        return

    for word_data in database.get_save(user_id): #type: ignore
        list_words_str += f"• [{word_data["word"]}]({word_data["message_url"]}) \n" 
        
    list_words_str += texts["words_list"]
    bot.send_message(user_id, list_words_str, parse_mode="MarkdownV2", disable_web_page_preview=True)  

def send_post():
    vocab_datas = WordScraper()
    vocab_datas.generate()

    post_text = f"<b>{vocab_datas.word}</b>\n<i>{vocab_datas.pronunciation}</i>\n\n{vocab_datas.meaning}\n{vocab_datas.example.replace('//', '•')}"

    video_scrapper = VideoScraper()
    videos_list = video_scrapper.get_videos("exorbitant")

    video_scrapper.download('./cache', videos_list)

    questions = question_generator(str(gemini_key), vocab_datas.word)

    database.add_vocal(
        vocab_datas.word, 
        vocab_datas.pronunciation, 
        vocab_datas.meaning, 
        vocab_datas.context,
        vocab_datas.facts,
        vocab_datas.podcast,
        questions
    )

   
    if not videos_list: 
        with open("./assets/video-error.png", "rb+") as file:
            bot.send_photo(str(channel_id), 
                       caption=post_text, 
                       photo=file, 
                       parse_mode="HTML", 
                       reply_markup=post_button(str(username), vocab_datas.word))
        return 

    video_editor = VideoEditor()

    for video in videos_list:
        video_editor.add_subtitle(video["video_id"], video["video_subtitle"], "./cache", "exorbitant")
    
    video_editor.concatenate_videos("./cache/result.mp4")
    
    with open("./cache/result.mp4", "rb+") as file:
        bot.send_video(str(channel_id), 
                       caption=post_text, 
                       video=file, 
                       parse_mode="HTML", 
                       reply_markup=post_button(str(bot.get_me().username), vocab_datas.word))

    video_scrapper.cache_clr("./cache")

send_post()

schedule.every().day.at("14:10").do(send_post)

def schedule_send():
    while True:
        schedule.run_pending()
        time.sleep(1)

schedule_thread = threading.Thread(target=schedule_send)
schedule_thread.start()

bot.infinity_polling()
