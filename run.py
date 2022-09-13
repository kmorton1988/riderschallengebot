import functions.reddit as reddit
import praw
import functions.db as db

KEYWORDS = ["complete"]

#Establish a Reddit Session
con = praw.Reddit()

def process_post(post):
    user = post.author
    db.add_point(user)
    flair_update = db.get_flair(user)
    return flair_update

def generate_flair_text(user, existing_flair):
    try:
        user_flair_text, _ = existing_flair.split(" | ", 1)
    except ValueError:
        user_flair_text = existing_flair

    points = db.get_points(user) or 0

    if user_flair_text:
        return f"{user_flair_text} | {points}"
    else:
        return str(points)



# Listening for Complete keyword in titles to reply to. 
for post in reddit.subreddit("riderschallengetest").stream.submissions():
    if post.saved:
        continue
    has_keyword = any(k.lower() in post.title.lower() for k in KEYWORDS)
    not_self = post.author != con.user.me()
    if has_keyword and not_self:
        post.save()
        to_post = reddit.process_post(post)
        con.subreddit("riderschallengetest").flair.set(post.author, text=to_post)


    


### Test Calls below to test the database functions in varying states
#db.mod_flair(dbfile,'kmisterk',f"""{flair_entry1}""")
#db.add_point(dbfile,"ninja-racer")
#db.mod_flair(dbfile,"rocketricer334",flair_entry3)