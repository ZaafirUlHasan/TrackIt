from flask import Blueprint, render_template, request, redirect, url_for
import requests
roblox = Blueprint(__name__, "roblox")

@roblox.route("Roblox.html")
def goToRoblox():
    return render_template("Roblox.html")

@roblox.route('RobloxID', methods=['POST'])
def getRobloxID():
    user_id = request.form.get('user-id')
    return redirect(url_for('roblox.getRobloxStats', user_id=user_id))

@roblox.route('RobloxStats', methods=['GET', 'POST'])
def getRobloxStats():
    if request.method == 'POST':
        return redirect(url_for('roblox.getRobloxID'))
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
