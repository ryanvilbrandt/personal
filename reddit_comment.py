import time
from datetime import datetime, timedelta
from configparser import RawConfigParser

import praw

config = RawConfigParser()
config.read("inputs/reddit.ini")

username = config.get("Credentials", "username")
password = config.get("Credentials", "password")
client_id = config.get("Credentials", "client id")
client_secret = config.get("Credentials", "client secret")
user = config.get("Search", "user")

now = datetime.now()
print(now)
print(now.timestamp())
one_day = timedelta(days=1)
print(one_day)
print(now - one_day)
print(now - one_day * 2)
print(now - one_day * 3)
print(now - one_day * 4)

# user_agent = 'Comment searcher'
# print("Creating Reddit object with user agent {!r}".format(user_agent))
# r = praw.Reddit(user_agent=user_agent, client_id=client_id, client_secret=client_secret)
# print("Logging in as {}...".format(username))
# r.login(username, password)

# user = r.redditor(user)
# user_comments = user.comments.new(limit=1024, params={'after': 'e0zryun'})
# comments_count = 0
# for comment in user_comments:
#     comments_count += 1
#     if "meter" in comment.body:
#         print(dir(comment))
#         print(comment.body)
#         print(time.ctime(comment.created))
#         print(comment.permalink)
#         print(comment.id)
#
# print(comments_count)