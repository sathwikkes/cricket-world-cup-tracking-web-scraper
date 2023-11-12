from flask import Flask, render_template, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
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
# Create a database connection
#engine = create_engine('sqlite:///cricket.db')
#Base.metadata.bind = engine



@app.route('/')
def display_data():
    #good practice to close the database session after using it
    """
    losing the session is to ensure that resources associated with the database (such as database connections) are properly managed.
    The Session in SQLAlchemy represents an ongoing conversation between the application and the database, and it's important to close the session when you're done using it to release resources and prevent potential issues with connection pooling.
    """
    
    # Query the Players table
    # players_data = session.query(players).all()

    # # Query the Teams table
    # teams_data = session.query(teams).all()

    # # Query the MatchesPlayed table
    # matches_played_data = session.query(matchesplayed).all()

    # return render_template('index.html', players=players_data, teams=teams_data, matches_played=matches_played_data)
    session = Session(bind=engine)
    highest_score_players = session.query(players).filter(players.stat_name == "HIGHEST SCORE").all()

    most_runs_players = session.query(players).filter(players.stat_name == "MOST RUNS").all()

    most_wickets_players = session.query(players).filter(players.stat_name == "MOST WICKETS").all()

    # Query Teams table

    highest_innings_score_teams = session.query(teams).filter(teams.stat_name == "HIGHEST INNINGS SCORE").all()

    best_win_percentage_teams = session.query(teams).filter(teams.stat_name == "BEST WIN PERCENTAGE").all()
    session.close()
    return render_template('index.html', highest_score_players=highest_score_players,
                           most_runs_players=most_runs_players, most_wickets_players=most_wickets_players,
                           highest_innings_score_teams=highest_innings_score_teams,
                           best_win_percentage_teams=best_win_percentage_teams)


@app.route('/dictdata')
def data_transform():
    
    session = Session(bind=engine)

    matches_played_data = session.query(matchesplayed).all()
    players_data = session.query(players).all()

    combined_data = []


    for match in matches_played_data:
        player_ids_for_match = [match.id, match.id + 1, match.id + 2]
        players_for_match = [player for player in players_data if player.id in player_ids_for_match]
        combined_data.append({'match_data': match, 'players_data': players_for_match})

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

        if match_id in final_data:
            final_data[match_id]['Player Data'].update(player_data)
        else:
            final_data[match_id] = {'Match ID': match_id, "Matches Played":matches_played , "Date Scraped":match_date, 'Player Data': player_data}
    session.close()
    # print(final_data)
    return(jsonify(final_data))

@app.route('/analysis')
def analysis():
    return render_template('result.html')



if __name__ == '__main__':
    app.run(port=8000,debug=True)

