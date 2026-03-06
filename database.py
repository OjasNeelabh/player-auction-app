import sqlite3

conn = sqlite3.connect("auction.db", check_same_thread=False)
c = conn.cursor()

# Users table
c.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
password TEXT,
balance INTEGER DEFAULT 1000
)
""")

# Bids
c.execute("""
CREATE TABLE IF NOT EXISTS bids(
player TEXT,
user TEXT,
bid INTEGER
)
""")
# Users table
c.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
password TEXT,
balance INTEGER DEFAULT 1000
)
""")

conn.commit()