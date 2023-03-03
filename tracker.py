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
for game in data["data"]:
    print(f"Favorite game: {game['name']} (ID: {game['rootPlace']['id']})")

