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

    def find_sequel_seasonal():
        year = year_entry.get()
        season = season_var.get()
        result = main.find_sequel_seasonal(year, season)
        result.sort(key=lambda x: x.split(":")[0])  # Sort the result by mediatype
        result_text.delete(1.0, tk.END)  # Clear the text widget
        for i in result:
            media_type = i.split(":")[0]
            result_text.tag_configure(media_type, foreground=mediatype_colors[media_type])  # Create a tag for this media type
            result_text.insert(tk.END, f"{i}\n", media_type)  # Apply the tag to the inserted text
            
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
    year_entry.insert(0, "2025")  # Autofill with year 2024

    # Create a label and option menu for season name
    season_label = ttk.Label(input_frame, text="Season Name:")
    season_label.grid(row=1, column=0, padx=5, pady=5)
    season_var = tk.StringVar()
    season_option_menu = ttk.OptionMenu(input_frame, season_var, "winter", "summer", "fall", "winter", "spring")
    season_option_menu.grid(row=1, column=1, padx=5, pady=5)
    
    # Create a button    
    button = ttk.Button(window, text="Find Sequel Seasonal", command=find_sequel_seasonal)
    button.pack()
    
    # Create a text widget to display the results
    result_text = tk.Text(window, height=40, width=200)
    result_text.pack()

    # Start the main loop
    window.mainloop()

find_sequel_seasonal_gui()