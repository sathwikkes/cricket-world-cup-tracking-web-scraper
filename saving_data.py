import datetime
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


from main import  player_stat_name, player_stat, player_fname, player_lname, player_country, team_stat, team_stat_name, country, matches_played
engine = create_engine('sqlite:///cricket.db')

date = datetime.date.today()

Base = declarative_base()

class MatchesPlayed(Base):
    __tablename__ = 'MatchesPlayed'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    matches_played = Column(Integer)

class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True, autoincrement=True)
    stat_name = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    nationality = Column(String)
    rating = Column(String)

class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True, autoincrement=True)
    stat_name = Column(String)
    rating = Column(String)
    country = Column(String)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# Insert player data
for i in range(len(player_stat_name)):
    player = Player(
        stat_name = player_stat_name[i],
        first_name=player_fname[i],
        last_name=player_lname[i],
        nationality=player_country[i],
        rating=player_stat[i]
    )
    session.add(player)

# Insert team data
for i in range(len(team_stat_name)):
    team = Team(
        stat_name=team_stat_name[i],
        rating=team_stat[i],
        country=country[i]
    )
    session.add(team)


new_match = MatchesPlayed(date=date, matches_played=matches_played)
session.add(new_match)

# Commit the changes
session.commit()


session.close()

print("Saved data...")
