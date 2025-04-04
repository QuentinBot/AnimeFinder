import ttkbootstrap as ttk
import datetime

SEASONS = ["Winter", "Spring", "Summer", "Fall"]


def get_current_season():
    now = datetime.datetime.now()
    return SEASONS[(now.month - 1) // 3]


def validate_year(year):
    if year.isdigit() and 1916 < int(year) < datetime.datetime.now().year + 2:
        return True
    else:
        return False
    

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

    search_season_button = ttk.Button(root, text="Search Selected Season", command=lambda: print(f"Searching {season_var.get()} {year_entry.get()}..."))
    search_season_button.pack(pady=5)


    root.mainloop()



if __name__ == "__main__":
    gui()