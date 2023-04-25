from flask import Blueprint, render_template, request, redirect, url_for
import requests
from jinja2 import Template
import json

Steam = Blueprint(__name__, "Steam")

@Steam.route("Steam.html")
def goToSteam():
    return render_template("Steam.html")

@Steam.route('SteamID', methods=['POST'])
def getSteamID():
    user_id = request.form.get('user-id')
    return redirect(url_for('Steam.getSteamStats', user_id=user_id))

@Steam.route('SteamStats', methods=['GET', 'POST'])
def getSteamStats():
    if request.method == 'POST':
            return redirect(url_for('Steam.getSteamID'))
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

