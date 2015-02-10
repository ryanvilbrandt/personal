import praw, time

ITERS = 1

user_agent = 'Random post grabber by marco262'
print "Creating Reddit object with user agent {!r}".format(user_agent)
r = praw.Reddit(user_agent=user_agent)
print "Logging in as marco262..."
r.login('marco262', 'lalala01')

print "Getting random posts"
for i in xrange(ITERS):
    try:
        s = r.get_random_submission()
    except Exception:
        pass
    else:
        try:
            title = str(s.title)
        except UnicodeEncodeError:
            title = repr(s.title)
        try:
            subreddit = str(s.subreddit.display_name)
        except UnicodeEncodeError:
            subreddit = repr(s.subreddit.display_name)
        print "\t".join(
            [
            title,
            subreddit,
            str(s.score),
            str(s.upvote_ratio),
            s.permalink
            ]
            )
    time.sleep(1)

