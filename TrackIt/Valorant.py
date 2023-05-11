from flask import Blueprint, render_template, request, redirect, url_for
import requests
from jinja2 import Template
import json

Valorant = Blueprint(__name__, "Valorant")

@Valorant.route("Valorant.html")
def goToValorant():
    return render_template("Valorant.html")

@Valorant.route("ValorantID", methods= ['POST'])
def getValorantID():
    user_id = request.form.get('user-id')
    tag = request.form.get('tag')
    return redirect(url_for('Valorant.getValorantStats', user_id=user_id, tag = tag))

@Valorant.route("ValorantID", methods= ['GET', 'POST'])
def getValorantStats():
    if request.method == 'POST':
        return redirect(url_for('Valorant.getValorantID'))
    try:
        name = request.args.get('user_id')
        tag = request.args.get('tag')
        profile = requests.get(f'https://api.henrikdev.xyz/valorant/v1/account/{name}/{tag}')
        profile = json.loads(profile.content)
        puuid = profile['data']['puuid']
        accountLevel = (profile['data']['account_level'])
        widePic = profile['data']['card']['wide']
        matches = requests.get(f'https://api.henrikdev.xyz/valorant/v1/by-puuid/lifetime/matches/na/{puuid}')
        matches = json.loads(matches.content)
        icons = []
        numberOfmatches = matches['results']['total']
        kills = 0
        deaths = 0
        i = 0
        for j in range(0,len(matches['data'])):
            kills += matches['data'][i]['stats']['kills']
            deaths += matches['data'][i]['stats']['deaths']
            i+=1
        estimate = (f'Your estimated kill to death ratio over the past {numberOfmatches} matches is {kills/deaths:.2f}')
        return render_template("myValorantPage.html", title = "my Valorant Stats", accountLevel = accountLevel, estimate = estimate, heading = "My Valorant Stats",img = widePic )
    except:
        return render_template("Valorant.html")
 
