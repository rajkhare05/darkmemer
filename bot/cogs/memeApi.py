from discord.ext import tasks, commands
from datetime import datetime
import requests
import discord
import json

class pull_memes(commands.Cog):
	def __init__(self, bot):
		d = datetime.now()
		self.AFTER = int(datetime(d.year, d.month, d.day, 0, 0, 0).timestamp())
		self.BEFORE = self.AFTER + 3600
		self.LINK = "https://apiv2.pushshift.io/reddit/submission/search?subreddit=memes"\
					"&limit=20"\
					"&after={0}"\
					"&before={1}".format(self.AFTER, self.BEFORE)
		data = {}
		data['memes'] = []
		reponse = requests.get(self.LINK)
		memes = reponse.json()
		with open('./bot/cogs/memes.json', 'w') as file:
			for meme in memes['data']:
				if self.validity(meme):
					data['memes'].append({
						'title': meme['title'],
						'url': meme['url'],
						'permalink': meme['permalink']
					})
			print('len: ', len(data['memes']))
			json.dump(data, file, indent = 4)
		self.memes = self.get_meme()

	def update_link(self):
		self.AFTER = self.BEFORE
		self.BEFORE = self.BEFORE + 3600
		self.LINK = "https://apiv2.pushshift.io/reddit/submission/search?subreddit=memes"\
					"&limit=20"\
					"&after={0}"\
					"&before={1}".format(self.AFTER, self.BEFORE)

	def add_more_memes(self):
		with open('./bot/cogs/memes.json', 'r+') as file:
			data = json.load(file)
			self.update_link()
			memes = requests.get(self.LINK).json()
			for meme in memes['data']:
				if self.validity(meme):
					self.memes['memes'].append({
						'title': meme['title'],
						'url': meme['url'],
						'permalink': meme['permalink']
					})
			print('len: ', len(self.memes['memes']))
			file.seek(0)
			json.dump(self.memes, file, indent = 4)

	def validity(self, data: dict):
		if not 'removed_by_category' in data.keys():
			return True
		elif data['removed_by_category'] == 'reddit':
			return True
		return False

	def delete_meme(self):
		with open('./bot/cogs/memes.json', 'w') as file:
			self.memes['memes'].pop(0)
			file.seek(0)
			json.dump(self.memes, file, indent = 4)

	def get_meme(self):
		with open('./bot/cogs/memes.json', 'r') as file:
			data = json.load(file)
			return data
	
	@commands.command(name = 'memes')
	async def send_memes(self, ctx):
		print(self.memes['memes'][0]['title'])
		embed_ = discord.Embed(
			title = self.memes['memes'][0]['title'],
			colour = discord.Colour.red(),
			url = 'https://reddit.com' + self.memes['memes'][0]['permalink']
		)
		embed_.set_image(url = self.memes['memes'][0]['url'])
		self.delete_meme()
		if len(self.memes['memes']) < 2:
			self.add_more_memes()
		return await ctx.send(embed = embed_)

def setup(bot):
	bot.add_cog(pull_memes(bot))
