print("Status: System starting now...")

import io
import re
import math
import string
from collections import Counter
import nltk
from nltk.util import ngrams
from nltk.tokenize import regexp_tokenize

import tkinter as tkr
from tkinter import ttk
import tkinter.scrolledtext as scrolled_text


class SpellingCheckerGUI(tkr.Tk):

    def __init__(self):
        """
        Initializing the GUI components and reading in,
        (cleaning?), and creation of unigrams and dictionary.
        """
        super(SpellingCheckerGUI, self).__init__()
        self.title("Spelling Checker")
        self.minsize(800, 600)

        # reading the dict.txt
        with io.open("dict.txt", "r", encoding="utf-16") as f:
            dict_contents = f.read()

        # create dict list
        self.dictList= sorted(set(dict_contents.split('\n')))
        self.non_words = []  # empty list of non-words

        self.create_layout()
        print("\nStatus: System started\n")

    def create_layout(self):

        #This is where the layout of the GUI is created.

        # Set the canvas and the frame
        canvas = tkr.Canvas(height=800, width=600)
        canvas.pack()
        frame = tkr.Frame(bg='#F0F0F0', bd=1)  # this is the light gray background
        frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.8, anchor='n')

        title = tkr.Label(frame, text="Spelling Checker", anchor='n',
                         fg="black", font="none 23 bold")
        title.place(relx=0.20, rely=0.01, relwidth=0.60)
        
        # Provide instructions to the user
        insTitle = tkr.Label(frame, text="Instructions for user(s):", anchor='w', fg="black", font="none 10 bold")
        insTitle.place(relx=0.1, rely=0.07, relwidth=0.60)
        ins1 = tkr.Label(frame, text="1. Enter text in the given area.", anchor='w')
        ins1.place(relx=0.1, rely=0.10, relwidth=0.60)
        ins2 = tkr.Label(frame, text="2. Press the SUBMIT button.", anchor='w')
        ins2.place(relx=0.1, rely=0.13, relwidth=0.60)
        ins3 = tkr.Label(frame, text="3. Double-click a highlighted word to select it.", anchor='w')
        ins3.place(relx=0.1, rely=0.16, relwidth=0.60)
        ins4 = tkr.Label(frame, text="4. Right-click the selected error word.", anchor='w')
        ins4.place(relx=0.1, rely=0.19, relwidth=0.60)
        ins5 = tkr.Label(frame, text="5. Choose one candidate correction word, or add the selected word to dictionary.", anchor='w')
        ins5.place(relx=0.1, rely=0.22, relwidth=0.60)

        # Text Label
        textlabel = tkr.Label(frame, text="Enter input here (500 words max)", font="none 10 normal")
        textlabel.place(relx=0.1, rely=0.26)
        
        # This is the big text box where user puts in their input
        self.text = scrolled_text.ScrolledText(frame, bg="white", width=50, font="Arial 10")
        self.text.pack(expand=True, fill='both')
        self.text.place(relx=0.1, rely=0.30, relwidth=0.35, relheight=0.4)

        # Add popup menu code, binding the right-click to selected text only
        self.popup_menu = tkr.Menu(self, tearoff=0, background='#E0EEEE',
                                  fg='black', activebackground='#C1CDCD',
                                  activeforeground='#00008B')
        self.text.tag_bind("sel", '<Button-3>', self.pop_up)

        # This is the clear button
        ResetButton = tkr.Button(frame, text="CLEAR", width=7, command=self.Reset)
        ResetButton.place(relx=0.1, rely=0.71)

        # This is the submit button
        SubmitButton = tkr.Button(frame, text="SUBMIT", width=7, command=self.Submit)
        SubmitButton.place(relx=0.20, rely=0.71)

        # Original Text Label
        originalTextLabel = tkr.Label(frame, text="Original Text:", font="none 10 normal")
        originalTextLabel.place(relx=0.1, rely=0.77)

        # This text area below is user inputted box. It stores original text
        self.originalText = scrolled_text.ScrolledText(frame, bg="white", width=50, font="Arial 10")
        self.originalText.pack(expand=True, fill='both')
        self.originalText.place(relx=0.1, rely=0.80, relwidth=0.80, relheight=0.4)

        # Dictionary Text Label
        VwDict = tkr.Label(frame, text="Dictionary:", font="none 10 normal")
        VwDict.place(relx=0.55, rely=0.26)

        # This is the search box below the dictionary
        self.userSearch = tkr.StringVar()
        searchBox = tkr.Entry(frame, textvariable=self.userSearch)
        searchBox.place(relx=0.55, rely=0.71, relwidth=0.23)

        SearchButton = tkr.Button(frame, text="SEARCH", width=9, command=self.Search)
        SearchButton.place(relx=0.80, rely=0.71)

        # This is the box containing all the Valid Words in the Dictionary (VwDict)
        self.VwDictList = tkr.Listbox(frame, bg='#FFFFFF', fg="black", font="none 10 normal")

        for word in self.dictList:
            self.VwDictList.insert(tkr.END, word)

        # Scrollbar should be attached to `VwDictList`
        VwScrollBar = tkr.Scrollbar(self.VwDictList, orient=tkr.VERTICAL)
        VwScrollBar.config(command=self.VwDictList.yview)
        VwScrollBar.pack(side=tkr.RIGHT, fill=tkr.Y)

        # Placing the dictionary list
        self.VwDictList.pack(expand=True, fill='both')
        self.VwDictList.config(yscrollcommand=VwScrollBar.set)
        self.VwDictList.place(relx=0.55, rely=0.30, relwidth=0.35, relheight=0.4)

    def pop_up(self, event):

        if self.text_selected():
            text_selected = self.text.get(*self.selection_ind)

            if text_selected in self.non_words:
                try:
                    nd = len(self.candidate_words(text_selected))
                    self.popup_menu.delete(0, nd + 3)
                    c = self.candidate_words(text_selected)
                    if (nd == 0):
                        self.popup_menu.add_command(label="No suggestions.")

                    if (nd > 0):
                        self.popup_menu.add_command(label=f"{c[0][1]} | {c[0][0]}",
                                                    command=lambda: self.select_correct_word(c[0][0]))
                        self.popup_menu.add_separator()
                    
                    if (nd > 1):
                            self.popup_menu.add_command(label = f"{1} | {c[1][0]}", command = lambda: self.select_correct_word(f"{c[1][0]}"))
                    if (nd > 2):
                            self.popup_menu.add_command(label = f"{2} | {c[2][0]}", command = lambda: self.select_correct_word(f"{c[2][0]}"))
                    if (nd > 3):
                            self.popup_menu.add_command(label = f"{3} | {c[3][0]}", command = lambda: self.select_correct_word(f"{c[3][0]}"))
                    if (nd > 4):
                            self.popup_menu.add_command(label = f"{4} | {c[4][0]}", command = lambda: self.select_correct_word(f"{c[4][0]}"))
                    if (nd > 5):
                            self.popup_menu.add_command(label = f"{5} | {c[5][0]}", command = lambda: self.select_correct_word(f"{c[5][0]}"))
                    if (nd > 6):
                            self.popup_menu.add_command(label = f"{6} | {c[6][0]}", command = lambda: self.select_correct_word(f"{c[6][0]}"))
                    if (nd > 0):
                        self.popup_menu.add_separator()
                        self.popup_menu.add_command(label="Add into dictionary", command=lambda: self.add_into_dictionary(text_selected))

                    self.popup_menu.tk_popup(event.x_root, event.y_root)
                finally:
                    self.popup_menu.grab_release()
            else:
                pass
        else:
            pass

    def Submit(self):
       return False

    def text_selected(self):
        if self.non_words:
            self.selection_ind = self.text.tag_ranges(tkr.SEL)
            if self.selection_ind:
                return True
            else:
                return False
        else:
            return False

    def Search(self):
        return False

    def candidate_words(self, error):

        return False

    def add_into_dictionary(self, word):

        if (word.isalpha() and existing_word):
            self.dictionary.append(word)
            self.unigrams.append(word)
            self.counts_u[word] = 1
            self.model_u[word] = 1 / len(self.dictList)
            self.VwDictList.insert(tkr.END, word)

            with io.open("dictionary.txt", "a", encoding="utf-16") as f:
                f.write(f"\n{word}")
            with io.open("clean_economics.txt", "a", encoding="utf-16") as f:
                f.write(f" {word}")

            print("Successfully added word to dictionary.")
        else:
            print("Select only the word, without punctuation or space.")

    def existing_word(self):
        word = self.userSearch.get()
        with io.open("dict.txt", "r", encoding="utf-16") as f:
                        
            if word in f.read():
                print("same")
                return True
            else:
                print("not same")
                return False  
            
    def select_correct_word(self, word):
        return False

    def Reset(self):
        self.text.delete("1.0",tkr.END)
        return


if __name__ == "__main__":
    spellingCheckerGUI = SpellingCheckerGUI()
    spellingCheckerGUI.mainloop()
