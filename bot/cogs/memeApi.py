import praw
from psaw import PushshiftAPI
from datetime import datetime
import json

LINK = 'https://reddit.com'

reddit = praw.Reddit(
		client_id = 'NWQzDzJmrD0Fr5m48nE6bg',
		client_secret = 'wVQyHwglsC6c7JBXYVW7j9h5O9i7Yw',
		user_agent = 'memepuller0'
)

api = PushshiftAPI(reddit)
beg = int(datetime(2020, 7, 6).timestamp())
end = int(datetime(2020, 7, 7).timestamp())
'''
	@bgtask 
	before, start
	new func: back and forth to retrieve new memes (acc 2 date/time of last)
'''
memes = list(api.search_submissions(
	# after = start,
	before = beg,
	subreddit = 'memes',
	limit = 100
))


with open('memes.json', 'w') as file:
	data = {}
	for i, meme in enumerate(memes):
		data[i] = []
		data[i].append({
			'title': meme.title,
			'source': meme.permalink,
			'url': meme.url,
			'upvotes': meme.ups,
			'downvotes': meme.downs,
			'comments': meme.num_comments
		})
	json.dump(data, file, indent = 4)
