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
name_list = []
counter = 0

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
    global name_list, counter

    #names = name_entry.get()
    #name_list = names.split(',')
    if counter < 3 and len(name_list) > 0:
        winner = random.choice(name_list)
        name_list.remove(winner)
        winner_index = name_listbox.get(0, "end").index(winner)
        name_listbox.itemconfig(winner_index,{'bg':'yellow'})
        counter += 1
        winner_label.config(text=f"Winner {counter}: {winner}")
        
    elif counter >= 3:
        winner_label.config(text=f"No more than 3 draws are allowed")
    else:
        winner_label.config(text=f"No names left to draw")

def record_button_click():
    global recording, click_to_start, name_list

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Get the directory of the executable
    if getattr(sys, 'frozen', False):
        executable_dir = os.path.dirname(sys.executable)
    else:
        executable_dir = os.path.dirname(os.path.abspath(__file__))
    # Set the output directory to the same directory as the executable
    output_directory = executable_dir
    filename = os.path.join(output_directory, f"quality_week_2023_final_{timestamp}.mp4")
    if click_to_start:
        names = name_entry.get()
        name_list = names.split(',')
        for name in name_list:
            name_listbox.insert ("end", name)
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
root.title("Quality Week 2023 Final Winners")
# Create and set widgets
# Create a font object with the desired family, size, and style
bold_font = tkFont.Font(family="Helvetica", size=14, weight="bold")


# Create the frames
frame1 = tk.Frame(root)
frame2 = tk.Frame(root)
# Create widgets in the first frame
title_label = tk.Label(frame1, text="Quality Week 2023 Final Winners")
title_label.config(font=bold_font)
name_label = tk.Label(frame1, text="Enter names separated by commas:")
name_entry = tk.Entry(frame1, width=50)
pick_button = tk.Button(frame1, text="Pick a Winner!", command=pick_winner)
winner_label = tk.Label(frame1, text="Winner: ")
record_button = tk.Button(frame1, text="Click to Start Recording", command=record_button_click)
# Create widgets in the second frame
name_listbox_label = tk.Label(frame2, text="Top Contributors of the Week")
name_listbox = tk.Listbox(frame2, height=15)
name_listbox_scrollbar = tk.Scrollbar(frame2, orient="vertical", command=name_listbox.yview)
name_listbox.configure(yscrollcommand=name_listbox_scrollbar.set)
# Position widgets on the frames
title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
name_label.grid(row=1, column=0, padx=10, pady=10)
name_entry.grid(row=1, column=1, padx=10, pady=10)
pick_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
winner_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
record_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
name_listbox_label.grid(row=0, column=0, padx=10, pady=10)
name_listbox.grid(row=1, column=0, padx=10, pady=10, sticky='ns')
name_listbox_scrollbar.grid(row=1, column=1, padx=10, pady=10, sticky='ns')
# Position frames on the root window
frame1.grid(row=0, column=0)
frame2.grid(row=0, column=1)



# Run the main loop
root.mainloop()
