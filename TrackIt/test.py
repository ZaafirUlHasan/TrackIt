from jinja2 import Template
import json
import requests

user_id = "56592984"

# Send a GET request to the API endpoint
response = requests.get(f"https://games.roblox.com/v2/users/{user_id}/favorite/games?accessFilter=2&limit=10&sortOrder=Asc")

# Check if the request was successful
if response.status_code != 200:
    print("Failed to get favorite games.")
    exit()

# Parse the response as JSON
data = response.json()

# Print the user's favorite games
game_list = {}
for game in data["data"]:
    game_list[game['name']] = game['name']

template = Template('''
<html>
<head>
  <title>{{ title }}</title>
</head>
<body>
  <h1>{{ heading }}</h1>
  {% for game in game_list %}
  <p>{{ game }}</p>
  {% endfor %}
</body>
</html>
''')

data1 = {
    'title': "hi",
    'heading': f"hi",
    'game_list': game_list
}

html = template.render(data1)

with open('my_page.html', 'w', encoding='utf-8') as f:
    f.write(html)