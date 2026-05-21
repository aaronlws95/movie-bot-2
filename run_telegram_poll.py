from telegram import Bot
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import pytz
import asyncio
import argparse

# Environment
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MOVIE_CHAT_ID = os.getenv("MOVIE_TELEGRAM_ID")

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
    message = await bot.send_poll(
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
    # Pin it so Thursday's script can find it easily
    await bot.pin_chat_message(chat_id=CHAT_ID, message_id=message.message_id)
    print(f"Poll sent and pinned: {message.message_id}")

async def check_poll():
    # 1. Find the pinned message
    chat = await bot.get_chat(CHAT_ID)
    
    # If no pinned message, it means we already finished for the week
    if not chat.pinned_message or not chat.pinned_message.poll:
        print("No active poll to check. Skipping.")
        return

    poll = chat.pinned_message.poll
    total_voters = poll.total_voter_count
    
    # Identify the specific options
    # We assume "Try again next week sucka" is the last option
    fail_option = poll.options[-1] 
    unanimous_options = [o.text for o in poll.options[:-1] if o.voter_count == 4]

    now = datetime.now(pytz.timezone("Asia/Singapore"))
    is_thursday = now.weekday() == 3  # 0=Mon, 3=Thu

    # --- LOGIC FLOW ---

    # 1. Check for "Try again next week" (Message B)
    if fail_option.voter_count >= 1:
        await bot.send_message(CHAT_ID, "Try again next week suckas")
        await bot.unpin_chat_message(CHAT_ID, chat.pinned_message.message_id)
        return

    # 2. Check for Unanimous Winners (Message A)
    if unanimous_options:
        categories = " or ".join(unanimous_options)
        await bot.send_message(CHAT_ID, f"We on baby. {categories}. ")
        await bot.unpin_chat_message(CHAT_ID, chat.pinned_message.message_id)
        return

    # 3. Unique Voters, No Unanimity (Split Vote)
    if total_voters >= 4:
        await bot.send_message(CHAT_ID, f"Looks like we offz suckas.")
        await bot.unpin_chat_message(CHAT_ID, chat.pinned_message.message_id)
        return
    
    # 4. Thursday Deadline (Message C)
    if is_thursday:
        # Note: We do NOT unpin here, so it keeps checking Fri/Sat
        await bot.send_message(CHAT_ID, "Somebody needs to vote soon or we gonna have trouble.")
        return
    
    print("Criteria not met, checking again tomorrow.") 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Movie Poll Bot Runner")
    
    # Using action="store_true" allows you to just use the flag name
    parser.add_argument("--send_poll", action="store_true", help="Send and pin a new poll")
    parser.add_argument("--check_poll", action="store_true", help="Check the current pinned poll")

    args = parser.parse_args()

    if args.send_poll:
        asyncio.run(send_poll())
    elif args.check_poll:
        asyncio.run(check_poll())
    else:
        parser.print_help()
