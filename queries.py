from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, aliased 
from sqlalchemy.ext.automap import automap_base
#from checking_results import Base, players, teams, matchesplayed

app = Flask(__name__)


# Create a database connection
engine = create_engine('sqlite:///cricket.db')
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)
# Print all of the classes mapped to the Base
#Base.classes.keys()
players = Base.classes.players
teams = Base.classes.teams
matchesplayed = Base.classes.MatchesPlayed
session = Session(bind=engine)



matches_played_data = session.query(matchesplayed).all()
players_data = session.query(players).all()

combined_data = []


for match in matches_played_data:
    player_ids_for_match = [match.id, match.id + 1, match.id + 2]
    players_for_match = [player for player in players_data if player.id in player_ids_for_match]
    combined_data.append({'match_data': match, 'players_data': players_for_match})

#combined_data_dict = {}

# Initialize a variable to keep track of the player ID
player_id = 1

# Initialize an empty dictionary to store the final results
final_data = {}

# Iterate through combined_data
for row in combined_data:
    # Access the 'match_data' from each row
    match_data = row['match_data']
    
    # Extract the 'Match ID' from match_data
    match_id = match_data.id
    matches_played = match_data.matches_played
    match_date = match_data.date

    # Create a list of 'Player IDs' for the current 'Match ID'
    player_ids = list(range(player_id, player_id + 3))

    # # Extract player first and last names for the 'Player IDs'
    # player_names_query = session.query(players.first_name, players.last_name, players.stat_name, players.nationality, players.rating).filter(players.id.in_(player_ids))
    # player_names = [f"{player.first_name} {player.last_name}" for player in player_names_query]
    # rest = [f"{player.stat_name} {player.nationality} {player.rating}" for player in player_names_query]
    # # Combine player IDs with names as a dictionary
    # player_data = {player_id: player_name for player_id, player_name in zip(player_ids, player_names, rest)}
    player_query = session.query(players.first_name, players.last_name, players.stat_name, players.nationality, players.rating).filter(players.id.in_(player_ids))

    # Initialize an empty list to store player data
    player_data = []

    # Iterate through the player names query result
    for player in player_query:
        player_name = f"{player.first_name} {player.last_name}"
        stat_name = player.stat_name
        nationality = player.nationality
        rating = player.rating

        # Create a dictionary for the current player
        player_dict = {
            'Player Name': player_name,
            'Stat Name': stat_name,
            'Nationality': nationality,
            'Rating': rating
        }
        # Append the player dictionary to the player_data list
        player_data.append(player_dict)

    # Update the player_id counter
    player_id += 3

    # Add the 'Player IDs' to the combined_data_dict under the 'Match ID'
    # if match_id in combined_data_dict:
    #     combined_data_dict[match_id]['Player IDs'].extend(player_ids)
    # else:
    #     combined_data_dict[match_id] = {'Match ID': match_id,  'Player IDs': player_ids}


     # Add the player data to the final_data dictionary under the 'Match ID'
    if match_id in final_data:
        final_data[match_id]['Player Data'].update(player_data)
    else:
        final_data[match_id] = {'Match ID': match_id, "Matches Played":matches_played , "Date Scraped":match_date, 'Player Data': player_data}

# Now, combined_data_dict contains the data grouped by 'Match ID' with corresponding 'Player IDs'
# Access data for a specific 'Match ID'
# match_id = 7
# if match_id in combined_data_dict:
#     print(f"Match ID: {match_id}")
#     print(f"Player IDs: {combined_data_dict[match_id]['Player IDs']}")

print(final_data)
