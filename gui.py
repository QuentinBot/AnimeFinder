import main
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def find_sequel_seasonal_gui():
    mediatype_colors = {
        "MOVIE": "purple",
        "TV": "blue",
        "OVA": "yellow",
        "ONA": "green",
        "SPECIAL": "brown",
        "MUSIC": "gray",
        "UNKNOWN": "black",
        "TV_SPECIAL": "red"
    }
    background_colors = ["white", "#ccffcc", "#ffcccc"] # "#ccffcc" = green, "#ffcccc" = red

    def find_sequel_seasonal():
        year = year_entry.get()
        season = season_var.get()
        result = main.find_sequel_seasonal(year, season)
        result.sort(key=lambda x: x.split(":")[0])  # Sort the result by mediatype
        result_text.delete(1.0, tk.END)  # Clear the text widget

        filename = f"./Savestates/sequel_seasonal_{year}_{season}.txt"
        background_dictionary = {}
        try:
            with open(filename, "r") as file:
                saved_lines = file.readlines()
                for line in saved_lines:
                    color, tag = line.split()
                    background_dictionary[tag] = color
        except FileNotFoundError:
            pass

        for i in result:
            media_type = i.split(":")[0]
            mal_id = i.split(" - ")[-1].split("/")[-1]
            if mal_id not in background_dictionary:
                background_dictionary[mal_id] = "white"

            result_text.tag_configure(mal_id, background=background_dictionary[mal_id], foreground=mediatype_colors[media_type])  # Create a tag for this media type
            result_text.insert(tk.END, f"{i}\n", mal_id)  # Apply the tag to the inserted text
            result_text.tag_bind(mal_id, "<Button-1>", lambda e, tag=mal_id: change_color(tag, 1))  # Bind left click event to change color
            result_text.tag_bind(mal_id, "<Button-3>", lambda e, tag=mal_id: change_color(tag, -1))  # Bind right click event to change color

    def change_color(tag, direction):
        # Change the color of the line when clicked
        current_color = result_text.tag_cget(tag, "background")
        new_color = background_colors[(background_colors.index(current_color) + direction) % len(background_colors)]
        result_text.tag_configure(tag, background=new_color)
        
    def save_state():
        year = year_entry.get()
        season = season_var.get()
        filename = f"sequel_seasonal_{year}_{season}.txt"
        with open("./Savestates/" + filename, "w") as file:
            for line in result_text.get(1.0, tk.END).splitlines():
                tag = line.split("/")[-1]
                if tag:
                    current_color = result_text.tag_cget(tag, "background")      
                    file.write(f"{current_color} {tag}\n")
        messagebox.showinfo("Save State", f"Results saved to {filename}")

    # Create the main window
    window = tk.Tk()
    window.title("Find Sequel Seasonal")
    
    # Create a label
    label = ttk.Label(window, text="Find Sequel Seasonal")
    label.pack()

    # Create a frame for input fields
    input_frame = ttk.Frame(window)
    input_frame.pack()

    # Create a label and entry for year
    year_label = ttk.Label(input_frame, text="Year:")
    year_label.grid(row=0, column=0, padx=5, pady=5)
    year_entry = ttk.Entry(input_frame)
    year_entry.grid(row=0, column=1, padx=5, pady=5)
    year_entry.insert(0, "2025")  # Autofill with year 2025

    # Create a label and option menu for season name
    season_label = ttk.Label(input_frame, text="Season Name:")
    season_label.grid(row=1, column=0, padx=5, pady=5)
    season_var = tk.StringVar()
    season_option_menu = ttk.OptionMenu(input_frame, season_var, "winter", "summer", "fall", "winter", "spring")
    season_option_menu.grid(row=1, column=1, padx=5, pady=5)
    
    # Create a button    
    button = ttk.Button(window, text="Find Sequel Seasonal", command=find_sequel_seasonal)
    button.pack()

    # Create a save button
    save_button = ttk.Button(window, text="Save", command=save_state)
    save_button.pack(side=tk.BOTTOM)

    # Create a text widget to display the results
    result_text = tk.Text(window, height=40, width=200)
    result_text.pack()

    # Start the main loop
    window.mainloop()

find_sequel_seasonal_gui()