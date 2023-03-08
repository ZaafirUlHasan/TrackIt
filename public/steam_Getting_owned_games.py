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
    print('Please ensure that the correct Steam ID was entered.')
    exit()


# Check if there was an error while getting user data
if (response1.status_code != 200) or (response2.status_code != 200): 
    print('Oops! We\'re having some trouble getting your data.')
    print('Try and recheck if your Steam profile is set to public so that we can access your data. If you\'re not sure how to do that, check out this video below:\nhttps://youtu.be/OM1DVv6sgt8?t=4')
          
else:
    # Extract the list of games
    games1 = data1['response']['games']
    data2 = response2.json()['applist']['apps']

    # Print the number of games
    print(f'Number of games: {len(games1)}')

    # Print the name and playtime for each game
    counter = 0
    for game1 in games1:
        counter += 1
        print(f'Data for game number {counter}')
        found = False
        for app2 in data2:
            if game1["appid"] == app2['appid']:
                found = True
                print(f"Playtime forever for {app2['name']} is {game1['playtime_forever']} minutes")
                if (game1['playtime_forever'] // 60) > 0 :
                    print(f'That\'s {timeConvertor(game1["playtime_forever"])}!')
                print()
            if found == True :
                break
