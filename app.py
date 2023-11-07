from flask import Flask, render_template
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

session = Session(bind=engine)


@app.route('/')
def display_data():
    # Query the Players table
    # players_data = session.query(players).all()

    # # Query the Teams table
    # teams_data = session.query(teams).all()

    # # Query the MatchesPlayed table
    # matches_played_data = session.query(matchesplayed).all()

    # return render_template('index.html', players=players_data, teams=teams_data, matches_played=matches_played_data)
    highest_score_players = session.query(players).filter(players.stat_name == "HIGHEST SCORE").all()

    most_runs_players = session.query(players).filter(players.stat_name == "MOST RUNS").all()

    most_wickets_players = session.query(players).filter(players.stat_name == "MOST WICKETS").all()

    # Query Teams table

    highest_innings_score_teams = session.query(teams).filter(teams.stat_name == "HIGHEST INNINGS SCORE").all()

    best_win_percentage_teams = session.query(teams).filter(teams.stat_name == "BEST WIN PERCENTAGE").all()

    return render_template('index.html', highest_score_players=highest_score_players,
                           most_runs_players=most_runs_players, most_wickets_players=most_wickets_players,
                           highest_innings_score_teams=highest_innings_score_teams,
                           best_win_percentage_teams=best_win_percentage_teams)

if __name__ == '__main__':
    app.run(debug=True)
