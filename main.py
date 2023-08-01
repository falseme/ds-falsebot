from app import bot
from api import keys

if __name__ == "__main__":
    keys.load()
    bot.run(bot_token = keys.get_discord_token())