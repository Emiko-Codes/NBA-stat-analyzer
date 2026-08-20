import pandas as pd  # Imports the Pandas library and gives it the shorter name "pd"


df = pd.read_csv(  # Reads the CSV file and converts it into a Pandas DataFrame
    "backend/data/lebron_james_2025-26.csv"
)


df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"])  # Converts the GAME_DATE column from text into actual date/time values


print("First five rows:")
print(df.head())  # Displays the first 5 rows of the DataFrame


print("\nShape:")
print(df.shape)  # Shows the size of the DataFrame as (number of rows, number of columns)


print("\nColumns:")
print(df.columns.tolist())  # Gets all column names and converts them into a normal Python list


print("\nBasic Stats:")

print("PPG:", df["PTS"].mean())  # Selects the PTS column and calculates the average points per game

print("RPG:", df["REB"].mean())  # Selects the REB column and calculates the average rebounds per game

print("APG:", df["AST"].mean())  # Selects the AST column and calculates the average assists per game


high_scoring_games = df[df["PTS"] >= 30]  # Filters df and keeps only rows where the player scored 30+ points

print("\n30+ Point Games:")

print(
    high_scoring_games[
        ["GAME_DATE", "MATCHUP", "PTS", "REB", "AST"]  # Selects only these columns from the filtered games
    ]
)


sorted_games = df.sort_values(
    by="PTS",          # Sorts the rows based on the PTS column
    ascending=False    # Highest point totals come first instead of lowest first
)


print("\nHighest Scoring Games:")

print(
    sorted_games[
        ["GAME_DATE", "MATCHUP", "PTS"]  # Only displays these 3 columns
    ].head(10)  # Displays only the first 10 rows, which are now the 10 highest-scoring games
)