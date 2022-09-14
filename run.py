import praw
import functions.db as db
import prawcore.exceptions as pc

KEYWORDS = ["complete"]

#Establish a Reddit Session
reddit = praw.Reddit()
sub = reddit.subreddit("riderschallengetest")

def process_post(post):
    user = post.author.name
    db.add_point(user)
    flair_update = str(db.get_points(user)) + ' | ' + db.get_flair(user)
    print(flair_update)
    return flair_update

#check for formerly stickied post
def get_sticky_id():
    print("attempting to get stickies...")
    try:
        return sub.sticky(number=2).id
    except pc.NotFound as e:
        print(e)
        return False
    except pc.Forbidden as f:
        print(f)
        return False

# Listening for Complete keyword in titles to reply to. 
for post in reddit.subreddit("riderschallengetest").stream.submissions():
    
    if post.saved:
        continue
    sticky_id = get_sticky_id()
    print(sticky_id)

    has_keyword = any(k.lower() in post.title.lower() for k in KEYWORDS)
    not_self = post.author.name != reddit.user.me.name()
    if has_keyword and not_self:
        post.save()
    
        try:
            sticky = reddit.submission(sticky_id)
            print(type(sticky))
            print(sticky)
            sticky.mod.flair(text="",)    
        except pc.Forbidden as f:
            print(f)
            continue
            
        to_post = process_post(post)
        print(to_post)
        reddit.subreddit("riderschallengetest").flair.set(post.author.name, text=to_post)
        post.mod.sticky()
        post.mod.flair(text="Current Challenge",)