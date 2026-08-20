from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog

search_name = "LeBron James"

matches = players.find_players_by_full_name(search_name)

if not matches:
    raise ValueError("Player not found.")

player = matches[0]

player_id = player["id"] #all the code above this is just to get the player id 

game_log = playergamelog.PlayerGameLog( #instance of the PlayerGameLog class, contains params like: player_id, season, timeout etc
    player_id=player_id,
    season="2025-26",
    season_type_all_star="Regular Season",
    timeout=30
)

#The nba_api package exposes response data in formats including dictionaries, JSON, and Pandas DataFrames.
df = game_log.get_data_frames()[0] #.get_data_frames() converts the game_log data into a list of Pandas DataFrames,
#                                   while the [0] gets the first item of that data frame, in this case a table containing lebron james's info

print(df.head())

df.to_csv( #tabular data stored in a text file - saving like this cause its faster and avoids unecessary network requests
    "backend/data/lebron_james_2025-26.csv",
    index=False
)

print("game log saved.")