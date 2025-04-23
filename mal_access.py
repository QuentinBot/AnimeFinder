import requests
import sys

from config import MAL_KEY


auth = {"X-MAL-CLIENT-ID": MAL_KEY}


def get_seasonal_anime(year, season, limit=100):
    params = {
        "nsfw": "true",
        "sort": "anime_num_list_users",
        "limit": limit,
        "fields": "id,title,num_list_users,media_type"
    }
    response = get_api_response(f"season/{year}/{season}", params=params)
    return response


def get_upcoming_anime(limit=50):
    params = {
        "ranking_type": "upcoming",
        "limit": limit,
        "fields": "id,title,num_list_users,media_type,related_anime"
    }
    response = get_api_response("ranking", params=params)
    return response


def get_anime_details(anime_id):
    params = {
        "fields": "related_anime"
    }
    response = get_api_response(anime_id, params=params)
    return response


def get_api_response(endpoint, params=None):
    for _ in range(3):  # Retry up to 3 times
        try:
            response = requests.get(f'https://api.myanimelist.net/v2/anime/{endpoint}', headers=auth, params=params)
            return response.json()
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Retrying...")
            sys.sleep(5)
    
    return None  