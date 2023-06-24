from loader import BotLoader
from dotenv import load_dotenv
import logging
import discord
import os

load_dotenv("credentials.env")
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s - %(name)s] %(message)s")
logging.getLogger("discord").setLevel(logging.WARNING)

bot = BotLoader(case_insensitive=True, max_messages=None,
                intents=discord.Intents.all(), help_command=None)
bot.run(os.environ["TOKEN"])
