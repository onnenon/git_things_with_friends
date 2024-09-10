import requests
import json

player_response = requests.get("https://api.sleeper.app/v1/players/nfl")

with open("players.json", "w") as file:
    file.write(json.dumps(player_response.json(), indent=4))
