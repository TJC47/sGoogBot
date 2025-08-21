import discord
from discord import app_commands
from discord.ext import commands
import requests
import time
import random
import discord
from io import StringIO
from contextlib import redirect_stdout
import logging
import asyncio

logger = logging.getLogger("googbot.goog")


class Goog(commands.Cog):
    def __init__(self, bot: commands.Bot) :
        self.bot = bot

    @app_commands.command(description = "goog")
    @app_commands.allowed_installs(guilds = True, users = True)
    @app_commands.allowed_contexts(guilds = True, dms = True, private_channels = True)
    async def goog(self, interaction: discord.Interaction):
        await interaction.response.send_message(content = "goog")


async def setup(bot: commands.Bot):
    await bot.add_cog(Goog(bot))
