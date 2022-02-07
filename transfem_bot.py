import discord
from discord.ext import commands
from datetime import datetime
from config import TOKEN


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot('!', intents=intents)
mod_commands_channel = bot.get_channel(937852789026070559)

infile = open('./name_filter.txt', 'r')
names = infile.read().splitlines()
infile.close()

flirt_ban_limit = 200


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_message(message):
    # if message is from this bot, do nothing
    if message.author == bot.user:
        return

    # if message is outside mod-commands, do nothing
    # if message.channel.id != mod_commands_channel.id:
    #    return

    # homestuck names
    words = message.content.split(' ')
    if len(words) == 2:

        if len(words[0]) == 4 and (len(words[1]) == 6 or len(words[1]) == 7):
            if message.content.lower() in names:
                return
            await message.channel.send(f'"{words[0]} {words[1]}" is a valid kid name.')

        if len(words[0]) == 6 and len(words[1]) == 6:
            if message.content.lower() in names:
                return
            await message.channel.send(f'"{words[0]} {words[1]}" is a valid troll name.')


# send mods the flirting ban countdown whenever someone joins
@bot.event
async def on_member_join(member):
    await mod_commands_channel.send(flirt_ban_warning(mod_commands_channel))


# send mods the flirting ban countdown whenever someone leaves
@bot.event
async def on_member_leave(member):
    await mod_commands_channel.send(flirt_ban_warning(mod_commands_channel))


# see current flirting ban countdown       guild_ids=[937495559063896134]
@bot.slash_command()
@commands.has_role("mod")
async def members_till_flirting_ban(channel):
    await channel.respond(flirt_ban_warning(channel))


def flirt_ban_warning(channel) -> str:
    time = datetime.now().strftime("%H:%M:%S")
    date = datetime.today().strftime("%B %d, %Y")
    members_till_ban = flirt_ban_limit - channel.guild.member_count
    return f"`It is {time} on {date.upper()} at UTC: we are {members_till_ban} members away from the ban on flirting.`"


bot.run(TOKEN)

# py -3 transfem_bot.py
