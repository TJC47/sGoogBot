import requests
import time
import random
import discord
from discord.ext import commands
from discord import app_commands
from discord.ext import tasks
import asyncio
import hashlib
import base64
from enum import Enum
import sys
import json

import logging
from LEBlogger import init
import os
import threading
import code


init(10)
logger = logging.getLogger("googbot.main")


RESET = "\033[0m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[36m"
GRAY = "\033[90m"
MAGENTA = "\033[35m"

f = open("token.sensitive")
TOKEN = f.readline()
f.close()



class MyClient(commands.Bot):


    def __init__(self,intents: discord.Intents):
        super().__init__(
        command_prefix='sg!',
        intents=discord.Intents.all(),
        activity=discord.CustomActivity(name='Goog...'),
        allowed_contexts=app_commands.AppCommandContext(guild=True, dm_channel=True, private_channel=True),
        allowed_installs=app_commands.AppInstallationType(guild=True, user=True),
        help_command=None)
    async def setup_hook(self):

        with open("cogs.json", "r") as f:
            cogfile = json.loads(f.read())
        for cogname in cogfile["active_cogs"]:
            logger.info(f"Loading extension '{cogname}'")
            await self.load_extension(cogname)
        logger.info("Loaded all extensions")





    async def on_message(self, message):
        global model
        if message.author == self.user:
            return
        is_owner = await self.is_owner(message.author)
        if message.content == "sgb!ereload" and is_owner:
            logtext = f"{YELLOW}Reloading all extensions...{RESET}"
            logmessage = await message.channel.send(content=f"```ansi\n{logtext}```")
            with open("cogs.json", "r") as f:
                cogfile = json.loads(f.read())
            for cogname in cogfile["active_cogs"]:
                await self.reload_extension(cogname)
                logtext = logtext + f"\n{CYAN}Reloaded extension '{GREEN}{cogname}{CYAN}'!{RESET}"
                await logmessage.edit(content=f"```ansi\n{logtext}```")
            logtext = logtext + f"""\n{GREEN}Reloaded {YELLOW}{len(cogfile["active_cogs"])}{GREEN} extensions!{RESET}"""
            await logmessage.edit(content=f"```ansi\n{logtext}```")

        if message.content == "sgb!synctree" and is_owner: 
            await self.tree.sync()
            await message.channel.send("googed the goog tree")


intents = discord.Intents.all()
client = MyClient(intents=intents)




@client.tree.command(description="reload all extensions")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def reload_extensions(interaction: discord.Interaction):
            is_owner = await client.is_owner(interaction.user)
            if is_owner:
                await interaction.response.send_message("Reloading all extensions...")
                logger.debug("Reloading all extensions, triggered by owner")
                with open("cogs.json", "r") as f:
                    cogfile = json.loads(f.read())
                for cogname in cogfile["active_cogs"]:
                    await client.reload_extension(cogname)
                    logger.info(f"Reloaded cog '{cogname}'!")

                await interaction.edit_original_response(content=f"""Reloaded all {len(cogfile["active_cogs"])} extensions!""")
            else:
                await interaction.response.send_message("nuh uh")

@client.tree.command(description="restart bot")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def restart_bot(interaction: discord.Interaction):
            is_owner = await client.is_owner(interaction.user)
            if is_owner:
                logger.warning("Manual restart triggered.")
                await interaction.response.send_message("bai bai")
                os.execvp("python", ["python", "main.py"])
            else:
                await interaction.response.send_message("nuh uh")

reset = "\x1b[0m"

b = [
  '\033[38;2;127;0;255m', 
  '\033[38;2;140;0;255m', 
  '\033[38;2;150;0;255m', 
  '\033[38;2;164;0;255m', 
  '\033[38;2;176;0;255m', 
  '\033[38;2;201;0;255m',
  '\033[38;2;213;0;255m',
  '\033[38;2;225;0;255m'
]

goog = f"""
                      __     __                  __               
.-----..-----..-----.|  |--.|__|.---.-..-----.  |  |.-----..--.--.
|__ --||  -__||__ --||  _  ||  ||  _  ||     |  |  ||  -__||_   _|
|_____||_____||_____||_____||__||___._||__|__|  |__||_____||__.__|
       A "better" GoogBot. With "cleaner" code. (Blatant stjbot ripoff i know i know)
"""
print(goog)
logger.debug(f"if this text is colored your terminal supports truecolor -> {b[0]}meow{reset}")
logger.debug(f"Current TERM variable -> {os.environ['TERM']}")


def start_console(local_vars=None):
  banner = ""
  logger.debug("Interactive Python Console is Active. Ctrl+D to exit.")
  # import rlcompleter
  import readline
  code.interact(banner=banner, local=local_vars or globals())

def restart():
  logger.warning("Manual restart triggered.")
  os.execvp("python", ["python", "main.py"])

async def reload_cogs_as():
    logger.info("Reloading all cogs...")
    with open("cogs.json", "r") as f:
        cogfile = json.loads(f.read())
    for cogname in cogfile["active_cogs"]:
        await client.reload_extension(cogname)
        logger.info(f"Reloaded cog '{cogname}'!")
    logger.info(f"""Reloaded all {len(cogfile["active_cogs"])} cogs!""")

def reload_cogs():
    asyncio.run(reload_cogs_as())

threading.Thread(target=start_console, args=(locals(),), daemon=True).start()

client.run(TOKEN)