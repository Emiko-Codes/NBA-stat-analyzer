#installing fast api:
#python -m pip install "fastapi[standard]"  The current FastAPI documentation recommends the standard installation because it 
# includes the normal dependencies needed to run FastAPI, including its command-line tooling.

#pip installs Python packages inside the virtual environment
#.venv is an isolated Python environment specifically for this project So packages we install for the NBA analyzer don't interfere with your other Python projects.

#run the backend: fastapi dev backend/main.py
#The FastAPI CLI provides the fastapi dev command specifically for running an application during development.

#in http://127.0.0.1:8000,  127.0.0.1 is basically my computer while 8000 is the port my computer uses for this server. Port allows different servers to run at the same time on my computer


from nba_api.stats.static import players
from fastapi import FastAPI, HTTPException #give me the FastAPI class from the fastapi library
from nba_api.stats.endpoints import playergamelog #accepts player_id and season
import pandas as pd

app = FastAPI(
    title="Hoops App API",
    description="Backend API for NBA player statistics, comparisons, and trends.",
    version="1.0.0"
    
) 
player_aliases = {
    "sga": "Shai Gilgeous-Alexander",
    "shai gilgeous alexander": "Shai Gilgeous-Alexander",
    "kd": "Kevin Durant",
    "steph": "Stephen Curry",
    "bron": "LeBron James",
    "lebron": "LeBron James",
    "joker": "Nikola Jokic"
}

def get_player_stats(player_id: int, season: str):
    game_log = playergamelog.PlayerGameLog(
        player_id=player_id,
        season=season
    )

    df = game_log.get_data_frames()[0]

    if df.empty:
        return None

    stats = {
        "games_played": len(df),
        "ppg": round(df["PTS"].mean(), 1),
        "rpg": round(df["REB"].mean(), 1),
        "apg": round(df["AST"].mean(), 1),
        "spg": round(df["STL"].mean(), 1),
        "bpg": round(df["BLK"].mean(), 1),
        "fg_pct": round(df["FG_PCT"].mean() * 100, 1),
        "fg3_pct": round(df["FG3_PCT"].mean() * 100, 1),
        "ft_pct": round(df["FT_PCT"].mean() * 100, 1),
    }

    return stats

@app.get("/")
def root():
    return {
        "message": "Hoops App " # pretty cool, FastAPI converts this python dictionary into a JSON response automatically
    }
    
@app.get("/api/health")   
def health_check():
    return {
        "status":"ok"
    }


@app.get("/api/players/search")
def player_search(name: str):
    search_name = name.strip()
    
    normalized_name = search_name.lower()
    search_name = player_aliases.get(normalized_name, search_name) # format: dictionary.get(key, fallback)
    
    matches = players.find_players_by_full_name(search_name) #this is a list btw
    return{
        "query": search_name,
        "count":len(matches),
        "players":matches     
    }
    

@app.get("/api/players/{player_id}/stats")
def get_stats(
    player_id: int,
    season: str = "2025-26"
):
    player = players.find_player_by_id(player_id)

    if not player:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )

    stats = get_player_stats(
        player_id,
        season
    )

    if stats is None:
        raise HTTPException(
            status_code=404,
            detail=f"No stats found for {player['full_name']} in {season}"
        )

    return {
        "player": {
            "id": player["id"],
            "name": player["full_name"]
        },
        "season": season,
        "stats": stats
    }
    
   
@app.get("/api/compare")
def compare_players(
    player1_id: int,
    player2_id: int,
    season: str = "2025-26"
):
    player1 = players.find_player_by_id(player1_id)
    player2 = players.find_player_by_id(player2_id)

    if not player1:
        raise HTTPException(
            status_code=404,
            detail="Player 1 not found"
        )

    if not player2:
        raise HTTPException(
            status_code=404,
            detail="Player 2 not found"
        )

    player1_stats = get_player_stats(
        player1_id,
        season
    )

    player2_stats = get_player_stats(
        player2_id,
        season
    )

    if player1_stats is None:
        raise HTTPException(
            status_code=404,
            detail=f"No stats found for {player1['full_name']} in {season}"
        )

    if player2_stats is None:
        raise HTTPException(
            status_code=404,
            detail=f"No stats found for {player2['full_name']} in {season}"
        )

    return {
        "season": season,
        "player1": {
            "id": player1["id"],
            "name": player1["full_name"],
            "stats": player1_stats
        },
        "player2": {
            "id": player2["id"],
            "name": player2["full_name"],
            "stats": player2_stats
        }
    }
    
@app.get("/api/players/{player_id}/trends")
def get_player_trends(
    player_id: int,
    season: str = "2025-26",
    last_n: int = 10
):
    
    player = players.find_player_by_id(player_id)

    if not player:
        raise HTTPException(
            status_code=404,
            detail="Player not found."
        )

    # Make sure the requested number of games is valid
    if last_n < 1:
        raise HTTPException(
            status_code=400,
            detail="last_n must be at least 1."
        )

    # Fetch the player's game log from the NBA API
    game_log = playergamelog.PlayerGameLog(
        player_id=player_id,
        season=season
    )

    # Convert the NBA API result into a Pandas DataFrame
    df = game_log.get_data_frames()[0]

    # Handle seasons where the player has no games
    if df.empty:
        raise HTTPException(
            status_code=404,
            detail=f"No games found for {player['full_name']} in {season}."
        )

    # Convert GAME_DATE into an actual Pandas date type
    df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"])

    # Get the most recent games, then put them in chronological order
    recent_games = (
        df.sort_values(by="GAME_DATE", ascending=False)
        .head(last_n)
        .sort_values(by="GAME_DATE") # we want in order of oldest => newest for graphing purposes
    )

    # Convert each game into JSON-friendly data
    games = []

    for _, row in recent_games.iterrows(): # _ is convension for variables we ignore when iterating
        games.append({
            "date": row["GAME_DATE"].strftime("%Y-%m-%d"),
            "matchup": row["MATCHUP"],
            "result": row["WL"],
            "points": int(row["PTS"]),
            "rebounds": int(row["REB"]),
            "assists": int(row["AST"])
        })

    # Calculate averages for the selected recent games
    recent_averages = {
        "ppg": round(recent_games["PTS"].mean(), 1),
        "rpg": round(recent_games["REB"].mean(), 1),
        "apg": round(recent_games["AST"].mean(), 1)
    }

    return {
        "player": {
            "id": player["id"],
            "name": player["full_name"]
        },
        "season": season,
        "games_returned": len(games),
        "recent_averages": recent_averages,
        "games": games
    }