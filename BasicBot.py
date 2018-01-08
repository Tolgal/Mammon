# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform

#custom import modules
import key
import random

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
client = Bot(description="Basic Bot by Habchy#1665", command_prefix="-", pm_help = True)

# This is what happens everytime the bot launches. In this case, it prints information like server count, user count the bot is connected to, and the bot id in the console.
# Do not mess with it because the bot can break, if you wish to do so, please consult me or someone trusted.

@client.event
async def on_ready():
	print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
	print('--------')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
	print('--------')
	print('Use this link to invite {}:'.format(client.user.name))
	print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
	print('--------')
	print('Support Discord Server: https://discord.gg/FNNNgqb')
	print('Github Link: https://github.com/Habchy/BasicBot')
	print('--------')
	print('Created by Habchy#1665')

#Commmand's

# This is a basic example of a call and response command. You tell it do "this" and it does it.
@client.command()
async def ping(*args):

	await client.say(":ping_pong: Pong!")


#Basic "let me google that for you command for the bot
@client.command()
async def google(content):

	await client.say("Let me google that for you...")
	await asyncio.sleep(1)
	await client.say(("https://google.com/search?q=%s&tbm=isch") % (content))

def random_numbers(number, die, addition):
	 #Generates numbers and adds them to each other
	numbers = []
	for i in range(number):
		numbers.append(random.randint(1,die))
	total = sum(numbers)
	string = ', '.join(str(k)for k in numbers)
	answer = 'Result: ' + str(number) + 'D' + str(die)
	if addition != 0:
		total += addition
		string += ', ' + str(addition)
		answer = answer + '+' + str(addition)
	answer =  answer + ' (' + string + ')\nTotal: ' + str(total)
	return answer

#Basic DnD Dice roll
@client.command()
async def roll(dice : str):
	#Rolls a dice in NdN format.
	# Turns everything to lowercase
	die = dice.lower()
	addition = 0
	if '+' in die:
		die, addition = die.split('+')
	try:
		rolls, limit = map(int, die.split('d'))
	except Exception:
		await client.say('Format has to be in NdN!')
		return
   	
    result = random_numbers(rolls, limit, int(addition))
    await client.say(result)
    # result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))


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

# Basic Bot was created by Habchy#1665
# Please join this Discord server if you need help: https://discord.gg/FNNNgqb
# Please modify the parts of the code where it asks you to. Example: The Prefix or The Bot Token
# This is by no means a full bot, it's more of a starter to show you what the python language can do in Discord.
# Thank you for using this and don't forget to star my repo on GitHub! [Repo Link: https://github.com/Habchy/BasicBot]

# The help command is currently set to be Direct Messaged.
# If you would like to change that, change "pm_help = True" to "pm_help = False" on line 9.
