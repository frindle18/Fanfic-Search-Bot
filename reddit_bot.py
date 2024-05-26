import praw
import config
from ffnet_search import search_fanfic

reddit = praw.Reddit(username = config.username,
                     password = config.password,
                     client_id = config.client_id,
                     client_secret = config.client_secret,
                     user_agent = 'Frindling fanfic links')

subreddit = reddit.subreddit('testingmyredditbots')

keyphrase = '!linkit '

for comment in subreddit.stream.comments():
    if keyphrase in comment.body:
        title = comment.body.replace(keyphrase, '')
        print(title)
        print('Finding fics...')

        fanfics = search_fanfic(title)
        for fanfic in fanfics:
            print(f'Title: {fanfic[0]}') 
            print(f'Link: {fanfic[1]}')
            