import requests
from config import MAL_KEY


auth = {"X-MAL-CLIENT-ID": MAL_KEY}
min_users_threshold = 10000


def get_seasonal(year, season):
    params = {"nsfw": "true", "sort": "anime_num_list_users", "limit": 100, "fields": "id,title,num_list_users,media_type"}
    response = requests.get(f'https://api.myanimelist.net/v2/anime/season/{year}/{season}', headers=auth, params=params)
    return response.json()


def get_details(id, params={"fields": "related_anime"}):
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
    
    if "data" not in data:
        return []
    
    filtered_data = filter_prequel(data)

    return filtered_data


def find_upcoming(params={"ranking_type": "upcoming", "limit": 10, "fields": "id,title,num_list_users,media_type,related_anime"}):
    print("Finding upcoming sequels...")
    response = requests.get(f'https://api.myanimelist.net/v2/anime/ranking', headers=auth, params=params)
    upcoming_sequels = []
    for anime in response.json()["data"]:
        if anime["node"]["num_list_users"] < min_users_threshold:
            break
        details = get_details(anime["node"]["id"])
        if len(details["related_anime"]) > 0:
            upcoming_sequels.append(anime)

    return upcoming_sequels


def main():
    id1 = "55749"
    id2 = "52807"
    params = {"ranking_type": "upcoming", "limit": 200, "fields": "id,title,num_list_users,media_type"}
    response = requests.get(f'https://api.myanimelist.net/v2/anime/ranking', headers=auth, params=params)
    for anime in response.json()["data"]:
        details = get_details(anime["node"]["id"])

        if anime["node"]["num_list_users"] < min_users_threshold:
            break
        if len(details["related_anime"]) > 0:
            media_type = anime["node"]["media_type"]
            filtered_anime = f"{media_type.upper()}: {anime['node']['title']} - {anime['node']['num_list_users']} - https://myanimelist.net/anime/{anime['node']['id']}"
            print(filtered_anime)
    # print(get_details(id2, params))   


if __name__ == '__main__': 
    find_upcoming()
    # find_sequel_seasonal(year=2025, season="spring")
    # find_sequel_seasonal(year=2025, season="summer")
    # main()
    # find_sequel_seasonal()

