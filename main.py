import requests
from config import MAL_KEY


auth = {"X-MAL-CLIENT-ID": MAL_KEY}
min_users_threshold = 10000


def get_seasonal(year, season):
    params = {"nsfw": "true", "sort": "anime_num_list_users", "limit": 100, "fields": "id,title,num_list_users,media_type"}
    response = requests.get(f'https://api.myanimelist.net/v2/anime/season/{year}/{season}', headers=auth, params=params)
    return response.json()


def get_details(id):
    params = {"fields": "related_anime"}
    response = requests.get(f'https://api.myanimelist.net/v2/anime/{id}', headers=auth, params=params)
    return response.json()


def filter_prequel(data):
    prequels = []
    for anime in data["data"]:
        details = get_details(anime["node"]["id"])
        if anime["node"]["num_list_users"] < min_users_threshold:
            break
        if len(details["related_anime"]) > 0:
            media_type = anime["node"]["media_type"]
            filtered_anime = f"{media_type.upper()}: {anime['node']['title']} - {anime['node']['num_list_users']} - https://myanimelist.net/anime/{anime['node']['id']}"
            print(filtered_anime)
            prequels.append(filtered_anime)
    return prequels


def find_sequel_seasonal(year=2024, season="summer"):
    data = get_seasonal(year, season)

    filtered_data = filter_prequel(data)

    return filtered_data


def main():
    id = "55749"
    params = {"nsfw": "true", "sort": "anime_num_list_users", "fields": "related_anime", "limit": 30}
    response = requests.get(f'https://api.myanimelist.net/v2/anime/season/2024/summer', headers=auth, params=params)
    print(response.json())   


if __name__ == '__main__': 
    # main()
    find_sequel_seasonal()

