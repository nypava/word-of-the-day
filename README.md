# Word of the day 
Word of the day is a simple automated script that posts new words from [Merriam-Webster](https://merriam-webster.com/) to a channel. Demo channel: @wordoftheday_s

## Deployment

### Installing dependencies

```
pip install -r requirements.txt
```

### Setup
Create .env file with the following variable:
```
bot_token = "" # Bot token from @botfather
channel_id = "" # Channel ID or username of the channel where the messages will be posted
mongo_token = "" # MongoDB database key from [mongodb](https://mongodb.com)
gemini_key = "" # Gemini key from https://aistudio.google.com/app/apikey
```
After changing the .env file, run the script:
 ```sh
 python3 bot.py
 ```

**Note**: Don't forget to add the bot to your channel and give it admin privileges.
