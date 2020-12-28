import discord
from discord.ext import commands
import darkmemer
from players import playerData
from market import market
import random

class playDarkMemer(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.dank = None

	def playerExistance(self):
		async def predicate(ctx):
			res = playerData.playerExist(
				ctx.author.id, ctx.author.name,
				ctx.author.discriminator, ctx.author.nick
			)
			return res
		return commands.check(predicate)

	@commands.command(name = 'start')
	async def startGame(self, ctx, name, nick):
		'''
		starts game for new player
		'''
		makeplayer = playerData()
		addPlayer = makeplayer.addNewPlayer(
			ctx.author.id, ctx.author.name,
			ctx.author.discriminator, ctx.author.nick
		)
		if addPlayer:
			return await ctx.send('{p}, you started game !'.format(p = ctx.author))
		return await ctx.send('{p}, you already started game !'.format(p = ctx.author))
	
	@commands.command(name = 'work')
	@commands.check(playerExistance)
	@commands.cooldown(rate = 1, per = 10.0, type = commands.BucketType.member)
	async def doSomeWork(self, ctx):
		'''
		work to get money
		'''
		self.dank = darkmemer.life(ctx.author.id, ctx.author.name, ctx.author.nick, ctx.author.discriminator)
		amount = random.randint(150, 1100)
		worked = self.dank.person.addMoney(amount)
		embed_ = discord.Embed(
			description = '{player_}, you worked !'.format(player_ = ctx.author),
			colour = discord.Colour.red()
		)
		if worked:
			return await ctx.send(embed = embed_)
		return await ctx.send('Something went wrong {player_} !'.format(player_ = ctx.author.mention))

	@commands.command(name = 'profile', aliases = ['info', 'p'])
	@commands.check(playerExistance)
	async def getProfile(self, ctx):
		'''
		returns the player profile
		'''
		self.dank = darkmemer.life(ctx.author.id, ctx.author.name, ctx.author.nick, ctx.author.discriminator)
		embed1 = discord.Embed(
			title = 'Profile',
			description = self.dank.person.profile(),
			colour = discord.Colour.blue()
		)
		embed1.set_thumbnail(url = ctx.author.avatar_url)
		return await ctx.send(embed = embed1)

	@commands.command(name = 'withdraw', aliases = ['with'])
	@commands.check(playerExistance)
	async def withdrawMoney(self, ctx, money: int):
		'''
		withdraw money
		'''
		self.dank = darkmemer.life(ctx.author.id, ctx.author.name, ctx.author.nick, ctx.author.discriminator)
		var = self.dank.person.withdraw(money)
		if var:
			return await ctx.send('**{amount}** coins withdrawn !'.format(amount = str(money)))
		return await ctx.send('Not enough money !')
	
	@commands.command(name = 'deposit', aliases = ['dep'])
	@commands.check(playerExistance)
	async def depositMoney(self, ctx, money: int):
		'''
		deposit money
		'''
		self.dank = darkmemer.life(ctx.author.id, ctx.author.name, ctx.author.nick, ctx.author.discriminator)
		var = self.dank.person.deposit(money)
		if var:
			return await ctx.send('**{amount}** coins deposited!'.format(amount = str(money)))
		return await ctx.send('Not enough money !')
	
	@commands.command(name = 'balance', aliases = ['bal'])
	@commands.check(playerExistance)
	async def playerNetBalance(self, ctx):
		'''
		returns the balance of player
		'''
		self.dank = darkmemer.life(ctx.author.id, ctx.author.name, ctx.author.nick, ctx.author.discriminator)
		embed_ = discord.Embed(
			title = '{player}\'s Balance'.format(player = ctx.author.name),
			description = 'Total : {total} \nWallet : Rs.{wallet} \nBank : Rs.{bank}'.format(
				total = str(self.dank.person.netBalance()),
				wallet = str(self.dank.person.playerWallet()),
				bank = str(self.dank.person.playerBank())
			),
			colour = discord.Colour.dark_green()
		)
		if self.dank:
			return await ctx.send(embed = embed_)
	
	@commands.command(name = 'inventory', aliases = ['inv'])
	@commands.check(playerExistance)
	async def playerInventory(self, ctx):
		'''
		returns the inventory of player
		'''
		self.dank = darkmemer.life(ctx.author.id, ctx.author.name, ctx.author.nick, ctx.author.discriminator)
		items = self.dank.person.inventory()
		print(items)
		inventory_ = '(Items, Price, Quantity)\n'
		for item in items:
			inventory_ += item
			inventory_ += ' '
			inventory_ += str(items[item][0])
			inventory_ += ' '
			inventory_ += str(items[item][1])
			inventory_ += '\n'
		print(inventory_)
		embed_ = discord.Embed(
			title = '{player}\'s Inventory'.format(player = ctx.author.name),
			description = inventory_,
			colour = discord.Colour.teal()
		)
		embed_.set_thumbnail(url = ctx.author.avatar_url)
		if self.dank:
			return await ctx.send(embed = embed_)
	
	@commands.command(name = 'market')
	@commands.check(playerExistance)
	async def globalMarketList(self, ctx):
		'''
		returns the market item list
		'''
		market_ = market()
		listItems = market_.marketItems()
		items_ = '(Items, Price)\n'
		for item in listItems:
			items_ += item[1]
			items_ += ' '
			items_ += str(item[2])
			items_ += '\n'
		embed2 = discord.Embed(
			title = 'Market',
			description = items_,
			colour = discord.Colour.red()
		)
		return await ctx.send(embed = embed2)
	
	@commands.command(name = 'buy', aliases = ['shop'])
	@commands.check(playerExistance)
	async def buyItems(self, ctx, itemName: str, quantity: int):
		'''
		buy items
		'''
		self.dank = darkmemer.life(ctx.author.id, ctx.author.name, ctx.author.nick, ctx.author.discriminator)
		buy = self.dank.person.buyItem(itemName, quantity)
		if buy:
			return await ctx.send('{player}, you bought this item !'.format(player = ctx.author.name))
		return await ctx.send('{player}, either you have low balance or item is not in stock !'.format(player = ctx.author.name))
	
	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			return await ctx.send(embed = discord.Embed(
				description = '{user}, RUKO JARA SABAR KARO {hand}! \ntry after {n} seconds !'.format(
					user = ctx.author,
					hand = '\N{raised hand}',
					n = str(error.retry_after)[:4]
				),
				colour = discord.Colour.teal()
				)
			)

def setup(bot):
	bot.add_cog(playDarkMemer(bot))