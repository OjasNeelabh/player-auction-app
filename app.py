import streamlit as st
import database

from utils.load_data import load_players, load_wins
from utils.auction_logic import place_bid, get_bids, get_highest_bid
from utils.auth import create_user, login_user
from utils.wallet import get_balance, update_balance, add_money


st.set_page_config(
    page_title="Cricket Auction",
    layout="wide"
)


# Load CSS
def load_css():

    with open("assets/style.css") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


load_css()


players = load_players()
wins = load_wins()

st.title("🏏 Cricket Player Auction")


menu = st.sidebar.selectbox(
    "Menu",
    ["Login","Signup","Auction"]
)


# ----------------
# SIGNUP
# ----------------

if menu == "Signup":

    st.subheader("Create Account")

    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")

    if st.button("Create Account"):

        try:

            create_user(new_user,new_pass)

            st.success("Account created")

        except:

            st.error("Username already exists")


# ----------------
# LOGIN
# ----------------

elif menu == "Login":

    st.subheader("Login")

    user = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if login_user(user,password):

            st.session_state["user"] = user

            st.success("Login successful")

        else:

            st.error("Invalid credentials")


# ----------------
# AUCTION
# ----------------

elif menu == "Auction":

    if "user" not in st.session_state:

        st.warning("Please login first")
        st.stop()


    username = st.session_state["user"]

    balance = get_balance(username)

    st.sidebar.write(f"User: {username}")
    st.sidebar.metric("Balance (USD)", balance)


    # ----------------
    # ADD MONEY
    # ----------------

    st.sidebar.subheader("Add Money")

    add_amount = st.sidebar.number_input(
        "Amount",
        min_value=0
    )

    if st.sidebar.button("Add Funds"):

        add_money(username, add_amount)

        st.sidebar.success("Money added")

        st.rerun()


    # ----------------
    # PLAYER TABLE
    # ----------------

    st.subheader("Players")

    st.dataframe(players, use_container_width=True)

    player = st.selectbox(
        "Select Player",
        players["player"]
    )


    p = players[players["player"] == player].iloc[0]


    col1,col2 = st.columns([1,2])


    with col1:

        st.image(p["image"], width=250)


    with col2:

        st.subheader(player)

        st.write("Team:",p["team"])
        st.write("Role:",p["role"])
        st.write("Age:",p["age"])
        st.write("Base Price:",p["base_price"])


    tabs = st.tabs(["Stats","Achievements","Bidding"])


    # ----------------
    # STATS
    # ----------------

    with tabs[0]:

        c1,c2,c3,c4 = st.columns(4)

        c1.metric("Matches",p["matches"])
        c2.metric("Runs",p["runs"])
        c3.metric("Wickets",p["wickets"])
        c4.metric("Strike Rate",p["strike_rate"])

        chart_data = {

            "Runs":p["runs"],
            "Wickets":p["wickets"]

        }

        st.bar_chart(chart_data)


    # ----------------
    # ACHIEVEMENTS
    # ----------------

    with tabs[1]:

        w = wins[wins["player"] == player].iloc[0]

        c1,c2,c3 = st.columns(3)

        c1.metric("Championships",w["championships"])
        c2.metric("Awards",w["awards"])
        c3.metric("MVP",w["mvp"])


    # ----------------
    # BIDDING
    # ----------------

    with tabs[2]:

        highest = get_highest_bid(player)

        if highest is not None:

            st.info(

                f"Highest Bid: {highest['user']} "

                f"{highest['bid']} {highest['currency']} "

                f"(≈ {round(highest['bid_usd'],2)} USD)"

            )


        currency = st.selectbox(
            "Currency",
            ["USD","INR","EUR"]
        )


        bid = st.number_input(
            f"Enter bid in {currency}",
            min_value=0
        )


        conversion = {

            "USD":1,
            "INR":0.012,
            "EUR":1.1

        }


        bid_usd = bid * conversion[currency]


        st.write(
            f"Converted Value: {round(bid_usd,2)} USD"
        )


        if st.button("Place Bid"):

            if bid_usd > balance:

                st.error("Not enough balance")

            elif highest is not None and bid_usd <= highest["bid_usd"]:

                st.error("Bid must be higher than current highest bid")

            else:

                place_bid(
                    player,
                    username,
                    bid,
                    currency,
                    bid_usd
                )

                update_balance(
                    username,
                    bid_usd
                )

                st.success(
                    f"Bid placed: {bid} {currency}"
                )

                st.rerun()


        bids = get_bids(player)

        st.subheader("Bid History")

        st.dataframe(bids)