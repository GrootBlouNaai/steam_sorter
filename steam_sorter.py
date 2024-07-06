import requests
import pandas as pd


USER_API_KEY = 'INSERT STEAM API KEY'
USER_STEAM_ID = 'INSERT STEAM ID'

# Fetch the list of all Steam apps
def fetch_app_list():
    api = 'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
    res = requests.get(url=api)
    return {game['appid']: game['name'] for game in res.json()['applist']['apps']}

# Get the name of a game by its app ID
def get_game_name(app_id, app_list):
    return app_list.get(app_id, "Unknown Game")

# Get the score of a game by its app ID
def get_game_score(app_id):
    url = f'https://store.steampowered.com/appreviews/{app_id}?json=1'
    data = requests.get(url).json()
    if 'query_summary' in data:
        query_summary = data['query_summary']
        total_positive = query_summary.get('total_positive', 0)
        total_reviews = query_summary.get('total_reviews', 1)
        return total_positive / total_reviews
    return 0

# Fetch the list of games owned by a user
def fetch_user_games(api_key, steam_id):
    url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}&format=json'
    user_game_data = requests.get(url).json()
    if 'response' in user_game_data and 'games' in user_game_data['response']:
        return [game['appid'] for game in user_game_data['response']['games']]
    return []

def main():
    app_list = fetch_app_list()
    games_owned_id = fetch_user_games(USER_API_KEY, USER_STEAM_ID)

    my_games_and_user_scores = {}
    for game_id in games_owned_id:
        try:
            game_name = get_game_name(game_id, app_list)
            game_score = get_game_score(game_id)
            my_games_and_user_scores[game_name] = game_score
        except Exception as e:
            print(f"Error processing game ID {game_id}: {e}")

    df = pd.DataFrame(my_games_and_user_scores.items(), columns=('Game', 'User Score'))
    df.sort_values(by='User Score', inplace=True, ascending=False, ignore_index=True)
    df.to_csv('~/Games/Dumps/Accounts/Share/games.csv', index=False)

if __name__ == "__main__":
    main()
