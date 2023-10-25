# Importing Libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# Options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)

wd.get("https://www.cricketworldcup.com/tournament-stats")

#parent_elements = wd.find_elements(By.CLASS_NAME,"tournament-stats__row tournament-stats__row--player-stats")

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
    #print("Stat Title:", stat_titles[i].text)
    player_stat_name.append(stat_titles[i].text)
    #print("First Name:", first_names[i].text)
    player_fname.append(first_names[i].text)
    #print("Last Name:", last_names[i].text)
    player_lname.append(last_names[i].text)
    #print("AMT", player_ratings[i].text)
    player_stat.append(player_ratings[i].text)
    #print("Nationality:", nationalities[i].text)
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
        #print("Card Title:", card_titles[i].text)
        #print("Card Rating:", card_ratings[i].text)
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
            #print("Card Nationality:", card_nationality)
        print("\n")
else:
    print("Card and Away Team Nationalities not available.")



print(player_stat_name)
print(player_fname)
print(player_lname)
print(player_stat)
print(player_country)
print("\n")
print("------------")
print(team_stat_name)
print(team_stat)
print(country)


# for i in range(len(card_titles)):
#     print("Card Title:", card_titles[i].text)
#     print("Card Rating:", card_ratings[i].text)
#     print("Card Nationality:", card_nationalities[i].text)
#     print("\n")




# for i in range(len(away_team_elements)):
#     print("Away Team Nationality:", away_team_elements[i].text)
#     print("\n")

 

# # Iterate through the parent elements
# for parent_element in parent_elements:
#     # Locate the child elements within the parent element
#     stat_title = parent_element.find_element(By.CLASS_NAME, "tournament-stats-card__title")
#     first_name = parent_element.find_element(By.CLASS_NAME,"tournament-stats-card__first-name")
#     last_name = parent_element.find_element(By.CLASS_NAME,"tournament-stats-card__last-name")
#     nationality = parent_element.find_element(By.CLASS_NAME,"tournament-stats-card__nation--abbr")

#     # Extract and print the text from each element
#     print("Stat Title:", stat_title.text)
#     print("First Name:", first_name.text)
#     print("Last Name:", last_name.text)
#     print("Nationality:", nationality.text)
#     print("\n")