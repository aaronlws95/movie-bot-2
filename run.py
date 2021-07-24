import csv
import os
import random
from pathlib import Path
from datetime import datetime

import imdb
import discord
from discord.ext import commands
from dotenv import load_dotenv
from bot import Bot

import utils


# Environment
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Bot
# help_command = commands.DefaultHelpCommand(no_category = "Commands")
# intents = discord.Intents.default()
# intents.members = True
# intents.messages = True
# bot = commands.Bot(command_prefix="!", intents=intents, help_command=help_command)
bot = Bot()
bot.run(TOKEN)


# @bot.event
# async def on_ready():
#     print(f"{bot.user.name} is online")
#     guild = utils.discord.get_guild(bot, GUILD)
#     bot_info_channel = utils.discord.get_channel(guild, "bot-info")
#     await bot_info_channel.send("I'm back baby")

# @bot.command(name="initial-score",
#              brief="Handle initial scoring process",
#              description="Run the command to start scoring. The bot will DM you for a response. Unless explicitly given, participants will be taken from whoever is in the General voice channel.",
#              usage="!initial-score [person1] [person2] ... [personN]")
# async def initial_score(ctx, *args):


#     # Participants
#     if len(args) > 1:
#         participants = []
#         for i in range(1, len(args)):
#             # Validate member
#             member = await utils.discord.get_member(bot_info_channel, args[i])
#             if member:
#                 participants.append(member)

#         if not participants:
#             await bot_info_channel.send("Cannot find participants")
#             return
#     else:
#         participants = general_voice_channel.members

#         if not participants:
#             await bot_info_channel.send(
#                 "Cannot find participants in voice channel. Try !initial-score <person1> <person2> ... <personN>")
#             return

#     await bot_info_channel.send("Initial scoring started")

#     with open("data/next_discussion.csv", 'r') as f:
#         next_disc_data = csv.reader(f)
#         # title, type, chooser
#         return line[0], line[1], line[2]

#     # Initial formatting
#     # title, year, chooser = utils.csv.get_next_movie()
#     # date = datetime.today().strftime("%d/%m/%Y")
#     # await scores_channel.send("**{}: {}**".format(date, title))

#     # Scoring
#     for p in participants:
#         channel = await p.create_dm()
#         await channel.send("What is your initial score?")
#     await bot_info_channel.send("Waiting for everyone to give a score")

#     remaining = [p.name for p in participants]
#     scores = {}
#     def check(message):
#         async def msg(message):
#             if isinstance(message.channel, discord.channel.DMChannel):
#                 await bot_info_channel.send("What the fuck")
#                 await message.channel.send("hi")
#                 return True
#         return commands.check(msg)
#         # if isinstance(message.channel, discord.channel.DMChannel):
#         #     try:
#         #         score = float(message.content)
#         #         if score < 0 or score > 10:
#         #             return False
#         #     except ValueError:
#         #         return False
#         #     if message.author.name in remaining:
#         #         remaining.remove(message.author.name)
#         #         scores[message.author.name] = score
#         # if not remaining:
#         #     return True
#         # return False

#     await bot.wait_for("message", check=check)

#     # Finish
#     await bot_info_channel.send("Initial scoring has finished")
#     for k,v in scores.items():
#         await scores_channel.send("**{}**: {:.2f}".format(k, v))

    # # Add data
    # if mode == "final":
    #     sh = utils.sheets.get_sheet(utils.sheets.SHEET)
    #     for p in participants:
    #         row_value = "{}|{:.2f}".format(title, scores[p.name])
    #         utils.sheets.append_csv_to_sheets(sh, row_value, p.name)
    #         with open(utils.csv.CSV_PATH + "/{}.csv".format(p.name.lower()), "a") as f:
    #             f.write(row_value + "\n")


# @bot.command(name="initial-score",
#              brief="Handle the scoring process",
#              description="Run the command to start scoring. The bot will DM you for a response. Unless explicitly given, participants will be taken from whoever is in the General voice channel.",
#              usage="<initial/final> [person1] [person2] ... [personN]")
# async def start_score(ctx, *args):
#     # Args
#     if len(args) == 0:
#         await ctx.send("Usage: !start-score <initial/final>")
#         return
#     elif args[0] not in ["initial", "final"]:
#         await ctx.send("Usage: !start-score <initial/final>")
#         return
#     mode = args[0].lower()

#     # Setup guild and channels
#     guild = utils.discord.get_guild(bot, GUILD)
#     bot_info_channel = utils.discord.get_channel(guild, "bot-info")
#     scores_channel = utils.discord.get_channel(guild, "scores")
#     general_voice_channel = utils.discord.get_channel(guild, "General", voice=True)

#     # Participants
#     if len(args) > 1:
#         participants = []
#         for i in range(1, len(args)):
#             # Validate member
#             member = await utils.discord.get_member(bot_info_channel, args[i])
#             if member:
#                 participants.append(member)

#         if not participants:
#             await bot_info_channel.send("Cannot find participants")
#             return
#     else:
#         participants = general_voice_channel.members

#         if not participants:
#             await bot_info_channel.send(
#                 "Cannot find participants in voice channel. Try !start-score <person1> <person2> ... <personN>")
#             return

#     # Start
#     await bot_info_channel.send("{} scoring has started".format(mode.capitalize()))
#     title, year, chooser = utils.csv.get_next_movie()
#     if mode == "initial":
#         date = datetime.today().strftime("%d/%m/%Y")
#         await scores_channel.send("**{}: {} ({})**".format(date, title, year))
#         sh = utils.sheets.get_sheet(utils.sheets.SHEET)
#         utils.csv.append_movie(title, year, date, chooser)
#         utils.sheets.append_csv_to_sheets(sh, "{}|{}|{}|{}".format(title, year, date, chooser), "Movies")
#     await scores_channel.send("**{}**".format(mode.capitalize()))

#     # Scoring
#     for p in participants:
#         channel = await p.create_dm()
#         await channel.send("Please DM me your {} score".format(args[0]))
#     await bot_info_channel.send("Waiting for everyone to give a score")

#     remaining = [p.name for p in participants]
#     scores = {}
#     def check(message):
#         if isinstance(message.channel, discord.channel.DMChannel):
#             try:
#                 score = float(message.content)
#             except ValueError:
#                 return False
#             if message.author.name in remaining:
#                 remaining.remove(message.author.name)
#                 scores[message.author.name] = score
#         if not remaining:
#             return True
#         return False

#     await bot.wait_for("message", check=check)

#     # Finish
#     await bot_info_channel.send("{} scoring has finished".format(mode.capitalize()))
#     for k,v in scores.items():
#         await scores_channel.send("**{}**: {:.2f}".format(k, v))

#     # Add data
#     if mode == "final":
#         sh = utils.sheets.get_sheet(utils.sheets.SHEET)
#         for p in participants:
#             row_value = "{}|{:.2f}".format(title, scores[p.name])
#             utils.sheets.append_csv_to_sheets(sh, row_value, p.name)
#             with open(utils.csv.CSV_PATH + "/{}.csv".format(p.name.lower()), "a") as f:
#                 f.write(row_value + "\n")

# @bot.command(name="choose-next-movie",
#              brief="Register the next movie",
#              description="Adds the next movie to the database. The bot will help you find the movie unless you add the year to the command.",
#              usage="\"<title>\" [year] <chooser>")
# async def choose_next_movie(ctx, *args):
#     # Setup guild and channels
#     guild = utils.discord.get_guild(bot, GUILD)
#     bot_info_channel = utils.discord.get_channel(guild, "bot-info")

#     # Args
#     if len(args) < 2:
#         await ctx.send("Usage: !choose-next-movie \"<title>\" <chooser>")
#         return
#     if len(args) == 3:
#         member = await utils.discord.get_member(bot_info_channel, args[1])
#         if member:
#             chooser = member.name
#         else:
#             return
#         utils.csv.update_next_movie(args[0], args[1], chooser)
#         return

#     # Validate member
#     member = await utils.discord.get_member(bot_info_channel, args[1])
#     if member:
#         chooser = member.name
#     else:
#         return

#     # Search movie
#     ia = imdb.IMDb()
#     candidates = ia.search_movie(args[0])
#     await bot_info_channel.send("Searching for next movie")
#     await bot_info_channel.send(""Y" to select movie")
#     await bot_info_channel.send(""EXIT" to cancel search")
#     await bot_info_channel.send("Input anything else to continue search")

#     def check(message):
#         if message.channel == ctx.channel:
#             return True
#         return False

#     for c in candidates:
#         if "movie" in c["kind"]:
#             await bot_info_channel.send("Did you mean {}?".format(c["long imdb title"]))
#             msg = await bot.wait_for("message", check=check)
#             if msg.content.upper() == "Y":
#                 utils.csv.update_next_movie(c["title"], c["year"], chooser)
#                 await bot_info_channel.send("Yo we watching {}".format(c["long imdb title"]))
#                 return
#             elif msg.content.upper() == "EXIT":
#                 await bot_info_channel.send("Exiting search")
#                 return

#     await bot_info_channel.send("No movie found, please manually add: !choose-next-movie \"<title>\" <year> <chooser>")


