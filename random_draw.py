import tkinter as tk
import random
import cv2
import numpy as np
import os
import sys
from PIL import ImageGrab
import threading
import time
from datetime import datetime
import tkinter.font as tkFont

recording = False
click_to_start = True

def record_screen(filename):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, 5.0, (root.winfo_width(), root.winfo_height()))
    while recording:
        img = ImageGrab.grab(bbox=(root.winfo_rootx(), root.winfo_rooty(), root.winfo_rootx() + root.winfo_width(), root.winfo_rooty() + root.winfo_height()))
        img_np = np.array(img)
        frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        out.write(frame)
    out.release()

def pick_winner():
    names = name_entry.get()
    name_list = names.split(',')
    winner = random.choice(name_list)
    winner_label.config(text=f"Winner: {winner}")

def record_button_click():
    global recording, click_to_start
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Get the directory of the executable
    if getattr(sys, 'frozen', False):
        executable_dir = os.path.dirname(sys.executable)
    else:
        executable_dir = os.path.dirname(os.path.abspath(__file__))
    # Set the output directory to the same directory as the executable
    output_directory = executable_dir
    filename = os.path.join(output_directory, f"quality_week_2023_{timestamp}.mp4")
    if click_to_start:
        recording = True
        click_to_start = False
        threading.Thread(target=record_screen, args=(filename,)).start()
        record_button.config(text="Click to Stop Recording")
    else:
        recording = False
        click_to_start = True
        record_button.config(text="Click to Start Recording")
    

# Create the main window
root = tk.Tk()
root.title("Quality Week 2023 Daily Winner")
# Create and set widgets
# Create a font object with the desired family, size, and style
bold_font = tkFont.Font(family="Helvetica", size=14, weight="bold")


title_label = tk.Label(root, text = "Quality Week 2023 Daily Winner")
title_label.config(font=bold_font)
name_label = tk.Label(root, text="Enter names separated by commas:")
name_entry = tk.Entry(root, width=50)
pick_button = tk.Button(root, text="Pick a Winner!", command=pick_winner)
winner_label = tk.Label(root, text="Winner: ")
record_button = tk.Button(root, text="Click to Start Recording", command=record_button_click)

# Position widgets on the main window
title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
name_label.grid(row=1, column=0, padx=10, pady=10)
name_entry.grid(row=1, column=1, padx=10, pady=10)
pick_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
winner_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
record_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Run the main loop
root.mainloop()










