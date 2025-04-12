import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
import tkinter as tk
import datetime
import json

import mal_access

SEASONS = ["Winter", "Spring", "Summer", "Fall"]
BACKGROUND_COLORS = ["white", "#ccffcc", "#ffcccc"]
SAVE_PATH = "./data/"
save_data = {}

def get_current_season():
    now = datetime.datetime.now()
    return SEASONS[(now.month - 1) // 3]


def validate_year(year):
    if year.isdigit() and 1916 < int(year) < datetime.datetime.now().year + 2:
        return True
    else:
        return False
    

def change_anime_status(label, save_data, direction, anime_id):
    new_index = (save_data[anime_id] + direction) % len(BACKGROUND_COLORS)
    save_data[anime_id] = new_index
    label.config(background=BACKGROUND_COLORS[new_index])
    

def show_seasonal_anime(year, season, frame):
    global save_data 
    save_data = load_save_data(year, season)
    seasonal_anime = mal_access.get_seasonal_anime(year, season)
    
    for widget in frame.winfo_children():
        widget.destroy()
    
    for anime in seasonal_anime["data"]:
        anime_id = str(anime['node']['id'])
        
        if anime_id not in save_data:
            save_data[anime_id] = 0

        label = ttk.Label(frame, text=f"{anime['node']['title']} - {anime['node']['num_list_users']} - {anime_id}", background=BACKGROUND_COLORS[save_data[anime_id]])
        
        label.bind("<Button-1>", lambda event, label=label, save_data=save_data, anime_id=anime_id: change_anime_status(label, save_data, 1, anime_id))
        label.bind("<Button-3>", lambda event, label=label, save_data=save_data, anime_id=anime_id: change_anime_status(label, save_data, -1, anime_id))
        label.pack(fill="x")


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


def gui():

    root = ttk.Window(title="Anime Recommender", themename="flatly", size=(800, 600))
    root.position_center()
    
    year_valid_function = root.register(validate_year)

    initial_label = ttk.Label(root, text="Anime Recommender", font=("Helvetica", 16))
    initial_label.pack(pady=10)

    year_frame = ttk.Frame(root)
    year_frame.pack(pady=5)
    year_label = ttk.Label(year_frame, text="Enter Year:")
    year_label.pack(side="left", expand=True, padx=5)
    year_entry = ttk.Spinbox(year_frame, from_=1916, to=datetime.datetime.now().year + 2, increment=1, width=5, validate="focus", validatecommand=(year_valid_function, "%P"))
    year_entry.set(datetime.datetime.now().year)
    year_entry.pack(side="left", expand=True, padx=5)

    season_frame = ttk.Frame(root)
    season_frame.pack(pady=5)
    season_label = ttk.Label(season_frame, text="Select Season:")
    season_label.pack(side="left", expand=True, padx=5)
    season_var = ttk.StringVar()
    season_menu = ttk.OptionMenu(season_frame, season_var, get_current_season(), *SEASONS)
    season_menu.pack(side="left", expand=True, padx=5)

    search_season_button = ttk.Button(root, text="Search Selected Season", command=lambda: show_seasonal_anime(year_entry.get(), season_var.get().lower(), sequels_frame))
    search_season_button.pack(pady=5)

    sequels_border_frame = tk.Frame(root, highlightbackground="black", highlightthickness=1, width=400, height=300)
    sequels_border_frame.pack(pady=5)
    sequels_frame = ScrolledFrame(sequels_border_frame, width=400, height=300, autohide=True)
    sequels_frame.pack(pady=3, padx=3)

    save_button = ttk.Button(root, text="Save Changes", command=lambda: save_changes(season_var.get().lower(), year_entry.get(), save_data))
    save_button.pack(pady=5)

    root.mainloop()



if __name__ == "__main__":
    gui()