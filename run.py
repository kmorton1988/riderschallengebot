import re
import praw
import sqlite3

#COnnect to and create cursor for Database
db = sqlite3.connect("RCMaster.db")
dbc = db.cursor()

reddit = praw.Reddit()

print(reddit.user.me())

