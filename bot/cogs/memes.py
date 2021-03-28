import discord
from discord.ext import commands
import json
import requests

class memes(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.listOfMemes = []
		self.jump = -1
		self.next = -1
		self.update = False
		self.list_of_memes()
	
	def get_reddit_html(self, subreddit):
		headers = {
			"Host": "www.reddit.com",
			"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
		}
		html = requests.get("https://www.reddit.com/r/"+ subreddit + "/new/.json", headers = headers)
		return html

	def get_meme(self, node, html):
		title = html.json()["data"]["children"][node]["data"]["title"]
		url = html.json()["data"]["children"][node]["data"]["url"]
		upvotes = html.json()["data"]["children"][node]["data"]["ups"]
		downvotes = html.json()["data"]["children"][node]["data"]["downs"]
		comments = html.json()["data"]["children"][node]["data"]["num_comments"]
		return {'title': title, 'image': url, 'upvotes': upvotes, 'downvotes': downvotes, 'comments': comments}

	def list_of_memes(self):
		html = self.get_reddit_html('memes')
		for i in range(0, 24):
			self.next = self.next + 1 if self.next < 24 else 0
			meme_ = self.get_meme(self.next, html)
			if not meme_ in self.listOfMemes:
				if len(self.listOfMemes) < 24 and not self.update:
					self.listOfMemes.append(meme_)
				elif self.update and i < 12:
					self.listOfMemes[i] = meme_
		self.listOfMemes = self.listOfMemes[::-1]

	@commands.command(name = 'meme')
	async def post_memes(self, ctx):
		if self.jump < 23:
			if self.jump == 11:
				self.update = True
				self.list_of_memes()
				self.update = False
			self.jump += 1
		else:
			self.jump = 0
		print(self.jump)
		embed_ = discord.Embed(
			title = self.listOfMemes[self.jump]['title'],
			colour = discord.Colour.red(),
			url = self.listOfMemes[self.jump]['image']
		)
		embed_.set_image(url = self.listOfMemes[self.jump]['image'])
		embed_.set_footer(
			text = '\N{THUMBS UP SIGN}' + str(self.listOfMemes[self.jump]['upvotes']) + '  '
					+'\N{THUMBS DOWN SIGN}' + str(self.listOfMemes[self.jump]['downvotes']) + '  '
					+'\N{SPEECH BALLOON}' + str(self.listOfMemes[self.jump]['comments'])
		)
		await ctx.send(embed = embed_)
		return

def setup(bot):
	bot.add_cog(memes(bot))