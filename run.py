import functions.reddit as reddit


KEYWORDS = ["complete"]

#Establish a Reddit Session
session = reddit.connect()

# Listening for Complete keyword in titles to reply to. 
for post in session.subreddit("riderschallengetest").stream.submissions():
    if post.saved:
        continue
    has_keyword = any(k.lower() in post.title.lower() for k in KEYWORDS)
    not_self = post.author != session.user.me()
    if has_keyword and not_self:
        post.save()
        to_post = reddit.process_post(post)
        session.subreddit("riderschallengetest").flair.set(post.author, text=to_post)


    


### Test Calls below to test the database functions in varying states
#db.mod_flair(dbfile,'kmisterk',f"""{flair_entry1}""")
#db.add_point(dbfile,"ninja-racer")
#db.mod_flair(dbfile,"rocketricer334",flair_entry3)