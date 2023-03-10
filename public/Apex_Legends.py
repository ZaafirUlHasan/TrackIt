import requests
import json
def timeConvertor(time): # Takes time in minutes as a parameter and returns a string that is formatted in terms of days, hours and minutes. Example return value: 8.0 days 6.0 hours and 15.0 minutes
    days = time // 1440
    if days >= 1:
        time -= (days * 1440)
    
    hours = time // 60
    if hours >= 1:
        time -= (hours * 60)
        
    minutes = time
    
    result = ""
    if days > 0:
        result += str(days) + " day"
        if days > 1:
            result += "s"
    if hours > 0:
        if result:
            result += ", "
        result += str(hours) + " hour"
        if hours > 1:
            result += "s"
    if minutes > 0:
        if result:
            result += " and "
        result += str(minutes) + " minute"
        if minutes > 1:
            result += "s"
    if not result:
        result = "0 minutes"
    
    return result


player = "InVuLMoNsTeR" # Other usernames that can be used for testing: DarkisKarma, Daltoosh (all psn players)
platform = "psn"  # 'psn' for Playstation , 'origin' for PC, and 'xbl' for Xbox

url = f"https://public-api.tracker.gg/v2/apex/standard/profile/{platform}/{player}?="

headers = {
  'TRN-Api-Key': '8f143659-336b-474c-9798-6d8564d2a316',
  'Cookie': '__cf_bm=_uDyLoMlBdCMRiTvOqtpR6zKyv0cLLNko_OT0wYnW.I-1677382263-0-AZ67sX8zljR/XyqtXKsnyi2L+NC5P8BGKjy6V4r0fNTZvMzS493SL+oMpWCaGAhvQ9+iggxcgqzZ1Ze9Ecohj0hhzrKXvlVIM99xlwGkZoFo; X-Mapping-Server=s13'
}

response = requests.get(url, headers = headers)

data = json.loads(response.text)

print("Stats".center(50, "-"))
counter = 0

for segment in data['data']["segments"]:
    if segment["type"] == "legend":
        counter += 1
        legend_name = segment["metadata"]["name"]
        kills = segment["stats"].get("kills", {}).get("value", 0)
        winning_kills = segment["stats"].get("winningKills", {}).get("value", 0)
        matches_played = segment["stats"].get("matchesPlayed", {}).get("value", 0)
        print(f"{counter}. {legend_name}")
        print("Kills:", int(kills))
        if winning_kills:
            print("Winning Kills:", int(winning_kills))
        if matches_played:
          print("Matches Played:", int(matches_played), "\n")
        print()


total_kills = data['data']['segments'][0]['stats']['kills']['value']
total_matches_played = data['data']['segments'][0]['stats']['matchesPlayed']['value']
approximatePlaytimeMinutes = total_matches_played * 15

print(f'Your lifetime kills are: {total_kills}')
print(f'Your lifetime matches played are: {total_matches_played}')
print(f'Based on an average match length of 15 minutes, your total playtime is approximately {approximatePlaytimeMinutes} minutes')
print(f'That\'s {timeConvertor(approximatePlaytimeMinutes)}!')


