#Import basic Discord modules
import discord
import asyncio
import platform

from discord.ext import commands

#Import Google API stuff
import httplib2
import os
import Google

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

#Import custom modules
import key
import random
import Functions
import re


directories = ['Data', 'Data\\rps']
files = ['Data\\allowed_users']
bot_dev_role_ids = {'Admin':'400573127412678656', 'Bot':'399325522313609217', 'Developer':'399325464855969796'}
delete_commands = ('-google', '-roll', '-randchar')
host_dict = {} #Creates the dictionary for the host messages.

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
bot = commands.Bot(command_prefix="-", description="4LAN basic Bot", pm_help = True, help_attrs=dict(hidden=True,brief="This is just the help function"))

# This is what happens everytime the bot launches. In this case, it prints information like server count, user count the bot is connected to, and the bot id in the console.
@bot.event
async def on_ready():
	print('Logged in as '+bot.user.name+' (ID:'+bot.user.id+') | Connected to '+str(len(bot.servers))+' servers | Connected to '+str(len(set(bot.get_all_members())))+' users')
	print('--------')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
	print('--------')
	print('Use this link to invite {}:'.format(bot.user.name))
	print('https://discordapp.com/oauth2/authorize?bot_id={}&scope=bot&permissions=8'.format(bot.user.id))
	await bot.change_presence(game=discord.Game(name="Say -help Tolgal is evil!"))
	Functions.create_dirs(directories)
	Functions.create_files(files)
	Functions.create_server_dict(bot.servers)


"""Commmand's"""

#Automatically removes commands given to bot
@bot.event
async def on_message(message):
	if message.author.bot:
		return
	if message.content.startswith(delete_commands):
		try:
			await bot.delete_message(message)
		except:
			pass
	# global allowed
	allowed, check = Functions.check_allowed(message)
	if allowed:
		Functions.write_file('Data\\allowed_users', [allowed])
		try:
			await bot.delete_message(message)
		except:
			pass
		await bot.send_message(message.channel, '{} As my loyal servant you may now use my services'.format(message.author.mention))
	if check == False:
		try:
			await bot.delete_message(message)
		except:
			pass
		await bot.send_message(message.channel, '{} You have no power here.'.format(message.author.mention))
		return
	await bot.process_commands(message)


# ping > pong
@bot.command(brief='Play PingPong with Mammon')
async def ping(*args):
	"""Play PingPong with Mammon. Bot returns :ping_pong: Pong!"""
	await bot.say(":ping_pong: Pong!")


#Basic "let me google that for you" command for the bot
@bot.command(pass_context=True, brief='Google something')
async def google(ctx, *, search : str, member: discord.Member = None):
	"""
	Google something
	"""
	if member is None:
		member = ctx.message.author.mention
	await bot.say('{0}\nLet me google that for you:\n'.format(member) + ('https://google.com/search?q=%s&tbm=isch') % (search))


#The DnD Roll function
@bot.command(pass_context=True, brief='Roll dice')
async def roll(ctx, *, dice : str, member: discord.Member = None):
	"""
	Roll dice
	"""
	if member is None:
		member = ctx.message.author.mention
	## Clean up string and convert to list
	dice_list = Functions.cleanup_roll(dice)
	# loop through all elements in dice_list and if its an int put it as a list in results
	# or if in format NdN send to function for list of random numbers and put in results
	# if not in right format comment will be sent and function is stopped
	results = []
	rex = re.compile("^[0-9]+d[0-9]+$")
	for i in dice_list:
		if i.replace("-", "").isdigit() == True:
			results.append([int(i)])
		elif rex.match(i.replace("-", "")):
			results.append(Functions.create_die(i))
		else:
			comment = 'This is not the right format: ' + i
			await bot.say(comment)
			return
	# Calculate sum of all numbers in results and formulate answer string
	# Formulate answer string
	answer = Functions.create_roll_answer(dice_list, results)
	await bot.say('{0}{1}'.format(member, answer))


#Rolls 4d6 (keep highest 3) six times
@bot.command(pass_context=True, brief='Create random stats for character')
async def randchar(ctx, member: discord.Member = None):
	"""
	Create random stats for character
	"""
	stat_names = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']
	result = ""
	if member is None:
		member = ctx.message.author.mention
	for i in stat_names:
		d6 = []
		for j in range(4):
			d6.append(random.randint(1,6))
		sorted_d6 = sorted(d6)
		result += '{0:10} {1}'.format(str(d6), '= **' + str(sum(sorted_d6[1::])) + " **" + i + '\n') 
	await bot.say('{0}\n{1}'.format(member, result))


@bot.command(pass_context = True, brief='Chooses one thing at random')
async def choose(ctx, *, choices : str, member : discord.Member = None):
	"""
	Returns a random element from a backwards slash seperated string
	"""
	if member is None:
		member = ctx.message.author.mention
	try:
		choice_list = choices.split('/')
	except Exception:
		await bot.say('Choices have to be separated by a "/"')
		return
	random_choice = random.choice(choice_list)
	message = "After much deliberating between the options (**" + ', '.join(choice_list) + \
		'**) it has been decided **' + random_choice + '** is the best.'
	await bot.say('{0}\n{1}'.format(member, message))



@bot.command(pass_context = True, brief='Returns lmgtfy link with mention')
async def lmgtfy(ctx, *, search : str, member : discord.Member = None):
	"""
	Returns lmgtfy link with mention
	"""
	search, member = Functions.check_mention(search)
	if member is None:
		member = ctx.message.author.mention
	search = search.replace(' ', '+')
	await bot.say('{0}\nhttps://lmgtfy.com/?q={1}'.format(member, search))


#Mentions an user using name
@bot.command(pass_context=True, brief='Mentions user')
async def pinguser(ctx, *, pu_name : str):
	"""
	Mentions user
	"""
	user = discord.Server.get_member_named(ctx.message.server, pu_name)
	if user is not None:
		user_id = user.mention
		await bot.say(user_id)
	else:
		await bot.say("User not found.")


@bot.command(pass_context=True, hidden = True)
async def test(ctx, roles: discord.Member.roles = None):
	if roles is None:
		roles = ctx.message.author.roles
	if bot_dev_role_ids.get('Developer') in [y.id for y in roles]:
		await bot.say('You have permission to use this command')
	else:
		await bot.say('You don\'t have permission to use this command')


"""
#test getting the user ID + commands
@bot.command(pass_context=True)
async def test(ctx, *, temp, member: discord.Member = None):
	if member is None:
		member = ctx.message.author.id
	await bot.say('<@{0}>'.format(member))
	await bot.say(str(ctx.message.content))
"""


#Allows members to broadcast their interest to start a mission with other players, so that it is posted in a dedicated channel. Optional: ping a specific 'looking for games' role, display time since message was posted. 
@bot.command(pass_context=True, brief='Allows an user to set up a mission in the #mission-sandbox channel')
async def host_mission(ctx, *, host_message : str, member : discord.Member = None):
	"""
	Type "!host_mission [message]" to display the message in #mission-sandbox. Use !stop_hosting to remove the message.
	"""
	#await bot.send_message(discord.Object(id='404410215564312576'),  '**Mission Board:**') #Use this to make an initial message
	final_message = ''
	global host_dict
	if member is None:
		member = ctx.message.author
	if member.id in host_dict:
		del host_dict[member.id]
	host_dict[member.id] = '**{0}:** {1}'.format(member.display_name, host_message)
	final_message = Functions.edit_host_message(host_dict)
	await bot.edit_message(await bot.get_message(bot.get_channel('404410215564312576'), '404426711577526293'), final_message)


#Allows members to stop broadcasting their mission
@bot.command(pass_context=True, brief='Deletes your current host message')
async def stop_hosting(ctx, *, member : discord.Member = None):
	"""
	Deletes your current !host_mission message in #mission-sandbox
	"""
	final_message = ''
	global host_dict
	if member is None:
		member = ctx.message.author
	if member.id in host_dict:
		del(host_dict[member.id])
		final_message = Functions.edit_host_message(host_dict)
		await bot.edit_message(await bot.get_message(bot.get_channel('404410215564312576'), '404426711577526293'), final_message)
	else:
		await bot.say('{0} is not hosting a mission'.format(member.display_name))


@bot.command(pass_context=True)
async def rps(ctx, *, pchoice:str):
	"""
	Play rock, paper, scissors against Mammon
	"""
	users = []
	stats = Functions.open_file('Data\\rps')
	stats = [x.strip() for x in stats]
	stats = [x.split(',') for x in stats]
	for user in stats[1:]:
		users.append(user[0])
	print(stats)
	if ctx.message.author.id not in users:
		stats.append([ctx.message.author.id,'0','0','0','0','0'])
	for stat in stats:
		if stat[0] == ctx.message.author.id:
			user_stats = stat
			index = stats.index(stat)
	member = ctx.message.author.mention
	rpsdict = {'rock':'scissors', 'paper':'rock', 'scissors':'paper'}
	bchoice = random.choice(['rock', 'paper', 'scissors'])
	answer = '\n{0} chose: {1}\n{2} chose: {3}\n'.format(member, pchoice, bot.user.mention, bchoice)
	try:
		if bchoice == pchoice.lower():
			await bot.say(answer + '**It\'s a tie**')
			user_stats[2] = str(int(user_stats[2])+ 1)
			user_stats[5] = '0'
		elif rpsdict[pchoice.lower()] == bchoice:
			await bot.say(answer + '**You won :frowning:**')
			user_stats[1] = str(int(user_stats[1])+ 1)
			user_stats[5] = str(int(user_stats[5])+ 1)
			if int(user_stats[5]) > int(user_stats[4]):
				user_stats[4] = user_stats[5]
		elif rpsdict[bchoice.lower()] == pchoice:
			await bot.say(answer + '**I won :smile:**')
			user_stats[3] = str(int(user_stats[3])+ 1)
			user_stats[5] = '0'
		else:
			await bot.say('{0} Something went wrong'.format(member))
		stats[index] = stat
		stats = [','.join(x) for x in stats]
		Functions.write_file('Data\\rps', stats)
	except:
		print('exception')


#start the bot	
bot.run(key.BotKey)

