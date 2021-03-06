import discord
from discord.ext import commands

 #bot token
token = ''

intents = discord.Intents.all()
permissions_ = discord.Permissions.all()

bot = commands.Bot(
	command_prefix = '$',
	case_insensitive = True,
	intents = intents
)

@bot.event
async def on_ready():
	print('online')

@bot.command(name = 'ping', hidden = True)
async def send_ping(ctx):
	'''
	Sends a ping 
	'''
	return await ctx.send(
		'pong {emo_} \n{latency}ms'.format(
			emo_ = '\N{Table Tennis Paddle and Ball}',
			latency = str(bot.latency)[2:5]
		)
	)

@bot.command(name = 'shutdown', hidden = True)
async def turn_off_bot(ctx):
	'''
	Shutdown the bot
	'''
	await ctx.send('Going offline in a minute \nSee ya !')
	return await bot.close()

extensions = [
	'cogs.managecogs',
	'cogs.dark',
	'cogs.memeApi',
	'cogs.test'
]

if __name__ == '__main__':
	for extension in extensions:
		bot.load_extension(extension)

bot.run(token)
