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
    try:
        if user_exists(user):
            print('Returning current points value')
            p = cur.execute("""SELECT points FROM users WHERE user = ?;""",(user,)).fetchone()
            return int(p[0])
    except Error as e:
        print(f"Error getting points for user {user}: {e}")
        return None

def get_flair(user):
    try:
        if user_exists(user):
            for row in cur.execute("""select flair from users where user = ?;""",(user,)):
                if row[0] == None:
                    return "Riders Challenge Participant"
                else:
                    return row[0]
    except Error as e:
        print(f"Error getting flair for user {user}: {e}")
        return None

def add_point(user):
    try:
        if not user_exists(user):
            add_user(user)
        cur.execute("""UPDATE users SET points = points + 1 WHERE user = ?;""", (user,))
        con.commit()
        print('point added. Current points: ' + str(cur.execute("""SELECT points FROM users WHERE user = ?;""",(user,)).fetchone()))
    except Error as e:
        print(f"Error adding a point for user {user}: {e}")
        return(e)

def user_exists(user):
    try:
        if cur.execute("select 1 from users where user = ?;", (user, )).fetchone():
            print('User Exists: ' + str(cur.execute("""SELECT * FROM users WHERE user = ?;""",(user,)).fetchall()))
            return True
        else:
            print('User does not exist.')
            return False
    except Error as e:
        print(f"Error checking if user {user} exists: {e}")
        return False

def add_user(user):
    try:
        print('Creating user now...')
        cur.execute("""INSERT INTO users VALUES (?,?,?);""",(user,int(0),"Riders Challenge Participant",))
        print("User Created: " + str(cur.execute("""SELECT * FROM users WHERE user = ?;""",(user,)).fetchall())) 
    except Error as e:
        print(f"Error adding user {user}: {e}")

def standings(user):
    try:
        p = int(cur.execute("""SELECT points FROM users WHERE user = ?;""",(user,)).fetchone()[0])
        standings = cur.execute("""select * from users order by points desc;""").fetchall()
        return standings
    except Error as e:
        print(f"Error getting standings for user {user}: {e}")
        return None
