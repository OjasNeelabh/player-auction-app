import pandas as pd

def load_players():
    return pd.read_csv("players.csv")

def load_wins():
    return pd.read_csv("wins.csv")