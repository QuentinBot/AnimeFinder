import datetime
import os
from main import find_sequel_seasonal, find_upcoming, get_details, get_seasonal
import heapq


seasons = ["winter", "spring", "summer", "fall"]
project_path = "D:/CodingAdventures/AnimeFinder/"
CURRENT_VIEWER_THRESHOLD = 100000


def run():
    while True:
        print("What would you like to do?")
        print("1: Search for new anime")
        print("2: Mark anime as caught up")
        print("3: Add anime to catch-up list")
        print("4: Open catch-up list")
        print("5: Remove old seasons")
        print("6: Exit")
        choice = input().strip().lower()
        if choice == "1":
            search_new_anime()
            create_catch_up_list()
            print("Search complete.\n")
        elif choice == "2":
            id = input("Enter the MyAnimeList ID of the anime you have finished watching: ")
            update_catch_up_list(id, "0")
        elif choice == "3":
            id = input("Enter the MyAnimeList ID of the anime you want to add to the catch-up list: ")
            update_catch_up_list(id, "1")
        elif choice == "4":
            os.system(f"start {project_path}catch_up_list.txt")
        elif choice == "5":
            remove_old_seasons()
            create_catch_up_list()
            print("Old seasons removed.\n")
        elif choice == "6" or choice == "exit":
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
    

def search_new_anime():
    now = datetime.datetime.now()
    year = now.year
    cur_season = seasons[(now.month - 1) // 3]
    print("Checking for new anime in the current season...")
    result = get_seasonal(year, cur_season)
    
    filename = project_path + f"Savestates_Script/current_season.txt"
    visited = load_visited_anime(filename)

    for anime in result["data"]:
        if anime["node"]["num_list_users"] < CURRENT_VIEWER_THRESHOLD:
            break

        id = str(anime["node"]["id"])
        if id not in visited:
            input(f"{anime['node']['title']} - https://myanimelist.net/anime/{id} has reached the viewer threshold. Press any key to continue...")
            visited[id] = "1"

    save_visited_anime(filename, visited)

    next_season = seasons[(seasons.index(cur_season) + 1) % 4]
    if next_season == "winter":
        year += 1

    already_processed = {} # keep track of already processed to avoid duplicates in upcoming
    while True:
        print(f"Searching for {next_season} {year} anime...")
        result = find_sequel_seasonal(year, next_season)
        if not result:
            print("No results found.")
            break

        filename = project_path + f"Savestates_Script/{year}_{seasons.index(next_season)}_{next_season}.txt"
        visited = load_visited_anime(filename)

        for line in result:
            mal_id = line.split("/")[-1]
            if mal_id not in visited:
                if prompt_user_to_add(line):
                    visited[mal_id] = "1"
                else:
                    visited[mal_id] = "0"
            already_processed[mal_id] = "0"

        save_visited_anime(filename, visited)
        print(f"Completed search for {next_season} {year} anime.")

        next_season = seasons[(seasons.index(next_season) + 1) % 4]
        if next_season == "winter":
            year += 1

    upcoming = find_upcoming()
    filename = project_path + f"Savestates_Script/upcoming.txt"
    upcoming_visited = load_visited_anime(filename)
    upcoming_visited.update(already_processed)

    for anime in upcoming:
        id = str(anime["node"]["id"])
        if id not in upcoming_visited:
            if prompt_user_to_add(f"{anime['node']['title']} - https://myanimelist.net/anime/{id}"):
                upcoming_visited[id] = "1"
            else:
                upcoming_visited[id] = "0"   
    
    save_visited_anime(filename, upcoming_visited)


def load_visited_anime(filename):
    visited = {}
    try:
        with open(filename, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                id, status = line.split()
                visited[id] = status
    except FileNotFoundError:
        pass
    return visited


def save_visited_anime(filename, visited):
    with open(filename, "w") as file:
        for id, value in visited.items():
            file.write(f"{id} {value}\n")


def prompt_user_to_add(anime_info):
    while True:
        choice = input(f"Add to catch-up list: {anime_info}").strip().lower()
        if choice == "y":
            print("Added to catch-up list.")
            return True
        elif choice == "n":
            return False
        else:
            print("Invalid choice. Please enter 'y' or 'n'.")


def create_catch_up_list():
    path = project_path + "Savestates_Script/"
    catch_up_file = project_path + "catch_up_list.txt"
    
    with open(catch_up_file, "w", encoding="utf-8") as catch_up_list:
        for file in os.listdir(path):
            if file.endswith(".txt"):
                with open(os.path.join(path, file), "r") as f:
                    heap = []
                    lines = f.read().splitlines()
                    if file == "current_season.txt":
                        continue
                    elif file == "upcoming.txt":
                        name = "Upcoming"
                    else:
                        year, _, season = file.split('_')
                        name = f"Season: {season.split('.')[0].capitalize()} - {year}"
                    
                    catch_up_list.write("############################################################\n")
                    catch_up_list.write(f"{name}\n")
                    catch_up_list.write("############################################################\n")
                    for line in lines:
                        if line.split()[-1] == "1":
                            details = get_details(id=line.split()[0], params={"fields": "id,title,num_list_users"})
                            heapq.heappush(heap, (-details["num_list_users"], details["id"], details)) # max heap to keep most popular at the top
                    
                    while heap:
                        _, _, details = heapq.heappop(heap)
                        catch_up_list.write(f"{details['title']} - {details['num_list_users']} - https://myanimelist.net/anime/{details['id']}\n")

                    catch_up_list.write("\n\n")


def update_catch_up_list(id, val):
    details = get_details(id, params={"fields": "start_season"})
    if "error" in details:
        print(f"Anime with ID {id} not found.\n")
        return
    
    if "start_season" in details:
        filename = project_path + f"Savestates_Script/{details['start_season']['year']}_{seasons.index(details['start_season']['season'])}_{details['start_season']['season']}.txt"
    else:
        filename = project_path + "Savestates_Script/upcoming.txt"

    print("Updating catch-up list...")
    visited = load_visited_anime(filename)
    visited[id] = val
    save_visited_anime(filename, visited)
    create_catch_up_list()   
    print(f"{details["title"]} was updated.\n")


def remove_old_seasons():
    now = datetime.datetime.now()
    year = now.year
    cur_season_i = (now.month - 1) // 3

    for file in os.listdir(project_path + "Savestates_Script/"):
        if file.startswith("20"):
            split = file.split("_")
            if int(split[0]) < year or (int(split[0]) == year and int(split[1]) < cur_season_i + 1):
                os.remove(project_path + "Savestates_Script/" + file)


def test():
    create_catch_up_list()


if __name__ == '__main__':
    run()
    
    # test()