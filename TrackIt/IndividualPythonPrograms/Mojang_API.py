from mojang import Client
import requests
from PIL import Image
from io import BytesIO

#Placeholder, it is my minecraft account, user input will be needed.
client = Client("evanpalubinski@gmail.com", "Binski55")
#Getting the NameInformation class object
name_change_info = client.get_name_change_info()

#Extract the creation date from the name_change_info dictionary
creation_date = name_change_info.created_at.strftime("%d-%m-%y")
print(f"The Minecraft account was created on {creation_date}")

username = 'DJSALADD'

# Get the player's UUID
uuid_response = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}')
uuid_response.raise_for_status()
uuid = uuid_response.json()['id']

# Get the player's skin
skin_response = requests.get(f'https://crafatar.com/skins/{uuid}')
skin_response.raise_for_status()
skin_image = Image.open(BytesIO(skin_response.content))
skin_image.show()

# Get the player's cape (if any)
cape_response = requests.get(f'https://crafatar.com/capes/{uuid}')
if cape_response.status_code == 404:
    print(f'{username} does not have a cape.')
else:
    cape_response.raise_for_status()
    cape_image = Image.open(BytesIO(cape_response.content))
    cape_image.show()
