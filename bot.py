import discord
from discord.ext import commands

from shelton import Shelton

class Bot(commands.Bot):
    def __init__(self):
        help_command = commands.DefaultHelpCommand(no_category = "Commands")
        intents = discord.Intents.default()
        intents.members = True
        intents.messages = True
        super().__init__(command_prefix="!", intents=intents, help_command=help_command)

        self.add_cog(Shelton(self))


