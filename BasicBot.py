# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio
from discord.ext import commands
import platform

#custom import modules
import key
import random
import Functions

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
bot = commands.Bot(command_prefix="-", description="4LAN basic Bot", pm_help = True)

# This is what happens everytime the bot launches. In this case, it prints information like server count, user count the bot is connected to, and the bot id in the console.

@bot.event
async def on_ready():
	print('Logged in as '+bot.user.name+' (ID:'+bot.user.id+') | Connected to '+str(len(bot.servers))+' servers | Connected to '+str(len(set(bot.get_all_members())))+' users')
	print('--------')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
	print('--------')
	print('Use this link to invite {}:'.format(bot.user.name))
	print('https://discordapp.com/oauth2/authorize?bot_id={}&scope=bot&permissions=8'.format(bot.user.id))


"""Commmand's"""

# ping > pong
@bot.command()
async def ping(*args):

	await bot.say(":ping_pong: Pong!")

#Basic "let me google that for you command for the bot
@bot.command()
async def google(search):

	await bot.say("Let me google that for you...")
	await asyncio.sleep(1)
	await bot.say(("https://google.com/search?q=%s&tbm=isch") % (search))

#Basic DnD Dice roll
@bot.command()
async def roll(dice : str):
    nospace_dice = dice.replace(' ', '')
    die = nospace_dice.lower()
    addition = 0
    if '+' in die:
        die, addition = die.split('+')
    elif '-' in die:
        die, addition = die.split('-')
        addition = '-' + addition
    try:
        rolls, limit = map(int, die.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return
    answer = Functions.random_numbers(rolls, limit, int(addition))
    await bot.say(answer)

@bot.command()
async def game(games : str):
	#Returns a random element from a comma seperated string
	try:
		game_list = games.split('/')
	except Exception:
		await bot.say('Games have to be separated by a "/"')
		return
	random_game = game_list[random.randint(-1,len(game_list)-1)]
	await bot.say(random_game)


@bot.command(pass_context=True)
async def test(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author.id

    await bot.say('<@{0}> Hello'.format(member))

#start the bot	
bot.run(key.BotKey)

