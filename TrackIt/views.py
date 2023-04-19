from flask import Blueprint, render_template, request, redirect, url_for

from jinja2 import Template
import json
import requests
from mojang import Client
from datetime import datetime

views = Blueprint(__name__, "views")

#Index
@views.route("index.html")
def goToIndex():
    return render_template("index.html")

#About
@views.route("About.html")
def goToAbout():
    return render_template("About.html")

#Roblox
@views.route("Roblox.html")
def goToRoblox():
    return render_template("Roblox.html")

@views.route('RobloxID', methods=['POST'])
def getRobloxID():
    user_id = request.form.get('user-id')
    return redirect(url_for('views.getRobloxStats', user_id=user_id))

@views.route('RobloxStats', methods=['GET', 'POST'])
def getRobloxStats():
    if request.method == 'POST':
        return redirect(url_for('views.getRobloxID'))
    try:
        user_id = request.args.get('user_id', '56592984')
        response = requests.get(f"https://games.roblox.com/v2/users/{user_id}/favorite/games?accessFilter=2&limit=10&sortOrder=Asc")
        data = response.json()
        game_list = {}
        for game in data["data"]:
            game_list[game['name']] = game['name']
        return render_template("myRobloxPage.html", title="My Roblox Page", heading="My Game List", game_list=game_list)
    except:
        return render_template("Roblox.html")

#Mojang
@views.route("Mojang.html")
def goToMojang():
    return render_template("Mojang.html")

@views.route('MojangID', methods=['POST'])
def getMojangID():
    user_id = request.form.get('user-id')
    password = request.form.get('password')
    return redirect(url_for('views.getMojangStats', user_id=user_id, password=password))

@views.route('MojangStats', methods=['GET', 'POST'])
def getMojangStats():
    if request.method == 'POST':
        return redirect(url_for('views.getMojangID'))
    try:
        #Placeholder, it is my minecraft account, user input will be needed.
        user_id = request.args.get('user_id', 'evanpalubinski@gmail.com')
        password = request.args.get('password', 'Binski55')
        client = Client(user_id, password)
        #Getting the NameInformation class object
        name_change_info = client.get_name_change_info()

        #Extract the creation date from the name_change_info dictionary
        creation_date = (f'Created on {datetime.strptime(name_change_info.created_at, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")}')

        return render_template("myMojangPage.html", game=creation_date)
    except:
        return render_template("Mojang.html")

#Steam
@views.route("Steam.html")
def goToSteam():
    return render_template("Steam.html")

@views.route('SteamID', methods=['POST'])
def getSteamID():
    user_id = request.form.get('user-id')
    return redirect(url_for('views.getSteamStats', user_id=user_id))

@views.route('SteamStats', methods=['GET', 'POST'])
def getSteamStats():
    if request.method == 'POST':
            return redirect(url_for('views.getSteamID'))
    try:
        game_playtime = {}
        user_id = request.args.get('user_id', '76561197960434622')
        steam_id = int(user_id)
        api_key = '5D5EC3147B58B6B3BBB3F23BC5A64E6F'
        url1 = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}&format=json'
        url2 = f'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
        response1 = requests.get(url1)
        response2 = requests.get(url2)
        data1 = response1.json()
        games1 = data1['response']['games']
        data2 = response2.json()['applist']['apps']
        numberOfGames = (f'Number of games: {len(games1)}')
        for game1 in games1:
            for app2 in data2:
                if game1["appid"] == app2['appid']:
                    game_name = app2['name']
                    playtime = game1['playtime_forever']
                    game_playtime[game_name] = playtime
                    break
        return render_template("mySteamPage.html", title="My Steam Page", heading="My Game List", game_playtime=game_playtime)
    except:
        return render_template("Steam.html")

#LeagueOfLegends
@views.route("LeagueOfLegends.html")
def goToLeagueOfLegends():
    return render_template("LeagueOfLegends.html")

@views.route('LeagueOfLegendsID', methods=['POST'])
def getLeagueOfLegendsID():
    user_id = request.form.get('user-id')
    region = request.form.get('region')
    return redirect(url_for('views.getLeagueOfLegendsStats', user_id=user_id, region=region))

@views.route('LeagueOfLegendsStats', methods=['GET', 'POST'])
def getLeagueOfLegendsStats():
    if request.method == 'POST':
            return redirect(url_for('views.getLeagueOfLegendsID'))
    try:
        summoner_name = request.args.get('user_id')
        api_key = "RGAPI-c693b3ed-8b35-4418-92ad-6fa9189a650e"
        region = request.args.get('region')
        url = "https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_name + "?api_key=" + api_key
        response = requests.get(url)
        summoner_info = json.loads(response.content)
        summoner_id = summoner_info["id"]
        url = "https://" + region + ".api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/" + summoner_id + "?api_key=" + api_key
        response = requests.get(url)
        champ_mastery_list = json.loads(response.content)
        url = "https://" + region + ".api.riotgames.com/lol/league/v4/entries/by-summoner/" + summoner_id + "?api_key=" + api_key
        response = requests.get(url)
        rank_info = json.loads(response.content)
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
        return render_template("myLeagueOfLegendsPage.html", title="My League of Lengends Stats", heading="My Game Stats", statDict=statDict)
    except:
        return render_template("LeagueOfLegends.html")

    
