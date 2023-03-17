import requests
import json

# get summoner ID
summoner_name = input("Enter summoner name: ")
api_key = "RGAPI-c693b3ed-8b35-4418-92ad-6fa9189a650e"
region = input("Region: ")
url = "https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_name + "?api_key=" + api_key
response = requests.get(url)
summoner_info = json.loads(response.content)
summoner_id = summoner_info["id"]

# get champion mastery data
url = "https://" + region + ".api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/" + summoner_id + "?api_key=" + api_key
response = requests.get(url)
champ_mastery_list = json.loads(response.content)

# get summoner rank data
url = "https://" + region + ".api.riotgames.com/lol/league/v4/entries/by-summoner/" + summoner_id + "?api_key=" + api_key
response = requests.get(url)
rank_info = json.loads(response.content)

# create  dicionary with playtime hours and rank information
statDict = {}
if rank_info:
    statDict["playtime_hours"] = round(sum([int(champ_mastery['championPoints']) for champ_mastery in champ_mastery_list])/60, 2)
    statDict["rank_information"] = []
    for rank in rank_info:
        queue_type = rank["queueType"]
        tier = rank["tier"]
        rank = rank["rank"]
        lp = str(rank_info[0]["leaguePoints"]) + " LP"
        rank_info_str = queue_type + " - " + tier + " " + rank + " (" + lp + ")"
        statDict["rank_information"].append(rank_info_str)
        
print(statDict)
