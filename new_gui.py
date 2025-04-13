import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
import tkinter as tk
import datetime

import mal_access
import util
from util import SEASONS, BACKGROUND_COLORS


save_data = {}
    

def change_anime_status(label, save_data, direction, anime_id):
    new_index = (save_data[anime_id]["status"] + direction) % len(BACKGROUND_COLORS)
    save_data[anime_id]["status"] = new_index
    label.config(background=BACKGROUND_COLORS[new_index])


def change_anime_status_upcoming(label, direction):
    color = str(label.cget("background"))
    index = BACKGROUND_COLORS.index(color)
    new_index = (index + direction) % len(BACKGROUND_COLORS)
    label.config(background=BACKGROUND_COLORS[new_index])


def show_seasonal_anime(year, season, frame):
    global save_data 
    save_data = util.load_save_data(year, season)
    seasonal_anime = mal_access.get_seasonal_anime(year, season)
    seasonal_anime = util.filter_sequels(seasonal_anime)
    
    for widget in frame.winfo_children():
        widget.destroy()
    
    for anime in seasonal_anime:
        anime_id = str(anime['node']['id'])
        
        if anime_id not in save_data:
            save_data[anime_id] = {"title": anime['node']['title'], "num_list_users": anime['node']['num_list_users'], "media_type": anime['node']['media_type'], "status": 0}

        label = ttk.Label(frame, text=f"{anime['node']['title']} - {anime_id} - {anime['node']['num_list_users']}", background=BACKGROUND_COLORS[save_data[anime_id]["status"]])
        
        label.bind("<Button-1>", lambda event, label=label, save_data=save_data, anime_id=anime_id: change_anime_status(label, save_data, 1, anime_id))
        label.bind("<Button-3>", lambda event, label=label, save_data=save_data, anime_id=anime_id: change_anime_status(label, save_data, -1, anime_id))
        label.pack(fill="x")


def show_initial_season(year, season, frame):
    global save_data
    save_data = util.load_save_data(year, season)

    for widget in frame.winfo_children():
        widget.destroy()
    
    for anime_id, data in save_data.items():
        label = ttk.Label(frame, text=f"{data["title"]} - {anime_id} - {data["num_list_users"]}", background=BACKGROUND_COLORS[data["status"]])
        label.bind("<Button-1>", lambda event, label=label, save_data=save_data, anime_id=anime_id: change_anime_status(label, save_data, 1, anime_id))
        label.bind("<Button-3>", lambda event, label=label, save_data=save_data, anime_id=anime_id: change_anime_status(label, save_data, -1, anime_id))
        label.pack(fill="x")


def show_upcoming_anime(frame):
    upcoming_anime = mal_access.get_upcoming_anime()
    upcoming_data = util.load_upcoming_data()

    for widget in frame.winfo_children():
        widget.destroy()

    for anime in upcoming_anime["data"]:
        anime_id = str(anime['node']['id'])

        if anime_id not in upcoming_data:
            upcoming_data[anime_id] = {"title": anime["node"]["title"], "num_list_users": anime["node"]["num_list_users"], "status": 0}

        label = ttk.Label(frame, text=f"{anime['node']['title']} - {anime['node']['id']} - {anime['node']['num_list_users']}", background=BACKGROUND_COLORS[upcoming_data[anime_id]["status"]])
        label.bind("<Button-1>", lambda event, label=label: change_anime_status_upcoming(label, 1))
        label.bind("<Button-3>", lambda event, label=label: change_anime_status_upcoming(label, -1))
        label.pack(fill="x")


def show_initial_upcoming(frame):
    upcoming_data = util.load_upcoming_data()

    for widget in frame.winfo_children():
        widget.destroy()
    
    for anime_id, data in upcoming_data.items():
        label = ttk.Label(frame, text=f"{data['title']} - {anime_id} - {data['num_list_users']}", background=BACKGROUND_COLORS[data["status"]])
        label.bind("<Button-1>", lambda event, label=label: change_anime_status_upcoming(label, 1))
        label.bind("<Button-3>", lambda event, label=label: change_anime_status_upcoming(label, -1))
        label.pack(fill="x")


# TODO: Add current season recommendations
# TODO: Don't rely on global variable
def gui():

    root = ttk.Window(title="Anime Recommender", themename="flatly", size=(1400, 600))
    root.position_center()
 
    year_valid_function = root.register(util.validate_year)

    initial_label = ttk.Label(root, text="Anime Recommender", font=("Helvetica", 16))
    initial_label.pack(pady=10)

    seasonal_root = tk.Frame(root, highlightbackground="black", highlightthickness=1)
    seasonal_root.pack(pady=5, expand=True, side="left")   

    year_frame = ttk.Frame(seasonal_root)
    year_frame.pack(pady=5)
    year_label = ttk.Label(year_frame, text="Enter Year:")
    year_label.pack(side="left", expand=True, padx=5)
    year_entry = ttk.Spinbox(year_frame, from_=1916, to=datetime.datetime.now().year + 3, increment=1, width=5, validate="focus", validatecommand=(year_valid_function, "%P"), wrap=True, command=lambda: show_initial_season(year_entry.get(), season_var.get().lower(), sequels_frame))
    year_entry.set(datetime.datetime.now().year)
    year_entry.pack(side="left", expand=True, padx=5)

    season_frame = ttk.Frame(seasonal_root)
    season_frame.pack(pady=5)
    season_label = ttk.Label(season_frame, text="Select Season:")
    season_label.pack(side="left", expand=True, padx=5)
    season_var = ttk.StringVar()
    season_menu = ttk.OptionMenu(season_frame, season_var, util.get_next_season(), *SEASONS, command=lambda val: show_initial_season(year_entry.get(), season_var.get().lower(), sequels_frame))
    season_menu.pack(side="left", expand=True, padx=5)

    search_season_button = ttk.Button(seasonal_root, text="Search Selected Season", command=lambda: show_seasonal_anime(year_entry.get(), season_var.get().lower(), sequels_frame))
    search_season_button.pack(pady=5)

    sequels_border_frame = tk.Frame(seasonal_root, highlightbackground="black", highlightthickness=1, width=400, height=300)
    sequels_border_frame.pack(pady=5, padx=5)
    sequels_frame = ScrolledFrame(sequels_border_frame, width=400, height=300, autohide=True)
    sequels_frame.pack(pady=3, padx=3)

    save_seasonal_button = ttk.Button(seasonal_root, text="Save Changes", command=lambda: util.save_changes(season_var.get().lower(), year_entry.get(), save_data))
    save_seasonal_button.pack(pady=5)

    show_initial_season(year_entry.get(), season_var.get().lower(), sequels_frame)

    upcoming_root = tk.Frame(root, highlightbackground="black", highlightthickness=1)
    upcoming_root.pack(pady=5, expand=True, side="left") 

    search_upcoming_button = ttk.Button(upcoming_root, text="Search Upcoming Anime", command=lambda: show_upcoming_anime(upcoming_frame))
    search_upcoming_button.pack(pady=5)

    upcoming_border_frame = tk.Frame(upcoming_root, highlightbackground="black", highlightthickness=1, width=400, height=300)
    upcoming_border_frame.pack(pady=5, padx=5)
    upcoming_frame = ScrolledFrame(upcoming_border_frame, width=400, height=300, autohide=True)
    upcoming_frame.pack(pady=3, padx=3)

    save_upcoming_button = ttk.Button(upcoming_root, text="Save Changes", command=lambda: util.save_upcoming_changes(upcoming_frame))
    save_upcoming_button.pack(pady=5)

    show_initial_upcoming(upcoming_frame)

    root.mainloop()


if __name__ == "__main__":
    gui()