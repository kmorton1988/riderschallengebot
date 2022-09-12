import praw
import dbedits.db as db
import dbedits.commands as commands

dbfile = "RCMaster.db"
reddit = praw.Reddit()
print(reddit.user.me())



#db.mod_flair(dbfile,'kmisterk',f"""{flair_entry1}""")

#db.add_point(dbfile,"ninja-racer")

#db.mod_flair(dbfile,"rocketricer334",flair_entry3)

#data = db.cursor.execute("select user from users;")
#print(data)
