import praw
import functions.db as db
import prawcore.exceptions as pc



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
    


    has_keyword = any(k.lower() in post.title.lower() for k in ["complete"])
    not_self = post.author.name != reddit.user.me.name()
    if has_keyword and not_self:
        post.save()
        sticky_id = get_sticky_id()
        print(sticky_id)
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

###################################################################
############ Implementation of multi-stream listening: ############
###################################################################

# comment_stream = sub.stream.comments(pause_after=-1) # Special Case to be able to pass "None" to active listener
# submission_stream = sub.stream.submissions(pause_after=-1) # Special Case to be able to pass "None" to active listener
# while True:

#___________________Active Listener for Comments___________________#

#     for comment in comment_stream:
#         if comment is None:
#             break
#         print(comment.author)

#__________________Active Listener for Submissions__________________#

#     for submission in submission_stream:
#         if submission is None:
#             break
#         for post in reddit.subreddit("riderschallengetest").stream.submissions():

        # if post.saved:
        #     continue

        # has_keyword = any(k.lower() in post.title.lower() for k in KEYWORDS)
        # not_self = post.author.name != reddit.user.me.name()
        # if has_keyword and not_self:
        #     post.save()
        #     sticky_id = get_sticky_id()
        #     print(sticky_id)
        #     try:
        #         sticky = reddit.submission(sticky_id)
        #         print(type(sticky))
        #         print(sticky)
        #         sticky.mod.flair(text="",)    
        #     except pc.Forbidden as f:
        #         print(f)
        #         continue
                
        #     to_post = process_post(post)
        #     print(to_post)
        #     reddit.subreddit("riderschallengetest").flair.set(post.author.name, text=to_post)
        #     post.mod.sticky()
        #     post.mod.flair(text="Current Challenge",)