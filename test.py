import praw
import sqlite3

db_file = "RCMaster-EndOfSeason-9-19-2022.sql"
con = None
try:
    con = sqlite3.connect(db_file)
except Error as e:
    print(e)
if con:
    cur = con.cursor()
    print('ensure USERS table exists',flush=True)
    cur.execute("CREATE TABLE IF NOT EXISTS users (user STRING PRIMARY KEY UNIQUE, points INTEGER, flair STRING);")
    con.commit()

reddit = praw.Reddit()
sub = reddit.subreddit("riderschallenge")



for flair in sub.flair(limit=None):
    
    
    user, points, userflair = flair["user"].name, flair["flair_text"].split(" | ")[0],flair["flair_text"].split(" | ")[1]
    
    print(user +" | "+ points +" | "+ userflair)

    cur.execute("""INSERT INTO users VALUES (?,?,?);""",(user, points, userflair))    
    con.commit()