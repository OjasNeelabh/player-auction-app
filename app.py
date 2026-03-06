import streamlit as st
from utils.load_data import load_players, load_wins
from utils.auction_logic import place_bid, get_bids, get_highest_bid
import database

# Page configuration (must be first Streamlit command)
st.set_page_config(
    page_title="Cricket Auction",
    layout="wide"
)

# Load custom CSS
def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Load data
players = load_players()
wins = load_wins()

# App title
st.title("🏏 Cricket Player Auction")

# Username input
username = st.text_input("Enter your username")

# Player selector
player = st.selectbox("Select Player", players["player"])

# Get player row
p = players[players["player"] == player].iloc[0]

# Player info layout
col1, col2 = st.columns([1,2])

with col1:
    st.image(p["image"], width=250)

with col2:
    st.subheader(player)
    st.write("Team:", p["team"])
    st.write("Role:", p["role"])
    st.write("Age:", p["age"])
    st.write("Base Price:", p["base_price"])

# Tabs
tabs = st.tabs(["Stats","Achievements","Bidding"])


# ======================
# Stats Tab
# ======================
with tabs[0]:

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Matches", p["matches"])
    c2.metric("Runs", p["runs"])
    c3.metric("Wickets", p["wickets"])
    c4.metric("Strike Rate", p["strike_rate"])

    chart_data = {
        "Runs": p["runs"],
        "Wickets": p["wickets"]
    }

    st.bar_chart(chart_data)


# ======================
# Achievements Tab
# ======================
with tabs[1]:

    w = wins[wins["player"] == player].iloc[0]

    c1,c2,c3 = st.columns(3)

    c1.metric("Championships", w["championships"])
    c2.metric("Awards", w["awards"])
    c3.metric("MVP", w["mvp"])


# ======================
# Bidding Tab
# ======================
with tabs[2]:

    bid = st.number_input("Enter your bid", min_value=0)

    if st.button("Place Bid"):

        if username.strip() == "":
            st.error("Please enter a username before bidding.")
        else:
            place_bid(player, username, bid)
            st.success("Bid placed successfully!")

    bids = get_bids(player)

    st.subheader("Bid History")
    st.dataframe(bids)

    highest = get_highest_bid(player)

    if highest is not None:
        st.success(
            f"Highest Bid: {highest['user']} - {highest['bid']}"
        )