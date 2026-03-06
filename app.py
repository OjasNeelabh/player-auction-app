import streamlit as st
import pandas as pd
import sqlite3

conn = sqlite3.connect("auction.db", check_same_thread=False)
c = conn.cursor()

players = pd.read_csv("players.csv")

st.title("🏆 Player Auction App")

username = st.text_input("Enter your username")

if username:

    st.subheader("Available Players")

    player = st.selectbox("Select Player", players["player"])

    bid = st.number_input("Enter your bid", min_value=0)

    if st.button("Place Bid"):

        c.execute("INSERT INTO bids VALUES(?,?,?)", (player, username, bid))
        conn.commit()

        st.success("Bid placed!")

    st.subheader("Current Bids")

    bids = pd.read_sql("SELECT * FROM bids", conn)
    st.dataframe(bids)

    if st.button("Finish Auction for Player"):

        result = pd.read_sql(
            f"SELECT * FROM bids WHERE player='{player}' ORDER BY bid DESC LIMIT 1",
            conn
        )

        if len(result) > 0:

            winner = result.iloc[0]["user"]
            price = result.iloc[0]["bid"]

            c.execute("INSERT INTO winners VALUES(?,?,?)",
                      (player, winner, price))
            conn.commit()

            st.success(f"{winner} won {player} for {price} coins!")

    st.subheader("Auction Winners")

    winners = pd.read_sql("SELECT * FROM winners", conn)
    st.dataframe(winners)