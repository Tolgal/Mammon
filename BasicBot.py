# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio
from discord.ext import commands
import platform

#custom import modules
import key
import random
import Functions
import re

bot_dev_role_ids = {'Admin':'400573127412678656', 'Bot':'399325522313609217', 'Developer':'399325464855969796'}
delete_commands = ('-google', '-roll', '-randchar')
host_dict = {} #Creates the dictionary for the host messages.

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
	await bot.change_presence(game=discord.Game(name="Say -help Tolgal is evil!"))
	Functions.create_server_dict(bot.servers)


"""Commmand's"""

#Automatically removes commands given to bot
@bot.event
async def on_message(message):
    if message.content.startswith(delete_commands):
        try:
            await bot.delete_message(message)
        except:
            pass
    await bot.process_commands(message)


# ping > pong
@bot.command(brief='Play PingPong with Mammon', description='Play PingPong with Mammon. Bot returns :ping_pong: Pong!')
async def ping(*args):

	await bot.say(":ping_pong: Pong!")


#Basic "let me google that for you" command for the bot
@bot.command(pass_context=True)
async def google(ctx, *, search : str, member: discord.Member = None):
        if member is None:
            member = ctx.message.author.mention
        await bot.say('{0}\nLet me google that for you:\n'.format(member) + ('https://google.com/search?q=%s&tbm=isch') % (search))


#The DnD Roll function
@bot.command(pass_context=True)
async def roll(ctx, *, dice : str, member: discord.Member = None):
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
@bot.command(pass_context=True)
async def randchar(ctx, member: discord.Member = None):
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


@bot.command(pass_context = True)
async def choose(ctx, *, choices : str, member : discord.Member = None):
	#Returns a random element from a backwards slash seperated string
    if member is None:
        member = ctx.message.author.mention
    try:
        choice_list = choices.split('/')
    except Exception:
        await bot.say('Choices have to be separated by a "/"')
        return
    random_choice = choice_list[random.randint(0,len(choice_list)-1)]
    message = "After much deliberating between the options (**" + ', '.join(choice_list) + \
        '**) it has been decided **' + random_choice + '** is the best.'
    await bot.say('{0}\n{1}'.format(member, message))



@bot.command(pass_context = True)
async def lmgtfy(ctx, *, search : str, member : discord.Member = None):
    search, member = Functions.check_mention(search)
    if member is None:
        member = ctx.message.author.mention
    search = search.replace(' ', '+')
    await bot.say('{0}\nhttps://lmgtfy.com/?q={1}'.format(member, search))


#Mentions an user using name
@bot.command(pass_context=True)
async def pinguser(ctx, *, pu_name : str):
	user = discord.Server.get_member_named(ctx.message.server, pu_name)
	if user is not None:
		user_id = user.mention
		await bot.say(user_id)
	else:
		await bot.say("User not found.")


@bot.command(pass_context=True)
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
@bot.command(pass_context=True)
async def host_mission(ctx, *, host_message : str, member : discord.Member = None):
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
@bot.command(pass_context=True)
async def stop_hosting(ctx, *, member : discord.Member = None):
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


#start the bot	
bot.run(key.BotKey)

