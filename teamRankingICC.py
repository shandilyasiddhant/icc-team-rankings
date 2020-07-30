from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import datetime

print("Please read the instructions carefully!!!")
print("Team Ranking for which one of the following are you looking for?")

competion_for = input("\nEnter 'mens' for MENS TEAM & 'womens' for WOMENS TEAM    :")

print("\nPLEASE NOTE: ICC does not release ranking for WOMEN'S TEST Matches")
print("\nSo format option for womens is limited to 't20i' and 'odi' ")

game_format = input("\nEnter t20i for T20I, enter odi for ODI, enter test for TEST:   ")

# creating link to be scraped using input provided by the user
full_url = "https://www.icc-cricket.com/rankings/" + competion_for + "/team-rankings/" + game_format

print(full_url)
print()

# checking/loading webpage content
response = requests.get(full_url)

if response.status_code == 200:
    print("Please wait while Data is being Scraped!")

    # parsing webpage
    soup = bs(response.text, 'html.parser')

    # targeting the desired content on webpage
    table = soup.find('div', {'class': 'rankings-block__container full rankings-table'})

    # empty lists: to be appended for each table content
    team = []
    match = []
    point = []
    rating = []

    # Teams
    teams_pc = table.find_all('span', {'class': 'u-hide-phablet'})

    # Matches: odd ones' in the list
    matches_and_points = table.find_all('td', {'class': 'table-body__cell u-center-text'})

    # Rating
    rating_pc = table.find_all('td', {'class': 'table-body__cell u-text-right rating'})

    # for row I: class for 1st row and rest of the rows vary significantly
    rowI = soup.find('tr', {'class': 'rankings-block__banner'})
    match_rowI = rowI.find('td', {'class': 'rankings-block__banner--matches'})
    point_rowI = rowI.find('td', {'class': 'rankings-block__banner--points'})
    rating_rowI = rowI.find('td', {'class': 'rankings-block__banner--rating u-text-right'})
    match.append(match_rowI.text)
    point.append(point_rowI.text)
    rating.append(rating_rowI.text.replace('\n', '').strip())

    # for rest of the rows
    # appending to empty list 'team' for all teams
    team = [t.text for t in teams_pc]

    # appending to empty list 'match' & 'point' for team ranked 2nd to 10th
    i = 0
    for m in matches_and_points:
        if i in range(0, 200, 2):
            match.append(m.text)
        else:
            point.append(m.text)
        i += 1

    # list of ratings for team ranked 2nd to 10th
    rating_teams = [rating.append(r.text) for r in rating_pc]

    # converting different lists to set of tuples
    data_team_ranking = list(zip(team, match, point, rating))

    # creating DataFrame to be written to Excel
    d = pd.DataFrame(data_team_ranking, columns=['Team', 'Match', 'Points', 'Ratings'])

    # changing header name (default: blank)
    d.index.names = ['Position']

    # default row index starts at 0, changing row index to start at 1
    d.index += 1

    # defining sheet name
    sheet_name = "Team Ranking" + "_" + competion_for + "_" + game_format

    # Writing the dataframe to a new Excel file
    try:
        d.to_excel('ICC Data_Team' + datetime.datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p") + '.xlsx',
                   sheet_name=sheet_name)  # filename

    except:
        print("\nSomething went wrong! Please check your code.")  # error msg

    else:
        print("\nWeb data successfully written to Excel.")

    finally:
        print("\nQuitting the program!")

else:
    print("Please re-start the program and enter details carefully!")