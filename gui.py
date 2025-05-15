import customtkinter as ctk
import threading
import time
from tkinter import font

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def read_file():
    try:
        with open("guisrs.txt", "r") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "File not found"

def update_text():
    file_content = ' ' + read_file()
    seats_label.configure(text=file_content)
    root.after(1000, update_text)

def file_monitor():
    previous_content = read_file()
    while True:
        time.sleep(1)
        current_content = read_file()
        if current_content != previous_content:
            previous_content = current_content
            root.event_generate("<<FileChanged>>", when="tail")

# Create the main window
root = ctk.CTk()
root.title("Dynamic Ticket Expert")
root.geometry('800x600')

# Create main frame
main_frame = ctk.CTkFrame(root)
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Title section
title_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
title_frame.pack(fill="x", pady=(0, 20))

main_title = ctk.CTkLabel(
    title_frame,
    text="DYNAMIC TICKET EXPERT",
    font=ctk.CTkFont(family="Helvetica", size=32, weight="bold")
)
main_title.pack(pady=(0, 10))

subtitle = ctk.CTkLabel(
    title_frame,
    text="GRAND CINEMAS",
    font=ctk.CTkFont(family="Helvetica", size=24, weight="bold")
)
subtitle.pack()

# Seats section
seats_frame = ctk.CTkFrame(main_frame)
seats_frame.pack(fill="both", expand=True, padx=20, pady=20)

seats_label_title = ctk.CTkLabel(
    seats_frame,
    text="SEATS LEFT",
    font=ctk.CTkFont(family="Helvetica", size=28, weight="bold")
)
seats_label_title.pack(pady=(20, 10))

seats_label = ctk.CTkLabel(
    seats_frame,
    text="",
    font=ctk.CTkFont(family="Helvetica", size=120, weight="bold")
)
seats_label.pack(pady=20)

# Start the file monitoring thread
file_monitor_thread = threading.Thread(target=file_monitor, daemon=True)
file_monitor_thread.start()

# Bind the file change event
root.bind("<<FileChanged>>", lambda event: update_text())

# Start the initial text update
update_text()

# Start the GUI main loop
root.mainloop()
