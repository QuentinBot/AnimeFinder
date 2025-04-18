import mal_access
import datetime
import json

SEASONS = ["Winter", "Spring", "Summer", "Fall"]
BACKGROUND_COLORS = ["white", "#ccffcc", "#ffcccc"]
SAVE_PATH = "./data/"
MIN_USERS_THRESHOLD = 10000
CURRENT_SEASON_THRESHOLD = 100000


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


def get_next_season():
    now = datetime.datetime.now()
    current_season_index = (now.month - 1) // 3
    next_season_index = (current_season_index + 1) % len(SEASONS)
    return SEASONS[next_season_index]


def save_changes(path, frame):
    print("Saving changes...")
    save_data = {}
    for widget in frame.winfo_children():
        num_list_users = widget.cget("text").split(" - ")[-1]
        anime_id = widget.cget("text").split(" - ")[-2]
        title = " - ".join(widget.cget("text").split(" - ")[:-2])
        save_data[anime_id] = {"title": title, "num_list_users": num_list_users, "status": BACKGROUND_COLORS.index(str(widget.cget("background")))}
    
    with open(f"{SAVE_PATH}{path}.json", "w") as file:
        json.dump(save_data, file, indent=4)


def load_save_data(path):
    try:
        with open(f"{SAVE_PATH}{path}.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}