import praw
import functions.db as db

KEYWORDS = ["complete"]

#Establish a Reddit Session
r = praw.Reddit()

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

def process_post(post):
    user = post.author.name
    db.add_point(user)
    flair_update = str(db.get_points(user)) + ' | ' + db.get_flair(user)
    print(flair_update)
    return flair_update

# Listening for Complete keyword in titles to reply to. 
for post in r.subreddit("riderschallengetest").stream.submissions():
    if post.saved:
        continue
    has_keyword = any(k.lower() in post.title.lower() for k in KEYWORDS)
    not_self = post.author.name != r.user.me()
    if has_keyword and not_self:
        post.save()
        to_post = process_post(post)
        print(to_post)
        r.subreddit("riderschallengetest").flair.set(post.author.name, text=to_post)