import pandas as pd
from database import conn


def place_bid(player, user, bid, currency, bid_usd):

    conn.execute(
        """
        INSERT INTO bids(player, user, bid, currency, bid_usd)
        VALUES (?, ?, ?, ?, ?)
        """,
        (player, user, bid, currency, bid_usd)
    )

    conn.commit()


def get_bids(player):

    df = pd.read_sql_query(
        """
        SELECT user, bid, currency, bid_usd
        FROM bids
        WHERE player=?
        ORDER BY bid_usd DESC
        """,
        conn,
        params=(player,)
    )

    return df


def get_highest_bid(player):

    df = pd.read_sql_query(
        """
        SELECT user, bid, currency, bid_usd
        FROM bids
        WHERE player=?
        ORDER BY bid_usd DESC
        LIMIT 1
        """,
        conn,
        params=(player,)
    )

    if len(df) == 0:
        return None

    return df.iloc[0]