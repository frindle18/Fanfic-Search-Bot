import praw
import config
from script import search_ffnet_fanfic

reddit = praw.Reddit(username = config.username,
                     password = config.password,
                     client_id = config.client_id,
                     client_secret = config.client_secret,
                     user_agent = 'Frindling fanfic links')

subreddit = reddit.subreddit('testingmyredditbots')

keyphrase = '!linkit '

for comment in subreddit.stream.comments(skip_existing=True):
    if keyphrase in comment.body:
        title = comment.body.replace(keyphrase, '')
        print(title)
        print('Finding fics...')

        fanfics = search_ffnet_fanfic(title)
        
        if fanfics:
            reply_text = "Here are the search results:\n\n"

            for idx, (fanfic_title, fanfic_link) in enumerate(fanfics, start=1):
                reply_text += f'{idx}. [{fanfic_title}]({fanfic_link})\n\n'

        else:
            reply_text = "No fanfiction found."

        comment.reply(reply_text)
        print("Reply posted.")
