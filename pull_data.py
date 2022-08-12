import json
import urllib.request as request
import itertools

DRAFT_ID = 860369702336180224
LEAGUE_ID = 860369701656707072


def get_league_users(league_id):
    contents = request.urlopen(f"https://api.sleeper.app/v1/league/{league_id}/users").read()
    return json.loads(contents)


def get_draft_picks(draft_id):
    contents = request.urlopen(f"https://api.sleeper.app/v1/draft/{draft_id}/picks").read()
    return json.loads(contents)


def load_players():
    with open("players.json") as f:
        return json.loads(f.read())


users = get_league_users(LEAGUE_ID)
players = load_players()
picks = get_draft_picks(DRAFT_ID)

# Merge draft pick json with league user data
for pick in picks:
    user_id = pick["picked_by"]
    pick["user"] = next(u for u in users if u["user_id"] == user_id)

# Merge draft pick json with cached player data
for pick in picks:
    picked_player_id = pick["player_id"]
    pick["player"] = players[picked_player_id]

age = []
grouped_picks = {k: list(v) for k, v in itertools.groupby(sorted(picks, key=lambda x: x["picked_by"]), key=lambda x: x["picked_by"])}
for user_id, user_picks in grouped_picks.items():
    # Turn the groupby into a list, so we can work on it
    total_age = sum(p["player"]["age"] for p in user_picks)

    avg_age = total_age / len(user_picks)

    age.append((user_id, avg_age, user_picks[0]["user"]))

sorted_ages = sorted(age, key=lambda x: x[1], reverse=True)

for age in sorted_ages:
    print(f"{age[2]['display_name']}: {age[1]}")


