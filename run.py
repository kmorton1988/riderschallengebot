import praw
import functions.db as db
import prawcore.exceptions as pc
import markdown_strings as markdown

#Establish a Reddit Session
reddit = praw.Reddit()
sub = reddit.subreddit("riderschallenge")



def process_post(post):
    user = post.author.name
    db.add_point(user)
    points = db.get_points(user)
    flair = db.get_flair(user)
    reply_body = "**_Current Standings_**\r\n\r\n"
    reply_body += markdown.table_row(["Username","Points","Current Flair"]) + "\r\n"
    reply_body += markdown.table_delimiter_row(3) +"\r\n"
    standings = db.standings(user)
    length = len(standings)
    for s in range(length):
        reply_body += markdown.table_row(standings[s]) + "\r\n"
    flair_update = str(points) + ' | ' + flair
    
    print(reply_body)
    post.reply(reply_body)
    return flair_update

#check for formerly stickied post
def get_sticky_id():
    print("attempting to get stickies...")
    try:
        print(sub.sticky(number=2).id)
        return sub.sticky(number=2).id
    except pc.NotFound as e:
        print(e)
        return False
    except pc.Forbidden as f:
        print(f)
        return False

# Listening for Complete keyword in titles to reply to.
while True:

    try:  
        for post in sub.stream.submissions(skip_existing=True):
            
            if post.saved:
                continue

            has_keyword = any(k.lower() in post.title.lower() for k in ["complete"])
            not_self = post.author.name != reddit.user.me().name
            if has_keyword and not_self:
                post.save()
                sticky_id = get_sticky_id()
                try:
                    sticky = reddit.submission(sticky_id)
                    
                    #sticky.flair.select("91da1cea-c87f-11ed-8f80-72de23ea66e4")                            #Flair for testing on test sub
                    sticky.flair.select("6e869780-2a0b-11e4-bfd1-12313b0eb184")    #Flair ID for "complete" flair on the subreddit - Use on Main sub.
                except ValueError as f:
                    print(f)
                    continue
                    
                to_post = process_post(post)
                sub.flair.set(post.author.name, text=to_post)
                choices = post.flair.choices()
                post.mod.sticky()
                
                #post.flair.select("9760f59e-c87f-11ed-8b66-827eed3bdcca")                        #When testing on test sub, use this line
                post.flair.select('55e0642e-49df-11e4-ba33-12313b0e9e2c')       # Flair ID for "Current Challenge" flair on the subreddit - Use when running on main sub.
                                
    except Exception as e:
        print(e)
        pass
