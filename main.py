# Import the necessary libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker
Base = declarative_base()

# Define your database classes (MatchesPlayed, Player, Team)
# ...
# Creates Player, Matches Played, and Team Classes which will serve as the anchor points for our Tables
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

# Function to scrape data from the website
def scrape_data():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    wd.get("https://www.cricketworldcup.com/tournament-stats")

    player_stat_name = []
    player_stat = []
    player_fname = []
    player_lname =[]
    player_country= []

    team_stat_name = []
    team_stat = []
    country = []

    # Locate the parent element by class name
    parent_element = wd.find_element(By.CLASS_NAME, "tournament-stats__row--player-stats")

    # Find and extract all h4 elements (stat titles)
    stat_titles = parent_element.find_elements(By.CLASS_NAME,"tournament-stats-card__title")

    # Find and extract all first name elements
    first_names = parent_element.find_elements(By.CLASS_NAME,"tournament-stats-card__first-name")

    # Find and extract all last name elements
    last_names = parent_element.find_elements(By.CLASS_NAME,"tournament-stats-card__last-name")

    player_ratings = parent_element.find_elements(By.CLASS_NAME,"tournament-stats-card__rating")

    # Find and extract all nationality elements
    nationalities = parent_element.find_elements(By.CLASS_NAME,"tournament-stats-card__nation--abbr")

    # Iterate through the elements and extract their text
    for i in range(len(stat_titles)):
        player_stat_name.append(stat_titles[i].text)
        player_fname.append(first_names[i].text)
        player_lname.append(last_names[i].text)
        player_stat.append(player_ratings[i].text)
        player_country.append(nationalities[i].text)
        #print("\n")


    # Locate the parent element by class name
    parent_elements = wd.find_element(By.CLASS_NAME,"tournament-stats__row--team-stats")

    # Locate the "Matches Played" value using its CSS selector
    matches_played_element = wd.find_element(By.CSS_SELECTOR,".wheel-chart.js-matches-played .wheel-chart__value.js-value-counter")

    if matches_played_element:
        # Extract and print the "Matches Played" value
        matches_played = matches_played_element.get_attribute("data-value")
        print("Matches Played:", matches_played)
    else:
        print("Matches Played element not found.")

    # Find and extract card titles
    card_titles = parent_elements.find_elements(By.CLASS_NAME,"tournament-stats-card__title")

    # Find and extract card ratings
    card_ratings = parent_elements.find_elements(By.CLASS_NAME,"tournament-stats-card__rating")

    # Find and extract card nationalities
    card_nationalities = parent_elements.find_elements(By.CLASS_NAME,"tournament-stats-card__nation--abbr")

    # Find and extract card nationalities for away team
    away_team_elements = parent_elements.find_elements(By.CLASS_NAME, "tournament-stats-card__nation.tournament-stats-card__nation--away-team.tournament-stats-card__nation--abbr")


    if card_nationalities and away_team_elements:
        for i in range(len(card_titles)):
            team_stat_name.append(card_titles[i].text)
            team_stat.append(card_ratings[i].text)
            if i < len(card_nationalities):
                card_nationality = card_nationalities[i].text
                # Check if there's an "away team nationality" available
                if i == (len(card_titles)-1):
                    for i in range(len(away_team_elements)):
                        away_team_nationality = away_team_elements[i].text
                    card_nationality += " vs " + away_team_nationality
                country.append(card_nationality)
            print("\n")
    else:
        print("Card and Away Team Nationalities not available.")

    return player_stat_name, player_stat, player_fname, player_lname, player_country, team_stat, team_stat_name, country, matches_played

# Function to connect to the database
def connect_to_database():
    # Create the database engine and tables
    engine = create_engine('sqlite:///cricket.db')
    conn = engine.connect()
    Base.metadata.create_all(conn)

    Session = sessionmaker(bind=engine)
    session = Session()

    return session

# Function to add data to the database
def add_data_to_database(session, statistic, player_rating, player_first_name, player_last_name, player_nationality, team_stat_name, team_data, team_country, matches_played):
    player_stat_name, player_stat, player_fname, player_lname, player_country, team_stat, team_stat_name, country =  statistic, player_rating, player_first_name, player_last_name, player_nationality, team_stat_name, team_data, team_country

    date = datetime.date.today()

    for i in range(len(player_stat_name)):
        player = Player(
            stat_name=player_stat_name[i],
            first_name=player_fname[i],
            last_name=player_lname[i],
            nationality=player_country[i],
            rating=player_stat[i]
        )
        session.add(player)

    for i in range(len(team_stat_name)):
        team = Team(
            stat_name=team_stat_name[i],
            rating=team_stat[i],
            country=country[i]
        )
        session.add(team)

    new_match = MatchesPlayed(date=date, matches_played=matches_played)
    session.add(new_match)

    session.commit()
    session.close()

    print("Saved data...")

def main():
    statistic, player_rating, player_first_name, player_last_name, player_nationality, team_stat_name, team_data, team_country, matches_played = scrape_data()
    session = connect_to_database()
    add_data_to_database(session,  statistic, player_rating, player_first_name, player_last_name, player_nationality, team_stat_name, team_data, team_country, matches_played)

if __name__ == "__main__":
    main()
