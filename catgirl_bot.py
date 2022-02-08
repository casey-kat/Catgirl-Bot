import discord
from discord.ext import commands
import re
import time
from config import TOKEN

# ------------------------------------------------------------------------------------------------------------------------------------------------

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot('!', intents=intents)
mod_commands_channel_id = 937852789026070559

infile = open('./name_filter.txt', 'r')
names = infile.read().splitlines()
infile.close()

flirt_ban_limit = 200

# ------------------------------------------------------------------------------------------------------------------------------------------------


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_message(message):

    # If message is from this bot, do nothing (bit reduntant due to the next section)
    if message.author == bot.user:
        return

    # -------------------------------------------------------------------------------------

    # If message is from any bot at all, do nothing (for pluralkit users)
    if message.author.bot:
        return

    # Will check a sent message, and if it could be a valid kid name (by following the letter count conventions) then it will reply saying so
    # If the message can be a valid kid name, send a message saying so.
    match = re.match(r'[a-zA-Z]{4} [a-zA-Z]{6,7}$', message.content)
    if match and match[0].lower() not in names:
        await message.channel.send(f'"{match[0]}" is a valid kid name.')

    # If the message can be a valid troll name, send a message saying so.
    match = re.match(r'[a-zA-Z]{6} [a-zA-Z]{6}$', message.content)
    if match and match[0].lower() not in names:
        await message.channel.send(f'"{match[0]}" is a valid troll name.')

    # -------------------------------------------------------------------------------------

    # If message is outside the mod-commands channel, return
    if message.channel.id != mod_commands_channel_id:
        return

    # -------------------------------------------------------------------------------------


# When a new member joins, send the result of flirt_ban_warning to the mod_commands channel
@bot.event
async def on_member_join(_):
    channel = bot.get_channel(mod_commands_channel_id)
    await channel.send(flirt_ban_warning(channel))


# When a member leaves, send the result of flirt_ban_warning to the mod_commands channel
@bot.event
async def on_member_leave(_):
    channel = bot.get_channel(mod_commands_channel_id)
    await channel.send(flirt_ban_warning(channel))


# When the command is inputted by a mod, send the result of flirt_ban_warning
@bot.slash_command()
@commands.has_role("mod")
async def members_till_flirting_ban(channel):
    await channel.respond(flirt_ban_warning(channel))


# ------------------------------------------------------------------------------------------------------------------------------------------------


# Prints the time, and also the amount of members that must join for the count to reach flirt_ban_limit
async def flirt_ban_warning(channel) -> str:
    members_till_ban = flirt_ban_limit - channel.guild.member_count
    return f"It is currently <t:{int(time.time())}> in your timezone. We are {members_till_ban} members away from the ban on flirting."


# ------------------------------------------------------------------------------------------------------------------------------------------------


bot.run(TOKEN)
