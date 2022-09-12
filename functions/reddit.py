import praw
import functions.db as db

dbfile = "../RCMaster.db"

def connect():
    reddit = praw.Reddit()
    return reddit

def process_post(post):
    user = post.author
    db.add_point(dbfile,user)
    flair_update = db.get_flair(dbfile,user)
    return flair_update