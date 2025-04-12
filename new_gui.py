import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
import tkinter as tk
import datetime

import mal_access
import util
from util import SEASONS, BACKGROUND_COLORS


save_data = {}
    

def change_anime_status(label, save_data, direction, anime_id):
    new_index = (save_data[anime_id] + direction) % len(BACKGROUND_COLORS)
    save_data[anime_id] = new_index
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
            save_data[anime_id] = 0

        label = ttk.Label(frame, text=f"{anime['node']['title']} - {anime_id} - {anime['node']['num_list_users']}", background=BACKGROUND_COLORS[save_data[anime_id]])
        
        label.bind("<Button-1>", lambda event, label=label, save_data=save_data, anime_id=anime_id: change_anime_status(label, save_data, 1, anime_id))
        label.bind("<Button-3>", lambda event, label=label, save_data=save_data, anime_id=anime_id: change_anime_status(label, save_data, -1, anime_id))
        label.pack(fill="x")


def show_initial_season(year, season, frame):
    global save_data
    save_data = util.load_save_data(year, season)

    for widget in frame.winfo_children():
        widget.destroy()
    
    for anime_id, status in save_data.items():
        label = ttk.Label(frame, text=f"Anime ID: {anime_id}", background=BACKGROUND_COLORS[status])
        label.bind("<Button-1>", lambda event, label=label, save_data=save_data, anime_id=anime_id: change_anime_status(label, save_data, 1, anime_id))
        label.bind("<Button-3>", lambda event, label=label, save_data=save_data, anime_id=anime_id: change_anime_status(label, save_data, -1, anime_id))
        label.pack(fill="x")


# TODO: Fix save format containing all necessary data (title, anime_id, num_list_users, media_type)
# TODO: Add upcoming anime
# TODO: Add current season recommendations
def gui():

    root = ttk.Window(title="Anime Recommender", themename="flatly", size=(800, 600))
    root.position_center()
    
    year_valid_function = root.register(util.validate_year)

    initial_label = ttk.Label(root, text="Anime Recommender", font=("Helvetica", 16))
    initial_label.pack(pady=10)

    year_frame = ttk.Frame(root)
    year_frame.pack(pady=5)
    year_label = ttk.Label(year_frame, text="Enter Year:")
    year_label.pack(side="left", expand=True, padx=5)
    year_entry = ttk.Spinbox(year_frame, from_=1916, to=datetime.datetime.now().year + 3, increment=1, width=5, validate="focus", validatecommand=(year_valid_function, "%P"), wrap=True, command=lambda: show_initial_season(year_entry.get(), season_var.get().lower(), sequels_frame))
    year_entry.set(datetime.datetime.now().year)
    year_entry.pack(side="left", expand=True, padx=5)

    season_frame = ttk.Frame(root)
    season_frame.pack(pady=5)
    season_label = ttk.Label(season_frame, text="Select Season:")
    season_label.pack(side="left", expand=True, padx=5)
    season_var = ttk.StringVar()
    season_menu = ttk.OptionMenu(season_frame, season_var, util.get_next_season(), *SEASONS, command=lambda val: show_initial_season(year_entry.get(), season_var.get().lower(), sequels_frame))
    season_menu.pack(side="left", expand=True, padx=5)

    search_season_button = ttk.Button(root, text="Search Selected Season", command=lambda: show_seasonal_anime(year_entry.get(), season_var.get().lower(), sequels_frame))
    search_season_button.pack(pady=5)

    sequels_border_frame = tk.Frame(root, highlightbackground="black", highlightthickness=1, width=400, height=300)
    sequels_border_frame.pack(pady=5)
    sequels_frame = ScrolledFrame(sequels_border_frame, width=400, height=300, autohide=True)
    sequels_frame.pack(pady=3, padx=3)

    save_button = ttk.Button(root, text="Save Changes", command=lambda: util.save_changes(season_var.get().lower(), year_entry.get(), save_data))
    save_button.pack(pady=5)

    show_initial_season(year_entry.get(), season_var.get().lower(), sequels_frame)

    root.mainloop()


if __name__ == "__main__":
    gui()