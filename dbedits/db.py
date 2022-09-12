import sqlite3
from sqlite3 import Error

# Creates database connection, creates 'users' table if there is no existing 'users' table
def create_connection(db_file):
    con = None
    try:
        con = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    if con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users (user STRING PRIMARY KEY UNIQUE, points INTEGER, flair STRING);")
        con.commit
    return con

def get_points(file,user):
    # Get's current Points by Connecting to the file and executing a command to return current value in "points". returns "None" even if you attempt to convert "None" to 0 explicitly. 
    con = create_connection(file)
    cur = con.cursor()
    for row in cur.execute("""SELECT points from users where user = ?;""",(user,)):
        return int(row[0])

def get_flair(file,user):
    # get's current flair and passes the value forward. mod_flair() has logic to handle None value. (there is no other reason to have this method called from anywhere else)
    con = create_connection(file)
    cur = con.cursor()
    for row in cur.execute("""select flair from users where user = ?""",(user,)):
        return(row[0])

# Function for adding a point for a completed post
def add_point(file,user):
    # Creates database connection
    con = create_connection(file)
    
    # and the database cursor
    cur = con.cursor()
    
    # sets a flair variable for later use
    flair = get_flair(file,user)

    # sets the current points to a variable
    current_points = get_points(file,user)
    if current_points == None:
        current_points = 0    
    # Adds a point. 
    new_points = current_points + 1

    # Modifies the values of the existing user, or creates a new row in case the user does not yet exist. It's okay for flair to be entered as None if no flair exists for the user.
    cur.execute("""INSERT OR REPLACE INTO users (user,points,flair) VALUES (?,?,?);""",(user, new_points, flair,))
    
    # commites the change to the database
    con.commit()
    
    # closes the connection to the database. 
    con.close()

def mod_flair(file,user,flair):
    # Takes 3 arguments: File: database file, User: user to be modified, Flair: custom flair requested

    # Database Connection Created
    con = create_connection(file)
    
    # Database Cursor created
    cur = con.cursor()

    # Capture current points
    current_points = get_points(file,user)

    # Ensuring an integer is eventually passed, in case of no points for user
    if current_points == None:
        current_points = 0
    
    #capture current flair
    current_flair = get_flair(file,user)

    #Checks for existing flair. If flair is found, it overwrites existing flair with new flair. If no flair is found, it creates the flair. 
    if current_flair == None:
        cur.execute("""INSERT OR REPLACE INTO users (user,points,flair) VALUES (?,?,?);""",(user, current_points, str(current_points) + " | " + flair,))
    else:
        new_flair = str(current_points) + " | " + flair
        cur.execute("""INSERT OR REPLACE INTO users (user, points, flair) VALUES (?,?,?);""",(user, current_points, new_flair,))
    con.commit()
    con.close()