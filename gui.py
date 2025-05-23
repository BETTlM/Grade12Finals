import tkinter as tk
from tkinter import font
import threading
import time

# --- Gradient background helper ---
def draw_gradient(canvas, width, height, color1, color2):
    '''Draw a vertical gradient from color1 to color2.'''
    r1, g1, b1 = canvas.winfo_rgb(color1)
    r2, g2, b2 = canvas.winfo_rgb(color2)
    r_ratio = (r2 - r1) / height
    g_ratio = (g2 - g1) / height
    b_ratio = (b2 - b1) / height
    for i in range(height):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = f'#{nr//256:02x}{ng//256:02x}{nb//256:02x}'
        canvas.create_line(0, i, width, i, fill=color)

# --- File reading and monitoring logic ---
def read_file():
    try:
        with open("guisrs.txt", "r") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "File not found"

def update_text():
    file_content = ' ' + read_file()
    seats_label.config(text=file_content)
    root.after(1000, update_text)

def file_monitor():
    previous_content = read_file()
    while True:
        time.sleep(1)
        current_content = read_file()
        if current_content != previous_content:
            previous_content = current_content
            root.event_generate("<<FileChanged>>", when="tail")

# --- Main window setup ---
root = tk.Tk()
root.title("Dynamic Ticket Expert")
root.geometry('800x600')
root.resizable(False, False)

# --- Gradient background ---
canvas = tk.Canvas(root, width=800, height=600, highlightthickness=0)
canvas.place(x=0, y=0, relwidth=1, relheight=1)
draw_gradient(canvas, 800, 600, '#232526', '#414345')

# --- Main frame with rounded border effect ---
main_frame = tk.Frame(root, bg='#222c37', bd=0, highlightthickness=0)
main_frame.place(relx=0.5, rely=0.5, anchor='center', width=700, height=500)

# --- Title section ---
title_font = font.Font(family="Helvetica", size=32, weight="bold")
subtitle_font = font.Font(family="Helvetica", size=20, weight="bold")

main_title = tk.Label(
    main_frame,
    text="DYNAMIC TICKET EXPERT",
    font=title_font,
    fg="#00c3ff",
    bg="#222c37",
    pady=10
)
main_title.pack(pady=(30, 0))

subtitle = tk.Label(
    main_frame,
    text="GRAND CINEMAS",
    font=subtitle_font,
    fg="#f7971e",
    bg="#222c37"
)
subtitle.pack(pady=(0, 20))

# --- Seats section ---
seats_label_title = tk.Label(
    main_frame,
    text="SEATS LEFT",
    font=font.Font(family="Helvetica", size=24, weight="bold"),
    fg="#ffffff",
    bg="#222c37"
)
seats_label_title.pack(pady=(10, 5))

# --- Stylish seat count display ---
seats_label = tk.Label(
    main_frame,
    text="",
    font=font.Font(family="Helvetica", size=100, weight="bold"),
    fg="#00ff99",
    bg="#181f27",
    bd=0,
    relief="flat",
    highlightthickness=0
)
seats_label.pack(pady=20, ipadx=30, ipady=10)

# --- Shadow effect for seat count (optional) ---
# You can add a shadow label behind seats_label for more depth if desired.

# --- Start the file monitoring thread ---
file_monitor_thread = threading.Thread(target=file_monitor, daemon=True)
file_monitor_thread.start()

# --- Bind the file change event ---
root.bind("<<FileChanged>>", lambda event: update_text())

# --- Start the initial text update ---
update_text()

# --- Start the GUI main loop ---
root.mainloop()
