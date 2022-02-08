import discord
from discord.ext import commands

from config import TOKEN

import re
import time
import random


# ------------------------------------------------------------------------------------------------------------------------------------------------

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot('!', intents=intents)
mod_commands_channel_id = 937852789026070559

infile = open('./name_filter.txt', 'r')
names = infile.read().splitlines()
infile.close()

# ------------------------------------------------------------------------------------------------------------------------------------------------


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_message(message):

    # If message is from this bot, do nothing (bit reduntant due to the next section, but ill keep anyway for safeguarding)
    if message.author == bot.user:
        return

    # If message is from any bot at all, do nothing (for pluralkit users)
    if message.author.bot:
        return

    # 25% the time will check a sent message, and if it could be a valid kid name (by following the letter count conventions) then it will reply saying so
    if random.random() < 0.25 or message.channel.id == 940644970438729768:
        # If the message can be a valid kid name, send a message saying so.
        match = re.search(
            r'(?:\W|^)([a-zA-Z]{4}) ([a-zA-Z]{6,7})(?:\W|$)', message.content)
        if match and match[0].lower() not in names:
            await message.channel.send(f'"{match[0].strip()}" is a valid kid name')

        # If the message can be a valid troll name, send a message saying so.
        match = re.search(
            r'(?:\W|^)([a-zA-Z]{6}) ([a-zA-Z]{6})(?:\W|$)', message.content)
        if match and match[0].lower() not in names:
            await message.channel.send(f'"{match[0].strip()}" is a valid troll name')


# ------------------------------------------------------------------------------------------------------------------------------------------------


bot.run(TOKEN)
