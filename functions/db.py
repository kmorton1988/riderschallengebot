import sqlite3
from sqlite3 import Error

# Creates database connection, creates 'users' table if there is no existing 'users' table
db_file = "RCMaster.sql"
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

def get_points(user):
# Get's current Points by Connecting to the file and executing a command to return current value in "points". returns "None" even if you attempt to convert "None" to 0 explicitly. 
    if user_check(user):
        print('Returning current points value')
        p = cur.execute("""SELECT points FROM users WHERE user = ?;""",(user,)).fetchone()
        return int(p[0])
        
def get_flair(user):
    # get's current flair and passes the value forward. mod_flair() has logic to handle None value. (there is no other reason to have this method called from anywhere else)
    if user_check(user):
        for row in cur.execute("""select flair from users where user = ?;""",(user,)):
            if row[0] == None:
                return "Riders Challenge Participant"
            else:
                return row[0]

def add_point(user):
    if user_check(user):       
        try:
            cur.execute("""UPDATE users SET points = ? WHERE user = ?;""", (get_points(user) + 1, user,))
            con.commit()
            print('point added. Current points: ' + str(cur.execute("""SELECT points FROM users WHERE user = ?;""",(user,)).fetchone()))
        except Error as e:
            print("""Something didn't work when adding a point for ?. Returning the Error message: ?""",(user,e,))
            return(e)

def user_check(user):
    if cur.execute("select 1 from users where user = ?;", (user, )).fetchone():
        print('User Exists: ' + str(cur.execute("""SELECT * FROM users WHERE user = ?;""",(user,)).fetchall()))
        return True
    else:
        print('User did not exist. Creating now...')
        cur.execute("""INSERT INTO users VALUES (?,?,?);""",(user,int(0),"Riders Challenge Participant",))
        print("User Created: " + str(cur.execute("""SELECT * FROM users WHERE user = ?;""",(user,)).fetchall())) 
        return True

def standings(user):
    p = int(cur.execute("""SELECT points FROM users WHERE user = ?;""",(user,)).fetchone()[0])
    print(p)
    standings = cur.execute("""select * from users order by points desc;""").fetchall()
    print(standings)
    return standings