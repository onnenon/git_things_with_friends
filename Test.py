import json
import requests


def get_roster_players_info_string(player_infos):
    if player_infos is None:
        return "No players found"
    return "\n".join(
        [
            f"{",".join(player["fantasy_positions"])} {player["first_name"]} {player["last_name"]}"
            for player in player_infos
        ]
    )


def get_player_infos_for_roster(player_ids, rosters, user_id):
    roster_players = [
        roster["players"] for roster in rosters if roster["owner_id"] == user_id
    ][0]

    if roster_players is None:
        return None

    return [player_ids[player] for player in roster_players]


with open("players.json", "r") as f:
    player_ids = json.load(f)


user_response = requests.get("https://api.sleeper.app/v1/user/TakeM3Higher")
user_id = user_response.json()["user_id"]

league_response = requests.get(
    f"https://api.sleeper.app/v1/user/{user_id}/leagues/nfl/2024"
)
league_ids = [x["league_id"] for x in league_response.json()]


for league_id in league_ids:
    league_info = requests.get(f"https://api.sleeper.app/v1/league/{league_id}")
    league_name = league_info.json()["name"]
    roster_response = requests.get(
        f"https://api.sleeper.app/v1/league/{league_id}/rosters"
    )

    print(f"\nPlayers in {league_name}: \n")
    roster_player_infos = get_player_infos_for_roster(
        player_ids, roster_response.json(), user_id
    )

    print(get_roster_players_info_string(roster_player_infos))
