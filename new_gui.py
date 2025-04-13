import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
import tkinter as tk
import datetime

import mal_access
import util
from util import SEASONS, BACKGROUND_COLORS, CURRENT_SEASON_THRESHOLD


def change_anime_status(label, direction):
    color = str(label.cget("background"))
    index = BACKGROUND_COLORS.index(color)
    new_index = (index + direction) % len(BACKGROUND_COLORS)
    label.config(background=BACKGROUND_COLORS[new_index])


def show_seasonal_anime(year, season, frame):
    seasonal_data = util.load_save_data(year, season)
    seasonal_anime = mal_access.get_seasonal_anime(year, season)
    seasonal_anime = util.filter_sequels(seasonal_anime)
    
    for widget in frame.winfo_children():
        widget.destroy()
    
    for anime in seasonal_anime:
        anime_id = str(anime['node']['id'])
        
        if anime_id not in seasonal_data:
            seasonal_data[anime_id] = {"title": anime['node']['title'], "num_list_users": anime['node']['num_list_users'], "media_type": anime['node']['media_type'], "status": 0}

        label = ttk.Label(frame, text=f"{anime['node']['title']} - {anime_id} - {anime['node']['num_list_users']}", background=BACKGROUND_COLORS[seasonal_data[anime_id]["status"]])
        
        label.bind("<Button-1>", lambda event, label=label: change_anime_status(label, 1))
        label.bind("<Button-3>", lambda event, label=label: change_anime_status(label, -1))
        label.pack(fill="x")


def show_initial_season(year, season, frame):
    seasonal_data = util.load_save_data(year, season)

    for widget in frame.winfo_children():
        widget.destroy()
    
    for anime_id, data in seasonal_data.items():
        label = ttk.Label(frame, text=f"{data["title"]} - {anime_id} - {data["num_list_users"]}", background=BACKGROUND_COLORS[data["status"]])
        label.bind("<Button-1>", lambda event, label=label: change_anime_status(label, 1))
        label.bind("<Button-3>", lambda event, label=label: change_anime_status(label, -1))
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
        label.bind("<Button-1>", lambda event, label=label: change_anime_status(label, 1))
        label.bind("<Button-3>", lambda event, label=label: change_anime_status(label, -1))
        label.pack(fill="x")


def show_initial_upcoming(frame):
    upcoming_data = util.load_upcoming_data()

    for widget in frame.winfo_children():
        widget.destroy()
    
    for anime_id, data in upcoming_data.items():
        label = ttk.Label(frame, text=f"{data['title']} - {anime_id} - {data['num_list_users']}", background=BACKGROUND_COLORS[data["status"]])
        label.bind("<Button-1>", lambda event, label=label: change_anime_status(label, 1))
        label.bind("<Button-3>", lambda event, label=label: change_anime_status(label, -1))
        label.pack(fill="x")


def show_current_season_anime(frame):
    current_season_anime = mal_access.get_seasonal_anime(datetime.datetime.now().year, util.get_current_season().lower())
    current_season_data = util.load_current_season_data()

    for widget in frame.winfo_children():
        widget.destroy()
    
    for anime in current_season_anime["data"]:
        anime_id = str(anime['node']['id'])

        if anime["node"]["num_list_users"] < CURRENT_SEASON_THRESHOLD:
            break

        if anime_id not in current_season_data:
            current_season_data[anime_id] = {"title": anime["node"]["title"], "num_list_users": anime["node"]["num_list_users"], "status": 0}

        label = ttk.Label(frame, text=f"{anime['node']['title']} - {anime['node']['id']} - {anime['node']['num_list_users']}", background=BACKGROUND_COLORS[current_season_data[anime_id]["status"]])
        label.bind("<Button-1>", lambda event, label=label: change_anime_status(label, 1))
        label.bind("<Button-3>", lambda event, label=label: change_anime_status(label, -1))
        label.pack(fill="x")


def show_initial_current_season(frame):
    current_season_data = util.load_current_season_data()

    for widget in frame.winfo_children():
        widget.destroy()
    
    for anime_id, data in current_season_data.items():
        label = ttk.Label(frame, text=f"{data['title']} - {anime_id} - {data['num_list_users']}", background=BACKGROUND_COLORS[data["status"]])
        label.bind("<Button-1>", lambda event, label=label: change_anime_status(label, 1))
        label.bind("<Button-3>", lambda event, label=label: change_anime_status(label, -1))
        label.pack(fill="x")


# TODO: Reduce redundancy
# TODO: Change logic to use three labels per anime instead of one label with multiple lines
# TODO: Make prettier
def gui():

    root = ttk.Window(title="Anime Recommender", themename="flatly", size=(1400, 600))
    root.position_center()
 
    year_valid_function = root.register(util.validate_year)

    initial_label = ttk.Label(root, text="Anime Recommender", font=("Helvetica", 16))
    initial_label.pack(pady=10)

    # Seasonal Anime
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

    save_seasonal_button = ttk.Button(seasonal_root, text="Save Changes", command=lambda: util.save_changes(season_var.get().lower(), year_entry.get(), sequels_frame))
    save_seasonal_button.pack(pady=5)

    show_initial_season(year_entry.get(), season_var.get().lower(), sequels_frame)


    # Current Season Anime
    current_season_root = tk.Frame(root, highlightbackground="black", highlightthickness=1)
    current_season_root.pack(pady=5, expand=True, side="left")

    current_season_button = ttk.Button(current_season_root, text="Search Current Season", command=lambda: show_current_season_anime(current_season_frame))
    current_season_button.pack(pady=5)

    current_season_border_frame = tk.Frame(current_season_root, highlightbackground="black", highlightthickness=1, width=400, height=300)
    current_season_border_frame.pack(pady=5, padx=5)
    current_season_frame = ScrolledFrame(current_season_border_frame, width=400, height=300, autohide=True)
    current_season_frame.pack(pady=3, padx=3)

    save_current_season_button = ttk.Button(current_season_root, text="Save Changes", command=lambda: util.save_current_season_changes(current_season_frame))
    save_current_season_button.pack(pady=5)

    show_initial_current_season(current_season_frame)


    # Upcoming Anime
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