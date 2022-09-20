import sqlite3
from sqlite3 import Error

# Creates database connection, creates 'users' table if there is no existing 'users' table
DB_FILE = "../RCMaster.sql"
__CONN = None # Module State? Not sure what this means. Seems to be a standard, though?

def cursor():
    global __CONN
    if __CONN:
        return __CONN

    __CONN = sqlite3.connect(DB_FILE, isolation_level=None)  # auto-commit as we don't need transactions
    
    return __CONN

def setup_db():
    cursor().execute("CREATE TABLE IF NOT EXISTS users (user STRING PRIMARY KEY UNIQUE, points INTEGER UNIQUE, flair STRING);")

def get_points(user):
    if row := cursor().execute("SELECT points from users where user = ?;", (user, )).fetchone():
        return row[0]
        
def add_point(user):
    if user_exists(user):
        cursor().execute("UPDATE users SET points = ? WHERE user = ?;", (get_points(user) + 1,
                                                                        user))
    else:
        cursor().execute("INSERT INTO users (user, points) VALUES (?, ?);", (user, 0))

def user_exists(user):
    if cursor().execute("select 1 from users where user = ?;", (user, )).fetchone():
        return True