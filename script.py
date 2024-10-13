import datetime
import os
from main import find_sequel_seasonal, find_upcoming


def run():
    while True:
        choice = input("Search for new anime? (y/n): ").strip().lower()
        if choice == "y":
            search_new_anime()
            break
        elif choice == "n":
            return
        else:
            print("Invalid choice. Please enter 'y' or 'n'.")
    
    create_catch_up_list()


def search_new_anime():
    now = datetime.datetime.now()
    year = now.year
    seasons = ["winter", "spring", "summer", "fall"]
    next_season = seasons[((now.month - 1) // 3 + 1) % 4]
    if next_season == "winter":
        year += 1

    complete_visited = set()
    while True:
        print(f"Searching for {next_season} {year} anime...")
        result = find_sequel_seasonal(year, next_season)
        if not result:
            print("No results found.")
            break

        filename = f"./Savestates_Script/{year}_{next_season}.txt"
        visited = load_visited_anime(filename)

        for line in result:
            mal_id = line.split("/")[-1]
            if mal_id not in visited:
                if prompt_user_to_add(line):
                    # need to add to catch-up list (maybe dictionary, maybe save to file with 1 and 0 marking watched and unwatched)
                    pass
                visited.add(mal_id)

        save_visited_anime(filename, visited)
        complete_visited.update(visited)

        next_season = seasons[(seasons.index(next_season) + 1) % 4]
        if next_season == "winter":
            year += 1

    upcoming = find_upcoming()
    filename = f"./Savestates_Script/upcoming.txt"
    complete_visited.update(load_visited_anime(filename))

    for anime in upcoming:
        if str(anime["node"]["id"]) not in complete_visited:
            if prompt_user_to_add(f"{anime['node']['title']} - https://myanimelist.net/anime/{anime['node']['id']}"):
                # need to add to catch-up list
                pass
            complete_visited.add(anime["node"]["id"])          

    save_visited_anime(filename, complete_visited)


def load_visited_anime(filename):
    visited = set()
    try:
        with open(filename, "r") as file:
            visited.update(file.read().splitlines())
    except FileNotFoundError:
        pass
    return visited


def save_visited_anime(filename, visited):
    with open(filename, "w") as file:
        for line in visited:
            file.write(f"{line}\n")


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
    path = "./Savestates_Script/"
    catch_up_file = "./catch_up_list.txt"
    
    with open(catch_up_file, "w") as catch_up_list:
        for file in os.listdir(path):
            if file.endswith(".txt"):
                with open(os.path.join(path, file), "r") as f:
                    lines = f.read().splitlines()
                    if file == "upcoming.txt":
                        name = "Upcoming"
                    else:
                        season, year = file.split('_')
                        name = f"Season: {season.capitalize()} - {year.split('.')[0]}"
                    
                    catch_up_list.write("############################################################\n")
                    catch_up_list.write(f"{name}\n")
                    catch_up_list.write("############################################################\n")
                    catch_up_list.write("\n".join(lines))
                    catch_up_list.write("\n\n\n")


if __name__ == '__main__':
    run()