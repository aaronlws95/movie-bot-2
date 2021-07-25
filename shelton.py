import os
import csv
from datetime import datetime
from enum import Enum

import discord
import gspread
from discord.ext import commands
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials


# Environment
load_dotenv()
CREDENTIALS = os.getenv('GOOGLE_CREDENTIALS')
SHEET_ID = os.getenv('GOOGLESHEET_ID')
GUILD = os.getenv("DISCORD_GUILD")


class Shelton(commands.Cog):
    class State(Enum):
        IDLE = 1
        INITIAL_SCORE = 2
        FINAL_SCORE = 3

    def __init__(self, bot):
        self.bot = bot

        self.guild = None
        self.guild_name = GUILD
        self.channels = {}
        self.participants = []
        self.remaining = []
        self.scores = {}
        self.state = self.State.IDLE
        self.current_date = datetime.today().strftime("%d/%m/%Y")

        with open("data/user_info.csv", "r") as f:
            user_info = list(csv.reader(f))
        self.user_name_map = {}
        for x in user_info:
            self.user_name_map[x[1]] = x[0]

        with open(f"data/next_discussion_info.csv", "r") as f:
            next_discussion_info = list(csv.reader(f))[0]
        self.current_title = next_discussion_info[0]
        self.current_type = next_discussion_info[1]
        self.current_chooser = next_discussion_info[2]

        scope = ["https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive.file",
                "https://www.googleapis.com/auth/drive"]

        credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS + '.json', scope)
        client = gspread.authorize(credentials)
        self.sheet = client.open_by_key(SHEET_ID)


    def is_scoring(self):
        return self.state == self.State.INITIAL_SCORE or self.state == self.State.FINAL_SCORE


    async def populate_participants(self, names=[]):
        if not names:
            self.participants = self.channels["general_voice"].members
            if not self.participants:
                await self.channels["bot-info"].send(f"No one is in the voice channel")
        else:
            for name in names:
                member = discord.utils.get(self.channels["bot-info"].members, name=name)
                if member:
                    self.participants.append(member)
                else:
                    await self.channels["bot-info"].send(f"Who the heck is {name}")
        return


    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = discord.utils.get(self.bot.guilds, name=self.guild_name)
        self.channels["bot-info"] = discord.utils.get(self.guild.channels, name="bot-info")
        self.channels["scores"] =discord.utils.get(self.guild.channels, name="scores")
        self.channels["general_voice"] = discord.utils.get(self.guild.voice_channels, name="General")

        await self.channels["bot-info"].send("I'm back baby")


    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.channel.DMChannel):
            if message.author != self.bot.user:
                if self.is_scoring():
                    try:
                        score = float(message.content)
                    except ValueError:
                        await message.channel.send(f"You need to give me a number")
                        return
                    if score < 0 or score > 10:
                        await message.channel.send("Between 0 and 10 please")
                        return
                    if message.author.name in self.remaining:
                        self.remaining.remove(message.author.name)
                        self.scores[message.author.name] = score

                    if not self.remaining:
                        if self.state == self.State.INITIAL_SCORE:
                            await self.channels["bot-info"].send("Initial scoring has finished")
                        if self.state == self.State.FINAL_SCORE:
                            await self.channels["bot-info"].send("Final scoring has finished")
                            self.sheet.values_append(
                                "Discussions",
                                params={'valueInputOption': 'USER_ENTERED'},
                                body={'values': [[self.current_title, self.current_type, self.current_date, self.current_chooser]]}
                            )
                            with open("data/Discussions.csv", "a") as f:
                                f.write(f"\"{self.current_title}\",{self.current_type},{self.current_date},{self.current_chooser}" + "\n")
                            for p in self.participants:
                                self.sheet.values_append(
                                    self.user_name_map[p.name],
                                    params={'valueInputOption': 'USER_ENTERED'},
                                    body={'values': [[self.current_title, self.scores[p.name]]]}
                                )
                                with open(f"data/user_scores/{self.user_name_map[p.name]}.csv", "a") as f:
                                    f.write(f"\"{self.current_title}\",{self.scores[p.name]:.2f}" + "\n")

                        for k,v in self.scores.items():
                            await self.channels["scores"].send("**{}**: {:.2f}".format(k, v))
                        self.state = self.State.IDLE
                        self.scores = {}


    async def initialize_scoring(self, args, mode="initial"):
        assert mode in ["initial", "final"], "Scoring mode can only be \"initial\| or \"final\""

        if self.is_scoring():
            await self.channels["bot-info"].send("Can you not see that I am already scoring!")
            return

        # Find participants
        await self.populate_participants(list(args))
        if not self.participants:
            await self.channels["bot-info"].send("I can not find anyone")
            return

        # Initialize
        if mode == "initial":
            self.state = self.State.INITIAL_SCORE
        elif mode == "final":
            self.state = self.State.FINAL_SCORE

        if mode == "initial":
            await self.channels["bot-info"].send("wait "*20, tts=True)
        await self.channels["bot-info"].send(f"{mode.capitalize()} scoring has started")

        if mode == "initial":
            await self.channels["scores"].send("**{}: {}**".format(self.current_date, self.current_title))

        await self.channels["scores"].send(f"**{mode.capitalize()}**")

        for p in self.participants:
            channel = await p.create_dm()
            await channel.send(f"What is your {mode} score?")
        await self.channels["bot-info"].send("Waiting for everyone to give a score")

        self.remaining = [p.name for p in self.participants]


    @commands.command(name="initial-score",
                      brief="Handle initial scoring process",
                      description="Run the command to start scoring. The bot will DM you for a response. Unless explicitly given, participants will be taken from whoever is in the General voice channel.",
                      usage="!initial-score [person1] [person2] ... [personN]")
    async def initial_score(self, ctx, *args):
        await self.initialize_scoring(args, "initial")


    @commands.command(name="final-score",
                      brief="Handle final scoring process",
                      description="Run the command to start scoring. The bot will DM you for a response. Unless explicitly given, participants will be taken from whoever is in the General voice channel.",
                      usage="!final-score [person1] [person2] ... [personN]")
    async def final_score(self, ctx, *args):
        await self.initialize_scoring(args, "final")


    @commands.command(name="next",
                      brief="Register the next discussion",
                      description="Register the next discussion",
                      usage="!next \"<title>\" <type> <chooser>")
    async def next(self, ctx, *args):
        if len(args) != 3:
            await self.channels["bot-info"].send("It is !next \"<title>\" <type> <chooser>")
            return
        with open("data/next_discussion_info.csv", "w") as f:
            f.write(f"\"{args[0]}\",{args[1]},{args[2]}")

        await self.channels["bot-info"].send(f"Yooo, we {args[1]}ing {args[0]} next")


    @commands.command(name="shutdown",
                      brief="Shut the bot down",
                      description="Shuts the bot down.")
    @commands.is_owner()
    async def shutdown(self, ctx):
        await self.channels["bot-info"].send("Bye bye")
        await self.bot.logout()