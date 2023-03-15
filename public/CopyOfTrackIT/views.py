from flask import Blueprint, render_template, request, redirect, url_for

from jinja2 import Template
import json
import requests

views = Blueprint(__name__, "views")

@views.route("index.html")
def goToIndex():
    return render_template("index.html")

@views.route("About.html")
def goToAbout():
    return render_template("About.html")

@views.route("Roblox.html")
def goToRoblox():
    return render_template("Roblox.html")

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

@views.route('RobloxID', methods=['POST'])
def getRobloxID():
    user_id = request.form.get('user-id')
    return redirect(url_for('views.getRobloxStats', user_id=user_id))

@views.route("Steam.html")
def goToSteam():
    return render_template("Steam.html")

@views.route('SteamStats', methods=['GET', 'POST'])
def getSteamStats():
    pass
    if request.method == 'POST':
            return redirect(url_for('views.getSteamID'))


@views.route('Steam', methods=['POST'])
def getSteamID():
    pass
    user_id = request.form.get('user-id')
    return redirect(url_for('views.getSteamStats', user_id=user_id))


