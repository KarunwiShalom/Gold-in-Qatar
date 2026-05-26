import pandas as pd
from string import ascii_uppercase as groups
import pickle

# Extracting all the groups from the website
GroupTable = pd.read_html('https://web.archive.org/web/20221115040351/https://en.wikipedia.org/wiki/2022_FIFA_World_Cup')
GroupTable[12]  # The first group is the 12th table by index search
GroupTable[19]  # Each of the tables are seperated by 7 other tables
GroupTable[26]

# Renaming each extracted group with appropriate group name
dict_table = {}
for x, i in zip(groups, range(12, 64, 7)):                          # For each table extracted (7 unnecessary tables inbetween each of them)
    df = GroupTable[i]                                              # Iterating through each extracted table  
    df.rename(columns = {df.columns[1] : 'Team'}, inplace = True),  # Renaming the second column to 'Teams'  
    df.drop(columns = df.columns[-1], inplace = True)               # Dropping the 'Qualification' column
    dict_table[f'Group {x}'] = df                                   # Adding each column into a dictionary as Group ("each iteration")


dict_table.keys() # Checking for errors
dict_table['Group E']

with open('groupstage', 'wb') as file:
    pickle.dump(dict_table, file)    # Exporting the dictionary


import requests
from bs4 import BeautifulSoup
from pandas.api.types import CategoricalDtype

years1 = [1930, 1934, 1938, 1950, 1954, 1958, 1962,
          1966, 1970, 1974, 1978, 1982, 1986]                                # All previous editions of the world cup

years2 = [1994, 1998, 2002, 2006, 2010, 2014, 2018]                          # 1990 extracts incomplete data so it's handled differently

url = 'https://en.wikipedia.org/wiki/2018_FIFA_World_Cup'                   # Preparing the soup
response = requests.get(url)
file = response.text

soup = BeautifulSoup(file,'lxml')                                           # Saving the soup

matches = soup.find_all('div', class_="footballbox")                        # Extracting the matches played from the soup

# Creating empty lists for each game played
home = []
score = []
away = []

# Appending the scraped information from the website into the empty lists
for match in matches:
    home.append(match.find('th', 'fhome').get_text())
    score.append(match.find('th', 'fscore').get_text())
    away.append(match.find('th', 'faway').get_text())

dict_matches = {'home':home, 'score':score, 'away':away}                    # Saving the lists into a dictionary

# Saving the dictionary into a dataframe
df_games = pd.DataFrame(dict_matches)
df_games['year'] = '2018'
df_games

# Creating a function to use for all previous editions
def all_games_played(year):                                         # The function name
    url = f'https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup'    # The 'f-string' to add the year variable for each year supplied into the function
    response = requests.get(url)
    file = response.text
    
    soup = BeautifulSoup(file,'lxml')   
    
    matches = soup.find_all('div', class_="footballbox")
    
    home = []
    score = []
    away = []
    
    for match in matches:
        home.append(match.find('th', 'fhome').get_text())
        score.append(match.find('th', 'fscore').get_text())
        away.append(match.find('th', 'faway').get_text())
    
    dict_matches = {'home':home, 'score':score, 'away':away} 
    
    df_games = pd.DataFrame(dict_matches)
    df_games['year'] = year                                          # Adding a year column according to the year supplied into the function
    
    return df_games

all_games_played('1990')                                             # Testing out the function

# Creating a dataframe for the missing data in 1990
df_missing_data = pd.DataFrame(
                {'home': ['Italy','United States', 'Italy', 'Austria', 'Italy', 'Austria',
                        'Argentina', 'Soviet Union', 'Argentina', 'Cameroon', 'Argentina', 'Cameroon',
                        'Brazil', 'Costa Rica', 'Brazil', 'Sweden', 'Brazil', 'Sweden',
                        'United Arab Emirates', 'West Germany', 'Yugosalavia', 'West Germany', 'West Germany', 'Yugoslavia',
                        'Belgium', 'Uruguay', 'Belgium', 'South Korea', 'Belgium', 'South Korea',
                        'England', 'Netherlands', 'England', 'Republic of Ireland', 'England', 'Republic of Ireland'], 
                'score': ['1-0', '1-5', '1-0', '0-1', '2-0', '2-1',
                         '0-1', '1-0', '2-0', '2-1', '1-1', '0-4',
                         '2-1', '1-0', '1-0', '1-2', '1-0', '1-2',
                         '0-2', '4-1', '1-0', '5-1', '1-1', '4-1',
                         '2-0', '0-0', '3-1', '1-3', '1-2', '0-1',
                         '1-1', '1-1', '0-0', '0-0', '1-0', '1-1'], 
                'away': ['Austria', 'Czechoslovakia', 'United States', 'Czechoslovakia', 'Czechoslovakia', 'United States',
                        'Cameroon', 'Romania', 'Soviet Union', 'Romania', 'Romania', 'Soviet Union',
                        'Sweden', 'Scotland', 'Costa Rica', 'Scotland', 'Scotland', 'Costa Rica',
                        'Colombia', 'Yugoslavia', 'Colombia', 'United Arab Emirates', 'Colombia', 'United Arab Emirates',
                        'South Korea', 'Spain', 'Uruguay' , 'Spain', 'Spain', 'Uruguay',
                        'Republic of Ireland', 'Egypt', 'Netherlands', 'Egypt', 'Egypt', 'Netherlands']})

df_missing_data['year'] = '1990'       # Adding the year column
df_missing_data                              

# Creating a dataframe for the extracted 1990 data
df_1990_2 = all_games_played('1990')

# Appending the extracted data to the missing data
df_1990 = df_missing_data._append(df_1990_2, ignore_index = True)
df_1990

# For loops using list comprehension
before_1990 = [all_games_played(year) for year in years1]
after_1990 = [all_games_played(year) for year in years2]           

# Extracting all world cup games data excluding 1990
df_before_1990 = pd.concat(before_1990, ignore_index=True)
df_after_1990 = pd.concat(after_1990, ignore_index = True)

# Adding 1990 data within the extracted data
df_world1 = df_before_1990._append(df_1990, ignore_index=True)
df_world_cup = df_world1._append(df_after_1990, ignore_index=True)
df_world_cup

# Saving the dataframe to a csv
df_world_cup.to_csv('World_cup_total_games_2018.csv', index=False)

# Extracting the fixtures for the 2022 world cup
url2 = 'https://web.archive.org/web/20221115040351/https://en.wikipedia.org/wiki/2022_FIFA_World_Cup'    
response = requests.get(url2)
file2 = response.text
    
soup2 = BeautifulSoup(file2,'lxml')   
    
matches = soup2.find_all('div', class_="footballbox")
    
home = []
score = []
away = []
    
for match in matches:
        home.append(match.find('th', 'fhome').get_text())
        score.append(match.find('th', 'fscore').get_text())
        away.append(match.find('th', 'faway').get_text())
    
dict_matches = {'home':home, 'score':score, 'away':away} 
    
df_fixtures = pd.DataFrame(dict_matches)
df_fixtures['year'] = 2022
df_fixtures

# Saving the dataframe to a csv
df_fixtures.to_csv('World_cup_fixtures_2022.csv', index=False)

df_fifa = pd.read_csv('World_cup_data_2018.csv')
df_fixture = pd.read_csv('World_cup_fixtures_2022.csv')

df_fifa[df_fifa['home'].isnull()]              #Check for null values

df_fifa

# Removing all leading and trailing whitespaces
df_fifa['home'] = df_fifa['home'].str.strip()
df_fifa['away'] = df_fifa['away'].str.strip()
df_fixture['home'] = df_fixture['home'].str.strip()
df_fixture['away'] = df_fixture['away'].str.strip()

df_fifa

# There is a game in which there was a walkover that needs to be removed

to_delete = df_fifa[df_fifa['score'].str.contains('w/o')].index  # Finding the index of the game
df_fifa.drop(index = to_delete, inplace= True)                        # Deleting the row with the index

# Removing all scores that have (a.e.t)
df_fifa['score'] = df_fifa['score'].str.replace('[(a-z)+.]','',regex=True)

# Removing leading or trailing whitespaces
df_fifa['score'] = df_fifa['score'].str.strip()

# Assigning the home and away goals respectively
df_fifa[['home_goals','away_goals','x']] = df_fifa['score'].str.split(" ", expand=True)

# Dropping the unecessary columns
df_fifa.drop(['score', 'x'], axis=1, inplace=True)

# Checking the datatypes
df_fifa.dtypes

# Assingning appropriate datatypes
df_fifa = df_fifa.astype({'home_goals':int, 'away_goals':int})

# Final check to see if all data was entered properly
years3 = [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 
          1978, 1982, 1986, 1994, 1998, 2002, 2006, 2010, 2014, 2018]                             
for year in years3:
    print(year, len(df_fifa[df_fifa['year']==year]))

# Saving the files
df_fifa.to_csv('World_cup_data_cleaned.csv', index=False)
df_fixture.to_csv('World_cup_fixtures_2022_cleaned.csv', index=False)

from scipy.stats import poisson     

group_stage = pickle.load(open('groupstage', 'rb'))                # Group stage tables for 2022 world cup
df_world = pd.read_csv('World_cup_data_cleaned.csv')               # World cup results from all previous editions
df_plays = pd.read_csv('World_cup_fixtures_2022_cleaned.csv')      # Fixtures for all 2022 world cup games

group_stage['Group A']

df_home = df_world[['home','home_goals','away_goals']]
df_away = df_world[['away','home_goals','away_goals']]
df_home = df_home.rename(columns = {'home':'Team', 'home_goals':'Goals_scored', 'away_goals':'Goals_conceded'})
df_away = df_away.rename(columns = {'away':'Team', 'home_goals':'Goals_conceded', 'away_goals':'Goals_scored'})

df_away

# Calculating the average goals scored by team over the previous editions
df_avg_goals = pd.concat([df_home,df_away]).groupby('Team').mean()
df_avg_goals

# Creating a function to predict each matchup

def prediction(home, away):
    if home in df_avg_goals.index and away in df_avg_goals.index:
        lambda_home = df_avg_goals.at[home,'Goals_scored'] * df_avg_goals.at[away,'Goals_conceded']   # Multiplying goals scored and conceded to serve as the lambda function
        lambda_away = df_avg_goals.at[away,'Goals_scored'] * df_avg_goals.at[home,'Goals_conceded']
        prob_home_win, prob_away_win, prob_draw = 0, 0, 0                                             # Initial states for win, loss and draw
        for x in range(0,11):                                                                         # Range of zero to ten goals for the home team
            for y in range(0,11):                                                                     # Range of zero to ten goals for the away team
                p = poisson.pmf(x, lambda_home) * poisson.pmf(y, lambda_away)                         # Poisson distribution with lamda as above and x&y for homegoals & awaygoals
                if x==y:                                                                              # If draw
                    prob_draw += p
                elif x > y:                                                                           # If home win
                    prob_home_win += p
                else:                                                                                 # If away win
                    prob_away_win += p
        home_points = 3 * prob_home_win + prob_draw                                                   # 3 points for an home win
        away_points = 3 * prob_away_win + prob_draw                                                   # 3 points for an away win
        return (home_points, away_points)                                                             # 1 point each for a draw 
    else:
        return (0, 0)       

# Testing out the function
prediction('Argentina', 'Uruguay')

# Structuring the games based on level
df_group_stage = df_plays[:48].copy()        # Group stage games
df_R_16 = df_plays[48:56].copy()             # The round of 16 teams
df_Qf = df_plays[56:60].copy()               # The Quarter final games
df_Sf = df_plays[60:63].copy()               # The semi-final and 3rd place games
df_F = df_plays[63:].copy()                  # The final game

df_group_stage

for group in group_stage:
    team_names = group_stage[group]['Team'].values                                           # Get the name of each team
    df_group_games = df_group_stage[df_group_stage['home'].isin(team_names)]                 # Check if each team is in the group stage D.F and assign to new D.F
    for index, row in df_group_games.iterrows():                                             # For each row in the new D.F
        home, away = row['home'], row['away']                                                # The first team is at home and the second team is away
        home_points, away_points = prediction(home, away)                                    # Use the function to predict a game between home and away
        group_stage[group].loc[group_stage[group]['Team'] == home, 'Pts'] += home_points     # Find the corresponding team in the group table and assign home point
        group_stage[group].loc[group_stage[group]['Team'] == away, 'Pts'] += away_points     # Find the corresponding team in the group table and assign away point

    group_stage[group] = group_stage[group].sort_values('Pts', ascending=False)              # Re-arrange the group table based on points in descending order
    group_stage[group] = group_stage[group][['Team','Pts']]                                  # Show only the teams and their accumulated points
    group_stage[group] = group_stage[group].round(0)                                         # Round each accumulated point to the nearest whole number

group_stage['Group D']

df_R_16

for group in group_stage:
    group_winner = group_stage[group].loc[0, 'Team']                     # Assign the first team as the group winner
    runner_up = group_stage[group].loc[1, 'Team']                        # Assign the second team the runner up

    df_R_16.replace({f'Winners {group}': group_winner,                   # Replace values in the D.F with the appropriate group winner and runner up
                    f'Runners-up {group}': runner_up}, inplace=True)
df_R_16['winner'] = 'TBD' 
df_R_16  

def winner(round):
    for index, row in round.iterrows():                      # For each row
        home, away = row['home'], row['away']                # Find the home and away team
        points_home, points_away = prediction(home, away)    # Predict the score between both of them
        if points_home > points_away:                        # If the home team scores more
            winner = home                                    # Home team wins
        else:                                                # If the away team scores more
            winner = away                                    # Away team wins
        round.loc[index, 'winner'] = winner                  # Update the Qf column to reflect the winner
    return round

winner(df_R_16)

df_Qf

def next_stage(round_1, round_2):
    for index, row in round_1.iterrows():                               # For each row
        winner = round_1.loc[index, 'winner']                           # Find the winner in the winner column
        match = round_1.loc[index, 'score']                             # Find the match number in the score column
        round_2.replace({f'Winners {match}': winner}, inplace=True)     # Replace the home and away columns with the match number winners respectively
    round_2['winner'] = 'TBD'                                           # Add a winner column
    return round_2

next_stage(df_R_16, df_Qf)

winner(df_Qf)

next_stage(df_Qf, df_Sf)

winner(df_Sf)

# 3rd and 4th placed teams
prediction('Argentina', 'Portugal')

next_stage(df_Sf, df_F)

winner(df_F)
