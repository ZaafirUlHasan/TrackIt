import requests
import json

name = input()
tag = input()
profile = requests.get(f'https://api.henrikdev.xyz/valorant/v1/account/{name}/{tag}')
profile = json.loads(profile.content)
puuid = profile['data']['puuid']
print(profile['data']['account_level'])
print(profile['data']['card']['small'])
print(profile['data']['card']['wide'])
print(profile['data']['card']['large'])

matches = requests.get(f'https://api.henrikdev.xyz/valorant/v1/by-puuid/lifetime/matches/na/{puuid}')
matches = json.loads(matches.content)
numberOfmatches = matches['results']['total']
kills = 0
deaths = 0
i = 0
for j in range(0,len(matches['data'])):
    kills += matches['data'][i]['stats']['kills']
    deaths += matches['data'][i]['stats']['deaths']
    i+=1
print(f'Your estimated kill to death ratio over the past {numberOfmatches} matches is {kills/deaths:.2f}')