import sqlite3
import pandas as pd

conn = sqlite3.connect("auction.db", check_same_thread=False)

def place_bid(player, user, bid):

    conn.execute(
        "INSERT INTO bids VALUES(?,?,?)",
        (player, user, bid)
    )

    conn.commit()


def get_bids(player):

    return pd.read_sql(
        "SELECT * FROM bids WHERE player=? ORDER BY bid DESC",
        conn,
        params=(player,)
    )


def get_highest_bid(player):

    bids = get_bids(player)

    if len(bids) > 0:
        return bids.iloc[0]

    return None