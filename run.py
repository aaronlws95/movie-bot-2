import os
from dotenv import load_dotenv
from bot import Bot

# Environment
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

bot = Bot()
bot.run(TOKEN)