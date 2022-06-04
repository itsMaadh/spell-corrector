from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
import tkinter
from tkinter.tix import COLUMN

# Initialize Tk and main frame
root = Tk()
root.title("Spell Checker")
frame = ttk.Frame(root, padding=20)
frame.grid()

# Multi-line input text box with label
text_input_label = ttk.Label(frame, text="Enter input here (500 words max)")
text_input_label.grid(column=0, row=0, sticky="W", padx=10)

text_input = scrolledtext.ScrolledText(frame, wrap=tkinter.WORD,
                                      width=50, height=8,
                                      font=("Times New Roman", 15))
text_input.grid(column=0, row=1, rowspan=2, pady=0, padx=10)

# Dictionary label and text box
dictionary_label = ttk.Label(frame, text="Dictionary:")
dictionary_label.grid(column=1, row=0, sticky="W", padx=40)

dictionary_listbox = Listbox(frame, width=30)
dictionary_listbox.grid(column=1, row=1, columnspan=1, padx=40, sticky="W")

# Insert sample numbers into the listbox
for values in range(100):
    dictionary_listbox.insert(END, values)

# Dictionary search label and input text box
search_label = ttk.Label(frame, text="Search:", width=10)
search_label.grid(column=1, row=2, sticky="W", padx=40)

search_input = ttk.Entry(frame, width=20)
search_input.grid(column=1, row=2, padx=110)

# Check spelling button
check_spelling_button = ttk.Button(frame, text="Check")
check_spelling_button.grid(column=0, row=3, sticky="E", padx=(0,10), pady=(10,0))

# Quit button
quit_button = ttk.Button(frame, text="Quit", command=root.destroy)
quit_button.grid(column=0, row=4, columnspan=2, pady=(30,0))

# Put everything together
root.mainloop()