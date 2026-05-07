from telegram import Bot
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import pytz
import asyncio

MOVIE_CHAT_ID = "-323399540"

# Environment
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

CHAT_ID = MOVIE_CHAT_ID

bot = Bot(token=TOKEN)

def get_next_weekend():
    now = datetime.now(pytz.timezone("Asia/Singapore"))

    # find next Saturday
    days_until_sat = (5 - now.weekday()) % 7
    saturday = now + timedelta(days=days_until_sat)

    sunday = saturday + timedelta(days=1)

    return saturday.strftime("%b %d"), sunday.strftime("%d")

async def send_poll():
    sat, sun = get_next_weekend()
    await bot.send_poll(
        chat_id=CHAT_ID,
        question=f"Next weekend? {sat}-{sun} (GMT+8)",
        options=[
            "Sat Afternoon (UK Morning)",
            "Sat Evening (UK Afternoon)",
            "Sun Afternoon (UK Morning)",
            "Sun Evening (UK Afternoon)",
            "Try again next week sucka",
        ],
        is_anonymous=False,
        allows_multiple_answers=True
    )
    print("Send poll")

if __name__ == "__main__":
    asyncio.run(send_poll())