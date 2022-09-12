import sqlite3

def dbconnect():
    con = sqlite3.connect("RCMaster.db")
    cur = con.cursor()