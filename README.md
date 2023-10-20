# Word of the day 

Word of the day is a simple automated script that posts new words from [Merriam-Webster](https://merriam-webster.com/) to a channel. Demo channel: @wordoftheday_s

## Deployment

### Installing dependencies

```
pip install -r requirements.txt
```

### Setup
Change the following variables in the .env file:

* bot_token - Bot token from @botfather
* channel_id - Channel ID or username of the channel where the messages will be posted
* bot_username - Main bot username (not the one that sends the post)
* mongo_key - MongoDB database key from [mongodb](https://mongodb.com)

After changing the .env file, run the script:
 ```sh
 python3 app.py
 ```

**Note**: Don't forget to add the bot to your channel and give it admin privileges
## Contribution Guidelines
- **How to contribute**

    - Fork the repository.
    - Create a new branch for your changes.
    - Make your changes and commit them to your branch.
    - Push your branch to GitHub.
    - Open a pull request against the main branch.

- **Coding style**
    - Just try to be more consistent with the current project's coding style.