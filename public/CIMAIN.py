pip install requests
import requests

response = requests.get("/riot/account/v1/accounts/by-puuid/{puuid}")
print(response.status_code)

