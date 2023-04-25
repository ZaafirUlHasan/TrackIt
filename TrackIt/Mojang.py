from flask import Blueprint, render_template, request, redirect, url_for, current_app
import requests
import os
from mojang import Client
from datetime import datetime

Mojang = Blueprint(__name__, "Mojang")

@Mojang.route("Mojang.html")
def goToMojang():
    return render_template("Mojang.html")

@Mojang.route('MojangID', methods=['POST'])
def getMojangID():
    user_id = request.form.get('user-id')
    password = request.form.get('password')
    user_name = request.form.get('user-name')
    return redirect(url_for('Mojang.getMojangStats', user_id=user_id, password=password, user_name=user_name))

@Mojang.route('MojangStats', methods=['GET', 'POST'])
def getMojangStats():
    if request.method == 'POST':
        return redirect(url_for('Mojang.getMojangID'))
    try:
        #Placeholder, it is my minecraft account, user input will be needed.
        user_id = request.args.get('user_id', 'evanpalubinski@gmail.com')
        password = request.args.get('password', 'Binski55')
        user_name= request.args.get('user_name', 'DJSALADD')
        client = Client(user_id, password)
        #Getting the NameInformation class object
        name_change_info = client.get_name_change_info()

        #Extract the creation date from the name_change_info dictionary
        creation_date = (f'Created on {datetime.strptime(name_change_info.created_at, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")}')

        uuid_response = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{user_name}')
        uuid = uuid_response.json()['id']
        skin_response = requests.get(f'https://crafatar.com/skins/{uuid}')
        static_path = os.path.join(current_app.root_path, "static")
        with open(os.path.join(static_path, "image.jpg"), "wb") as f:
            f.write(skin_response.content)
        image = "/static/image.jpg"

        return render_template("myMojangPage.html", game=creation_date,img_data=image,heading="My Minecraft Skin")
    except:
        return render_template("Mojang.html")