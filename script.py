import datetime
import os
from main import find_sequel_seasonal, find_upcoming, get_details


seasons = ["winter", "spring", "summer", "fall"]
project_path = "D:/CodingAdventures/AnimeFinder/"


def run():
    while True:
        print("What would you like to do?")
        print("1: Search for new anime")
        print("2: Mark anime as caught up")
        print("3: Open catch-up list")
        print("4: Exit")
        choice = input().strip().lower()
        if choice == "1":
            search_new_anime()
            create_catch_up_list()
            print("Search complete.\n")
        elif choice == "2":
            id = input("Enter the MyAnimeList ID of the anime you have finished watching: ")
            finished_watching(id)
            print("Anime marked as caught up.\n")
        elif choice == "3":
            os.system(f"start {project_path}catch_up_list.txt")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")
    

def search_new_anime():
    now = datetime.datetime.now()
    year = now.year
    next_season = seasons[((now.month - 1) // 3 + 1) % 4]
    if next_season == "winter":
        year += 1

    complete_visited = {}
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
            complete_visited[mal_id] = "0"

        save_visited_anime(filename, visited)
        print(f"Completed search for {next_season} {year} anime.")

        next_season = seasons[(seasons.index(next_season) + 1) % 4]
        if next_season == "winter":
            year += 1

    upcoming = find_upcoming()
    filename = project_path + f"Savestates_Script/upcoming.txt"
    complete_visited.update(load_visited_anime(filename))

    for anime in upcoming:
        id = str(anime["node"]["id"])
        if id not in complete_visited:
            if prompt_user_to_add(f"{anime['node']['title']} - https://myanimelist.net/anime/{id}"):
                complete_visited[id] = "1"
            else:
                complete_visited[id] = "0"   
    
    save_visited_anime(filename, complete_visited)


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
                    lines = f.read().splitlines()
                    if file == "upcoming.txt":
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
                            catch_up_list.write(f"{details['title']} - {details['num_list_users']} - https://myanimelist.net/anime/{details['id']}\n")
                            # maybe keep sequence order in heap to avoid wrong order in catch_up_list
                    catch_up_list.write("\n\n")


def finished_watching(id):
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
    visited[id] = "0"
    save_visited_anime(filename, visited)
    create_catch_up_list()        


if __name__ == '__main__':
    run()