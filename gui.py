import tkinter as tk
import threading
import time
from tkinter import font
from tkinter import *


time.sleep(3)


# Function to read the file content


def read_file():
    try:
        with open("guisrs.txt", "r") as file:
            content = file.read()

        return content


    except FileNotFoundError:
        return "File not found"



# Function to update the text in the GUI

def update_text():
    file_content = ' '+read_file()


    text_widget.config(state=tk.NORMAL)  # Enable text widget for editing

    text_widget.delete(1.0, tk.END)  # Clear the existing text

    text_widget.insert(tk.END, file_content)  # Insert the new content

    text_widget.config(state=tk.DISABLED)  # Disable text widget for editing

    root.after(1000, update_text)  # Schedule the update every 1 second



# Function to monitor the file for changes in a separate thread
def file_monitor():

    previous_content = read_file()

    while True:

        time.sleep(1)  # Check for changes every 1 second

        current_content = read_file()

        if current_content != previous_content:

            previous_content = current_content

            root.event_generate("<<FileChanged>>", when="tail")


# Create the main GUI window

root = tk.Tk()

root.title("DYNAMIC TICKET EXPERT")

root.geometry('550x550')

root.configure(bg= "cyan")



# Create a text widget to display the file content


# Create a custom font for the main title

main_title_font = font.Font(family="Cascadia Code", size=24, weight="bold")

# Create a Label for the main title
main_title_label = tk.Label(root, text="DYNAMIC TICKET EXPERT", font=main_title_font, bg="cyan")
main_title_label.pack(pady=30)



# Create a custom font for the secondary title
secondary_title_font = font.Font(family="Arial", size=20, slant="italic",weight="bold")


# Create a Label for the secondary title
secondary_title_label = tk.Label(root, text="GRAND CINEMAS", font=secondary_title_font, bg="cyan")
secondary_title_label.pack(pady=20)


# Create a custom font for the normal text
normal_text_font = font.Font(family="Helvetica", size=32)

# Create a Label for the normal text
normal_text_label = tk.Label(root, text="SEATS LEFT", font=normal_text_font, bg="cyan")
normal_text_label.pack(pady=20  )




temp = font.Font(family="Consolas", size= 150)


text_widget = tk.Text(root, wrap=tk.WORD,font=temp, bg="cyan")
text_widget.tag_configure("center", justify='center')
text_widget.tag_add("tag_name", "1.0", "end")
text_widget.pack()


text_widget.config(state=tk.DISABLED)  # Disable text widget for editing




# Create a thread to monitor the file


file_monitor_thread = threading.Thread(target=file_monitor, daemon=True)    
file_monitor_thread.start()


# Bind an event to update the text widget when the file changes

root.bind("<<FileChanged>>", lambda event: update_text())



# Start the initial text update

update_text()


# Start the GUI main loop

root.mainloop()
