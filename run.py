import praw
import functions.db as db
import prawcore.exceptions as pc

#################################################################
###################### REDDIT INTERACTIONS ######################
#################################################################

#Establish a Reddit Session
reddit = praw.Reddit()
sub = reddit.subreddit("riderschallengetest")

def process_post(post):
    user = post.author.name
    db.add_point(user)
    if len(post.author_flair_text.split("|")) == 2: 
        flair_update = str(db.get_points(user)) + ' | ' + post.author_flair_text
    else:
        flair_update = str(db.get_points(user) + "Riders Challenge Participant")
    return flair_update

#check for formerly stickied post
def get_sticky_id():
    try:
        return sub.sticky(number=2).id
    except pc.NotFound as e:
        print(e)
        return False

def get_flair(post):
    flair_text = ''
    if post.author_flair_text != '':
        flair_text = post.author_flair_text
    return flair_text

# Listening for Complete keyword in titles to reply to. 
# for post in reddit.subreddit("riderschallengetest").stream.submissions():
    
#     if post.saved:
#         continue

#     has_keyword = any(k.lower() in post.title.lower() for k in ["complete"])
#     not_self = post.author.name != reddit.user.me().name
    
#     if has_keyword and not_self:
#         post.save()
#         sticky_id = get_sticky_id()
        
#         sticky = reddit.submission(sticky_id)
#         sticky.mod.flair(text="Completed",)    
            
#         to_post = process_post(post)
#         sub.flair.set(post.author.name, text=to_post)
#         post.mod.sticky()
#         post.mod.flair(text="Current Challenge",)

###################################################################
############ Implementation of multi-stream listening: ############
###################################################################

comment_stream = sub.stream.comments(pause_after=-1) # Special Case to be able to pass "None" to active listener
submission_stream = sub.stream.submissions(pause_after=-1) # Special Case to be able to pass "None" to active listener
while True:

#___________________Active Listener for Comments___________________#

    for comment in comment_stream:
        if comment is None:
            break
        if comment.saved:
            continue

        if comment.body.find("!modflair"):
            comment.save()
            new_flair = comment.body[10:]
            db.mod_flair(comment.body.author, new_flair)
            print("Code to handle api interaction to be placed here eventually")
        else:
            continue

#__________________Active Listener for Submissions__________________#

    for submission in submission_stream:
        if submission is None:
            break
        for post in reddit.subreddit("riderschallengetest").stream.submissions():

            if post.saved:
                continue

            has_keyword = any(k.lower() in post.title.lower() for k in ['complete'])                  # Checks if lower-case title has keyword "complete"
            not_self = post.author.name != reddit.user.me.name()                                      # Checks if the bot is doing the posting
            if has_keyword and not_self:                                                              # Makes sure that the following actions only ever fire if the bot didn't post it and the keyword was found
                post.save()                                                                           # Saves the post to enable skipping existing posts later. 
                sticky_id = get_sticky_id()                                                           # runs a method that grabs the Post ID of the current stickied challenge
                print(sticky_id)                                                                      # Verifies we have a stickied ID in the variable  
                try:                                              
                    sticky = reddit.submission(sticky_id)                                             # Stores the post object of the current sticky
                    print(type(sticky))                                                               # ensures object type "Object" (Debug, will delete eventually, or convert to log entry)
                    sticky.mod.flair(text="",)                                                        # Un-sets any flair it has to remove the "Current Challenge" flair
                except pc.Forbidden as f:
                    print(f)                                                                          # Useless error handling that just prints the error, but tells the script to continue instead of exiting on an error.
                continue                                                                              # Usually, this error was called when I was trying to use submission.mod.distinguish(), which apparently has issues. 
                
            to_post = process_post(post)                                                              # Runs a process on the post object of this for loop iteration to          
            reddit.subreddit("riderschallengetest").flair.set(post.author.name, text=to_post)         # add points, 
            post.mod.sticky()                                                                         # Sticky the post, 
            post.mod.flair(text="Current Challenge",)                                                 # and add "Current Challenge" as flair to the pinned post. 