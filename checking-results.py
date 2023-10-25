from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from saving_data import Player, Team  # Import your database models

# Create a database connection
engine = create_engine('sqlite:///cricket.db')

# Create a Session
Session = sessionmaker(bind=engine)
session = Session()

players = session.query(Player).all()
teams = session.query(Team).all()


print("Players:")
for player in players:
    print(f"{player.stat_name} {player.first_name} {player.last_name} {player.rating} {player.nationality}")

print("\nTeams:")
for team in teams:
    print(f"{team.stat_name} {team.rating}  {team.country}")
