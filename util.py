import mal_access
import datetime
import json

SEASONS = ["Winter", "Spring", "Summer", "Fall"]
BACKGROUND_COLORS = ["white", "#ccffcc", "#ffcccc"]
SAVE_PATH = "./data/"
MIN_USERS_THRESHOLD = 10000


def filter_sequels(anime_list):
    sequels = []
    for anime in anime_list["data"]:
        if anime["node"]["num_list_users"] < MIN_USERS_THRESHOLD:
            break

        details = mal_access.get_anime_details(anime["node"]["id"])
        if len(details["related_anime"]) > 0:
            sequels.append(anime)
    
    return sequels


def validate_year(year):
    if year.isdigit() and 1916 < int(year) < datetime.datetime.now().year + 2:
        return True
    else:
        return False
    

def get_current_season():
    now = datetime.datetime.now()
    return SEASONS[(now.month - 1) // 3]


def save_changes(season, year, save_data):
    print("Saving changes...")
    with open(f"{SAVE_PATH}{year}_{season}.json", "w") as file:
        json.dump(save_data, file, indent=4)   


def load_save_data(year, season):
    try:
        with open(f"{SAVE_PATH}{year}_{season}.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}