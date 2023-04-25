from flask import Blueprint, render_template, request, redirect, url_for, current_app
import os
import requests
from jinja2 import Template
import json

LeagueOfLegends = Blueprint(__name__, "LeagueOfLegends")

#LeagueOfLegends
@LeagueOfLegends.route("LeagueOfLegends.html")
def goToLeagueOfLegends():
    return render_template("LeagueOfLegends.html")

@LeagueOfLegends.route('LeagueOfLegendsID', methods=['POST'])
def getLeagueOfLegendsID():
    user_id = request.form.get('user-id')
    region = request.form.get('region')
    return redirect(url_for('LeagueOfLegends.getLeagueOfLegendsStats', user_id=user_id, region=region))

@LeagueOfLegends.route('LeagueOfLegendsStats', methods=['GET', 'POST'])
def getLeagueOfLegendsStats():
    if request.method == 'POST':
            return redirect(url_for('LeagueOfLegends.getLeagueOfLegendsID'))
    try:
        summoner_name = request.args.get('user_id')
        api_key = "RGAPI-c693b3ed-8b35-4418-92ad-6fa9189a650e"
        region = request.args.get('region')
        url = "https://" + region + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner_name + "?api_key=" + api_key
        response = requests.get(url)
        summoner_info = json.loads(response.content)
        summoner_id = summoner_info["id"]
        player_level = summoner_info["summonerLevel"]
        icon_id = summoner_info["profileIconId"]
        url = "https://" + region + ".api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/" + summoner_id + "?api_key=" + api_key
        response = requests.get(url)
        champ_mastery_list = json.loads(response.content)
        url = "https://" + region + ".api.riotgames.com/lol/league/v4/entries/by-summoner/" + summoner_id + "?api_key=" + api_key
        response = requests.get(url)
        rank_info = json.loads(response.content)
        statDict = {}
        if rank_info:
            statDict["Playtime (Minutes)"] = round(sum([int(champ_mastery['championPoints']) for champ_mastery in champ_mastery_list])/60, 2)
            statDict["Rank"] = []
            for rank in rank_info:
                queue_type = rank["queueType"]
                tier = rank["tier"]
                rank = rank["rank"]
                lp = str(rank_info[0]["leaguePoints"]) + " LP"
                rank_info_str = queue_type + " - " + tier + " " + rank + " (" + lp + ")"
                statDict["Rank"].append(rank_info_str)
        if player_level:
            statDict["Player Level"] = player_level
        if icon_id:
            icon_url = f"https://cdn.communitydragon.org/latest/profile-icon/{icon_id}"
            icon_response = requests.get(icon_url)
            static_path = os.path.join(current_app.root_path, "static")
            with open(os.path.join(static_path, "image.jpg"), "wb") as f:
                f.write(icon_response.content)
            image = "/static/image.jpg"

        return render_template("myLeagueOfLegendsPage.html", title="My League of Lengends Stats", heading=f"{summoner_name}'s Game Stats", statDict=statDict, image = image)
    except:
        return render_template("LeagueOfLegends.html")