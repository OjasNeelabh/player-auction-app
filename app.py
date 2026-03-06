import streamlit as st
import database

from utils.load_data import load_players, load_wins
from utils.auction_logic import place_bid, get_bids, get_highest_bid
from utils.auth import create_user, login_user
from utils.wallet import get_balance, update_balance

st.set_page_config(
    page_title="Cricket Auction",
    layout="wide"
)


# Load CSS
def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

players = load_players()
wins = load_wins()

st.title("🏏 Cricket Player Auction")


# Sidebar Login Menu
menu = st.sidebar.selectbox(
    "Menu",
    ["Login", "Signup", "Auction"]
)


# -------------------
# Signup
# -------------------
if menu == "Signup":

    st.subheader("Create Account")

    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")

    if st.button("Create Account"):

        try:
            create_user(new_user, new_pass)
            st.success("Account created! Please login.")

        except:
            st.error("Username already exists.")


# -------------------
# Login
# -------------------
elif menu == "Login":

    st.subheader("Login")

    user = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if login_user(user, password):

            st.session_state["user"] = user
            st.success("Login successful!")

        else:
            st.error("Invalid credentials")


# -------------------
# Auction Page
# -------------------
elif menu == "Auction":

    if "user" not in st.session_state:

        st.warning("Please login first.")
        st.stop()

    username = st.session_state["user"]

    balance = get_balance(username)

    st.sidebar.write(f"👤 User: {username}")
    st.sidebar.metric("💰 Balance", balance)

    player = st.selectbox("Select Player", players["player"])

    p = players[players["player"] == player].iloc[0]

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(p["image"], width=250)

    with col2:
        st.subheader(player)
        st.write("Team:", p["team"])
        st.write("Role:", p["role"])
        st.write("Age:", p["age"])
        st.write("Base Price:", p["base_price"])

    tabs = st.tabs(["Stats", "Achievements", "Bidding"])

    # -------------------
    # Stats Tab
    # -------------------
    with tabs[0]:

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Matches", p["matches"])
        c2.metric("Runs", p["runs"])
        c3.metric("Wickets", p["wickets"])
        c4.metric("Strike Rate", p["strike_rate"])

        chart_data = {
            "Runs": p["runs"],
            "Wickets": p["wickets"]
        }

        st.bar_chart(chart_data)

    # -------------------
    # Achievements Tab
    # -------------------
    with tabs[1]:

        w = wins[wins["player"] == player].iloc[0]

        c1, c2, c3 = st.columns(3)

        c1.metric("Championships", w["championships"])
        c2.metric("Awards", w["awards"])
        c3.metric("MVP", w["mvp"])

    # -------------------
    # Bidding Tab
    # -------------------
    with tabs[2]:

        highest = get_highest_bid(player)

        if highest is not None:
            st.info(
                f"Current Highest Bid: {highest['user']} - {highest['bid']}"
            )

        bid = st.number_input("Enter your bid", min_value=0)

        if st.button("Place Bid"):

            if bid > balance:
                st.error("You do not have enough balance.")

            elif highest and bid <= highest["bid"]:
                st.error("Bid must be higher than the current highest bid.")

            else:

                place_bid(player, username, bid)
                update_balance(username, bid)

                st.success("Bid placed successfully!")

        bids = get_bids(player)

        st.subheader("Bid History")

        st.dataframe(bids)