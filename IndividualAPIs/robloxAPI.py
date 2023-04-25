import requests
from PIL import Image
from io import BytesIO

try:
    user_id = input('Enter ID')
    
    response = requests.get(f'https://thumbnails.roblox.com/v1/users/avatar?userIds={user_id}&size=250x250&format=Png&isCircular=false')
    data = response.json()
    img_data = data["data"][0]["imageUrl"]
    img_response = requests.get(img_data)
    image = Image.open(BytesIO(img_response.content))
    image.show()
    
    response = requests.get(f"https://games.roblox.com/v2/users/{user_id}/favorite/games?accessFilter=2&limit=10&sortOrder=Asc")
    data = response.json()
    game_list = {}
    for game in data["data"]:
        game_list[game['name']] = game['name']
        print(game['name'])
    
    response = requests.get(f"https://badges.roblox.com/v1/users/{user_id}/badges?limit=10&sortOrder=Asc")
    data = response.json()
    badges = {}
    for badge in data['data']:
        badges[badge['name']] = badge['name']
        print(badge['name'],'\n')
except:
    print('error')

