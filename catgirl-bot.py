import discord
from discord.ext import commands

from config import TOKEN
import homestuck

# ------------------------------------------------------------------------------------------------------------------------------------------------

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot('!', intents=intents)

mod_commands_channel_id = 937852789026070559
valid_name_channel_id = 940644970438729768
spam_channel_id = 937497124734660699

# ------------------------------------------------------------------------------------------------------------------------------------------------

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

    await homestuck.test()

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="with BLÅHAJ"))

@bot.event
async def on_message(message):

    # If message is from this bot, do nothing (bit reduntant due to the line after, but kept for safeguarding)
    if message.author == bot.user:
        return

    # If message is from any bot at all, do nothing (mostly for pluralkit users)
    if message.author.bot:
        return

    # If message is anywhere outside the test channel, do nothing (for testing purposes)
    if not (message.channel.id == mod_commands_channel_id): #or message.channel.id == spam_channel_id):
        return

    homestuck_name_reply = await homestuck.name_check(message.content)
    if homestuck_name_reply: await message.channel.send(homestuck_name_reply)

# ------------------------------------------------------------------------------------------------------------------------------------------------

bot.run(TOKEN)
