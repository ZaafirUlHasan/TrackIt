from jinja2 import Template
import json
import requests

def timeConvertor(time):
    days = time // 1440
    if days >= 1:
        time -= (days * 1440)
    
    hours = time // 60
    if hours >= 1:
        time -= (hours * 60)
        
    minutes = time
    
    result = ""
    if days > 0:
        result += str(days) + " day"
        if days > 1:
            result += "s"
    if hours > 0:
        if result:
            result += ", "
        result += str(hours) + " hour"
        if hours > 1:
            result += "s"
    if minutes > 0:
        if result:
            result += " and "
        result += str(minutes) + " minute"
        if minutes > 1:
            result += "s"
    if not result:
        result = "0 minutes"
    
    return result

try:
    steam_id = 76561197960434622
    api_key = '5D5EC3147B58B6B3BBB3F23BC5A64E6F'

    url1 = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}&format=json'
    url2 = f'https://api.steampowered.com/ISteamApps/GetAppList/v2/'

    response1 = requests.get(url1)
    response2 = requests.get(url2)
    data1 = response1.json()

except:
    value = ('Please ensure that the correct Steam ID was entered.')
    exit()

# Check if there was an error while getting user data
if (response1.status_code != 200) or (response2.status_code != 200): 
    value = ('Oops! We\'re having some trouble getting your data.')
          
else:
    # Extract the list of games
    games1 = data1['response']['games']
    data2 = response2.json()['applist']['apps']

    # Print the number of games
    print(f'Number of games: {len(games1)}')

    # Print the name and playtime for each game
    counter = 0
    gameListSteam = {}
    for game1 in games1:
        counter += 1
        print(f'Data for game number {counter}')
        found = False
        for app2 in data2:
            if game1["appid"] == app2['appid']:
                found = True
                print(f"Playtime forever for {app2['name']} is {game1['playtime_forever']} minutes")
                ##  Creates a dictionary with the name of the Steam game as they key and playime as value
                gameListSteam[app2['name']] = game1['playtime_forever']
                if (game1['playtime_forever'] // 60) > 0 :
                    print(f'That\'s {timeConvertor(game1["playtime_forever"])}!')
                print()
            if found == True :
                break

###Roblox
user_id = "56592984"

# Send a GET request to the API endpoint
response = requests.get(f"https://games.roblox.com/v2/users/{user_id}/favorite/games?accessFilter=2&limit=10&sortOrder=Asc")

# Check if the request was successful
if response.status_code != 200:
    print("Failed to get favorite games.")
    exit()

# Parse the response as JSON
data = response.json()

# Print the user's favorite games
game_list = {}
for game in data["data"]:
    game_list[game['name']] = game['name']

template1 = Template('''
<html>
<head>
  <title>{{ title }}</title>
</head>
<body>
  <h1>{{ heading }}</h1>
  {% for game in game_list %}
  <p>{{ game }}</p>
  {% endfor %}
</body>
</html>
''')

data1 = {
    'title': "hi",
    'heading': f"Favorite Games on Roblox",
    'game_list': game_list
}

html = template1.render(data1)

template2 = Template('''
<html>
<head>
  <title>{{ title }}</title>
</head>
<body>
  <h1>{{ heading }}</h1>
  {% for key, value in gameListSteam.items() %}
  <p>{{ key }}:{{ value }} minutes</p>
  {% endfor %}
</body>
</html>
''')

data2 = {
    'title': "hi",
    'heading': f"Steam Playtimes",
    'gameListSteam': gameListSteam,
    'minutes':'minutes'
}

html2 = template2.render(data2)

with open('my_page.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('my_page.html', 'a', encoding='utf-8') as f:
    f.write(html2)
