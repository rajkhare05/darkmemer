from discord.ext import tasks, commands
from datetime import datetime
import requests
import discord
import json

class pull_memes(commands.Cog):
	def __init__(self, bot):
		d = datetime.now()
		self.AFTER = int(datetime(d.year, d.month, d.day, 0, 0, 0).timestamp()) - 1
		self.BEFORE = self.AFTER + 3600
		self.LINK = "https://apiv2.pushshift.io/reddit/submission/search?subreddit=memes"\
					"&limit=100"\
					"&after={0}"\
					"&before={1}".format(self.AFTER, self.BEFORE)
		self.memes = {}
		self.memes['memes'] = []
		self.memes['last_time'] = 0
		self.queue_length = 0
		reponse = requests.get(self.LINK)
		raw_memes = reponse.json()
		with open('./bot/cogs/memes.json', 'w') as file:
			for meme in raw_memes['data']:
				if self.validity(meme):
					self.memes['memes'].append({
						'title': meme['title'],
						'url': meme['url'],
						'permalink': meme['permalink']
					})
			self.memes['last_time'] = meme['retrieved_on']
			self.queue_length = len(self.memes['memes'])
			json.dump(self.memes, file, indent = 4)
		self.initiate_add_more_memes.start()

	def update_link(self):
		self.AFTER = self.memes['last_time']
		if self.AFTER >= self.BEFORE:
			self.BEFORE = self.AFTER + 3600

		self.LINK = "https://apiv2.pushshift.io/reddit/submission/search?subreddit=memes"\
					"&limit=100"\
					"&after={0}"\
					"&before={1}".format(self.AFTER, self.BEFORE)

	def add_more_memes(self):
		with open('./bot/cogs/memes.json', 'r+') as file:
			self.update_link()
			memes = requests.get(self.LINK).json()
			for meme in memes['data']:
				if self.validity(meme):
					self.memes['memes'].append({
						'title': meme['title'],
						'url': meme['url'],
						'permalink': meme['permalink']
					})
			self.memes['last_time'] = meme['retrieved_on']
			self.queue_length = len(self.memes['memes'])
			file.seek(0)
			json.dump(self.memes, file, indent = 4)

	def validity(self, data: dict):
		key = 'removed_by_category'
		if not key in data.keys():
			return True
		elif data[key] == 'reddit' or data[key] is None:
			return True
		return False

	def delete_meme(self):
		with open('./bot/cogs/memes.json', 'w') as file:
			self.memes['memes'].pop(0)
			file.seek(0)
			json.dump(self.memes, file, indent = 4)
	
	@commands.command(name = 'meme')
	async def send_memes(self, ctx):
		embed_ = discord.Embed(
			title = self.memes['memes'][0]['title'],
			colour = discord.Colour.red(),
			url = 'https://reddit.com' + self.memes['memes'][0]['permalink']
		)
		embed_.set_image(url = self.memes['memes'][0]['url'])
		self.delete_meme()
		return await ctx.send(embed = embed_)
	
	@tasks.loop(seconds = 10.0)
	async def initiate_add_more_memes(self):
		if len(self.memes['memes']) <= self.queue_length/2:
			temp = self.queue_length
			self.add_more_memes()
			temp -= len(self.memes['memes'])

def setup(bot):
	bot.add_cog(pull_memes(bot))
