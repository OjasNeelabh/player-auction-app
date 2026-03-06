import sqlite3

# SINGLE shared connection
conn = sqlite3.connect(
    "auction.db",
    check_same_thread=False
)

cursor = conn.cursor()


# USERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
password TEXT,
balance REAL DEFAULT 1000
)
""")


# BIDS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS bids(
player TEXT,
user TEXT,
bid REAL,
currency TEXT,
bid_usd REAL
)
""")


conn.commit()