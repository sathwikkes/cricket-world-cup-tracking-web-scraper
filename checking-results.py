# Import the Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# Create a database connection
engine = create_engine('sqlite:///cricket.db')
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)
# Print all of the classes mapped to the Base
Base.classes.keys()
players = Base.classes.players
teams = Base.classes.teams
matchesplayed = Base.classes.MatchesPlayed

# Create a Session
#Session = sessionmaker(bind=engine)
session = Session(engine)


players_data = session.query(players).all()

# Print all rows in the Players table
for player in players_data:
    print(player.id, player.stat_name, player.first_name, player.last_name, player.nationality, player.rating)

# Query the Teams table
teams_data = session.query(teams).all()

# Print all rows in the Teams table
for team in teams_data:
    print(team.id, team.stat_name, team.rating, team.country)

# Query the MatchesPlayed table
matches_played_data = session.query(matchesplayed).all()

# Print all rows in the MatchesPlayed table
for match in matches_played_data:
    print(match.id, match.date, match.matches_played)

# players = session.query(Player).all()
# teams = session.query(Team).all()


# print("Players:")
# for player in players:
#     print(f"{player.stat_name} {player.first_name} {player.last_name} {player.rating} {player.nationality}")

# print("\nTeams:")
# for team in teams:
#     print(f"{team.stat_name} {team.rating}  {team.country}")
