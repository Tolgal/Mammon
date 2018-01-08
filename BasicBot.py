# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio
from discord.ext.commands import Bot
import platform

#custom import modules
import key
import random
import Functions

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
client = Bot(description="4LAN basic Bot", command_prefix="-", pm_help = False)

# This is what happens everytime the bot launches. In this case, it prints information like server count, user count the bot is connected to, and the bot id in the console.

@client.event
async def on_ready():
	print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
	print('--------')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
	print('--------')
	print('Use this link to invite {}:'.format(client.user.name))
	print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))


"""Commmand's"""

# ping > pong
@client.command()
async def ping(*args):

	await client.say(":ping_pong: Pong!")

#Basic "let me google that for you command for the bot
@client.command()
async def google(search):

	await client.say("Let me google that for you...")
	await asyncio.sleep(1)
	await client.say(("https://google.com/search?q=%s&tbm=isch") % (search))

#Basic DnD Dice roll
@client.command()
async def roll(dice : str):
    die = dice.lower()
    addition = 0
    if '+' in die:
        die, addition = die.split('+')
    try:
        rolls, limit = map(int, die.split('d'))
    except Exception:
        await client.say('Format has to be in NdN!')
        return
    answer = Functions.random_numbers(rolls, limit, int(addition))
    await client.say(answer)

@client.command()
async def game(games : str):
	#Returns a random element from a comma seperated string
	try:
		game_list = games.split('/')
	except Exception:
		await client.say('Games have to be separated by a "/"')
		return
	random_game = game_list[random.randint(-1,len(game_list)-1)]
	await client.say(random_game)


#start the bot	
client.run(key.BotKey)

