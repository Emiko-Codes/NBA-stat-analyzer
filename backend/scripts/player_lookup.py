from nba_api.stats.static import players

search_name = input("Enter an NBA player: ").strip()

aliases = {
    "sga": "Shai Gilgeous-Alexander",
    "shai gilgeous alexander": "Shai Gilgeous-Alexander", 
    "kd": "Kevin Durant",
    "steph": "Stephen Curry",
    "bron": "LeBron James",
    "lebron": "LeBron James",
    "joker": "Nikola Jokic"
}

normalized_name = search_name.lower()

search_name = aliases.get(normalized_name, search_name) #gets the real name form the now lower case nickname e.g 'sga'

matches = players.find_players_by_full_name(search_name)

if not matches:
    print("Player not found.")
else:
    player = matches[0]

    print("Name:", player["full_name"])
    print("Player ID:", player["id"])
    print("Active:", player["is_active"])