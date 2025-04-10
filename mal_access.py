import requests
from config import MAL_KEY

auth = {"X-MAL-CLIENT-ID": MAL_KEY}

# TODO: Handle exceptions of requests module
def get_seasonal_anime(year, season, limit=100):
    params = {
        "nsfw": "true",
        "sort": "anime_num_list_users",
        "limit": limit,
        "fields": "id,title,num_list_users,media_type"
    }
    response = requests.get(f'https://api.myanimelist.net/v2/anime/season/{year}/{season}', headers=auth, params=params)
    return response.json()


def get_upcoming_anime(limit=50):
    params = {
        "ranking_type": "upcoming",
        "limit": limit,
        "fields": "id,title,num_list_users,media_type,related_anime"
    }
    response = requests.get('https://api.myanimelist.net/v2/anime/ranking', headers=auth, params=params)
    return response.json()


def get_anime_details(anime_id):
    params = {
        "fields": "related_anime"
    }
    response = requests.get(f'https://api.myanimelist.net/v2/anime/{anime_id}', headers=auth, params=params)
    return response.json()