from flask import Blueprint, render_template, request, redirect, url_for, current_app
import requests
from mojang import Client

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
        #Getting user inputs
        user_id = request.args.get('user_id')
        password = request.args.get('password')
        user_name= request.args.get('user_name')
        #Getting the NameInformation class object
        client = Client(user_id, password)
        name_change_info = client.get_name_change_info()
        #Extract the creation date from the name_change_info dictionary
        creation_date = name_change_info.created_at.strftime("%d-%m-%y")
        creation_format = "The Minecraft account was created on "+creation_date
        uuid_response = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{user_name}')
        uuid = uuid_response.json()['id']
        skin = (f'https://crafatar.com/skins/{uuid}')
        cape =(f'https://crafatar.com/capes/{uuid}')
        body = (f'https://crafatar.com/renders/body/{uuid}')
        avatar = (f'https://crafatar.com/avatars/{uuid}')
        return render_template("myMojangPage.html", date=creation_format,skin=skin, cape=cape, body=body, avatar=avatar,
                               skin_heading="Skin",cape_heading="Cape", body_heading="Body", avatar_heading="Avatar")
    except:
        return render_template("Mojang.html")
