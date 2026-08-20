import pandas as pd


def calculate_percentage(made, attempted):
    if attempted == 0:
        return 0

    return (made / attempted) * 100


df = pd.read_csv(
    "backend/data/lebron_james_2025-26.csv"
)

df["GAME_DATE"] = pd.to_datetime(
    df["GAME_DATE"]
)

df = df.sort_values(
    by="GAME_DATE",
    ascending=False
)


games_played = len(df)

ppg = df["PTS"].mean()
rpg = df["REB"].mean()
apg = df["AST"].mean()
spg = df["STL"].mean()
bpg = df["BLK"].mean()


fg_percentage = calculate_percentage(
    df["FGM"].sum(),
    df["FGA"].sum()
)

three_percentage = calculate_percentage(
    df["FG3M"].sum(),
    df["FG3A"].sum()
)

ft_percentage = calculate_percentage(
    df["FTM"].sum(),
    df["FTA"].sum()
)


highest_scoring_index = df["PTS"].idxmax()

highest_scoring_game = df.loc[
    highest_scoring_index
]


last_five_games = df.head(5)

last_five_ppg = last_five_games["PTS"].mean()


player_stats = {
    "games_played": games_played,
    "ppg": round(ppg, 1),
    "rpg": round(rpg, 1),
    "apg": round(apg, 1),
    "spg": round(spg, 1),
    "bpg": round(bpg, 1),
    "fg_percentage": round(fg_percentage, 1),
    "three_percentage": round(three_percentage, 1),
    "ft_percentage": round(ft_percentage, 1),
    "last_five_ppg": round(last_five_ppg, 1)
}


print("\nPLAYER SEASON SUMMARY")
print("---------------------")

print("Games Played:", player_stats["games_played"])
print("PPG:", player_stats["ppg"])
print("RPG:", player_stats["rpg"])
print("APG:", player_stats["apg"])
print("SPG:", player_stats["spg"])
print("BPG:", player_stats["bpg"])

print("FG%:", player_stats["fg_percentage"])
print("3P%:", player_stats["three_percentage"])
print("FT%:", player_stats["ft_percentage"])

print("Last 5 PPG:", player_stats["last_five_ppg"])

print("\nHighest Scoring Game")
print("Points:", highest_scoring_game["PTS"])
print("Matchup:", highest_scoring_game["MATCHUP"])
print("Date:", highest_scoring_game["GAME_DATE"])