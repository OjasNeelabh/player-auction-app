import sqlite3

conn = sqlite3.connect("auction.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS bids(
player TEXT,
user TEXT,
bid INTEGER
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS winners(
player TEXT,
winner TEXT,
price INTEGER
)
""")

conn.commit()