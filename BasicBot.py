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
@bot.command(pass_context=True)
async def google(ctx, *, search : str, member: discord.Member = None):
        if member is None:
            member = ctx.message.author.id
        await bot.say('<@{0}>'.format(member) + ' Let me google that for you: ' + ('https://google.com/search?q=%s&tbm=isch') % (search))


#The DnD Roll function
@bot.command(pass_context=True)
async def roll(ctx, *, dice : str, member: discord.Member = None):
    if member is None:
        member = ctx.message.author.id
    nospace_dice = Functions.multireplace(dice, {' ': '', '\n': '', '\r': ''})
    die = nospace_dice.lower()
    dice_list = Functions.multireplace(die, {"+":"," ,"-":",-"})
    dice_list = dice_list.split(',')
    dice_list = list(filter(None, dice_list))
    results = []
    rex = re.compile("^[0-9]+d[0-9]+$")
    for i in dice_list:
        if i.replace("-", "").isdigit() == True:
            results.append([int(i)])
        elif rex.match(i.replace("-", "")):
            if '-' in i:
                i = i.replace('-', '')
                rolls, limit = map(int, i.split('d'))
                temp_list = Functions.random_roll(rolls, limit)
                neg_temp_list = [ -x for x in temp_list]
                results.append(neg_temp_list)
            else:
                rolls, limit = map(int, i.split('d'))
                results.append(Functions.random_roll(rolls, limit))
        else:
            comment = 'This is not the right format: ' + i
            await bot.say(comment)
            return
    total = 0
    for i in results:
        total += sum(i)

    answer = '\n**Result:**'
    for i in range(len(dice_list)):
        if i != range(len(dice_list))[-1]:
            if dice_list[i].replace("-", "").isdigit() == True:
                answer = answer + ' ' + dice_list[i] + ' +'
            else:
                answer = answer + ' ' + dice_list[i] + '(' + ','.join(str(k) for k in results[i]) + ') +'
        else:
            if dice_list[i].replace("-", "").isdigit() == True:
                answer = answer + ' ' + dice_list[i]
            else:
                answer = answer + ' ' + dice_list[i] + '(' + ','.join(str(k) for k in results[i]) + ')'

    answer = answer + '\n**Total**: ' + str(total)
    await bot.say('<@{0}>'.format(member) + answer)


#Rolls 4d6 (keep highest 3) six times
@bot.command(pass_context=True)
async def randchar(ctx, member: discord.Member = None):
	stat_names = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']
	result = ""
	if member is None:
		member = ctx.message.author.id
	for i in stat_names:
		d6 = []
		for j in range(4):
			d6.append(random.randint(1,6))
		sorted_d6 = sorted(d6)
		result += '{0:10} {1}'.format(str(d6), '= **' + str(sum(sorted_d6[1::])) + " **" + i + '\n') 
	await bot.say('<@{0}>'.format(member) + '\n' +  result)


@bot.command()
async def game(*, games : str):
	#Returns a random element from a comma seperated string
	try:
		game_list = games.split('/')
	except Exception:
		await bot.say('Games have to be separated by a "/"')
		return
	random_game = game_list[random.randint(0,len(game_list)-1)]
	await bot.say(random_game)


"""
#test getting the user ID + commands
@bot.command(pass_context=True)
async def test(ctx, *, temp, member: discord.Member = None):
    if member is None:
        member = ctx.message.author.id
    await bot.say('<@{0}>'.format(member))
    await bot.say(str(ctx.message.content))
"""


#start the bot	
bot.run(key.BotKey)

