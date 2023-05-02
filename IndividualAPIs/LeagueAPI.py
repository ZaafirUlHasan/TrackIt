import requests
import json
from PIL import Image
from io import BytesIO

def get_champion_name(champ_id):
    with open('champion_names.txt') as f:
        for line in f:
            data = line.strip().split()
            if int(data[1]) == champ_id:
                return data[0]
    return "Champion not found"

# Get summoner ID
summoner_name = input("Enter summoner name: ")
api_key = "RGAPI-c693b3ed-8b35-4418-92ad-6fa9189a650e"
region = input("Region: ")

url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}"
response = requests.get(url)
summoner_info = json.loads(response.content)
summoner_id = summoner_info["id"]
player_level = summoner_info["summonerLevel"]
icon_id = summoner_info["profileIconId"]

# Get champion mastery data
url = f"https://{region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}?api_key={api_key}"
response = requests.get(url)
champ_mastery_list = json.loads(response.content)

# Get top 5 champion mastery data
top_5_champs = sorted(champ_mastery_list, key=lambda x: x["championPoints"], reverse=True)[:5]

# Get summoner rank data
url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api_key}"
response = requests.get(url)
rank_info = json.loads(response.content)

# Create statDict dictionary with playtime hours, rank information, and player level
statDict = {}
if rank_info:
    playtime_hours = round(sum([int(champ_mastery['championPoints']) for champ_mastery in champ_mastery_list]) / 3600, 2)
    statDict["playtime_hours"] = playtime_hours

    statDict["rank_information"] = []
    for rank in rank_info:
        queue_type = rank["queueType"]
        tier = rank["tier"]
        rank = rank["rank"]
        lp = f"{rank_info[0]['leaguePoints']} LP"
        rank_info_str = f"{queue_type} - {tier} {rank} ({lp})"
        statDict["rank_information"].append(rank_info_str)

if player_level:
    statDict["player_level"] = player_level

# Get summoner icon URL and display the icon
if icon_id:
    icon_url = f"https://cdn.communitydragon.org/latest/profile-icon/{icon_id}"
    icon_response = requests.get(icon_url)
    icon_image = Image.open(BytesIO(icon_response.content))
    icon_image.show()

# Print statDict in a nice format
print("Summoner Stats:")
print("-" * 50)
if "player_level" in statDict:
    print(f"Player Level: {statDict['player_level']}")
if "playtime_hours" in statDict:
    print(f"Playtime Hours: {statDict['playtime_hours']} hours")
if "rank_information" in statDict:
    print("Rank Information:")
    for rank in statDict["rank_information"]:
        print(f"\t- {rank}\n")
if top_5_champs:
    print("Top 5 Champion Mastery:")
    for i, champ in enumerate(top_5_champs):
        champion_name = get_champion_name(champ['championId'])
        print(f"{i+1}. {champion_name} - Level {champ['championLevel']} - {champ['championPoints']} points")