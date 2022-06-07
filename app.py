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
from tkinter import messagebox

import csv

class SpellingCheckerGUI(tkr.Tk):

    def __init__(self):

        super(SpellingCheckerGUI, self).__init__()
        self.title("Spelling Checker")
        self.minsize(800, 600)

        # reading the corpus/dictonary.csv
    
        with open('corpus/dictonary.csv') as f_object:
            reader = csv.reader(f_object)
            data = list(reader)
        lexicon = data[0]

        # create dict list
        self.dictList= sorted(lexicon)
        self.non_words = []  # empty list of non-words

        self.initUI()


        self.add_into_dictionary("dfdf")
    def initUI(self):

        #GUI

        # Set the canvas and the frame
        canvas = tkr.Canvas(height=800, width=600)
        canvas.pack()
        frame = tkr.Frame(bg='#F0F0F0')  # this is the light gray background
        frame.place(relx=0.5, rely=0.0, relwidth=0.95, relheight=0.8, anchor='n')

        title = tkr.Label(frame, text="Spelling Checker", font="times 23 bold")
        title.place(relx=0.20, rely=0.01, relwidth=0.60)

        # User Guide
        insTitle = tkr.Label(frame, text="User guide:", anchor='w', font="none 10 bold")
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
        self.text = scrolled_text.ScrolledText(frame, width=50, font="Arial 10")
        self.text.pack(expand=True, fill='both')
        self.text.place(relx=0.1, rely=0.30, relwidth=0.35, relheight=0.4)

        # Add popup menu code, binding the right-click to selected text only
        self.popup_menu = tkr.Menu(self, tearoff=0, background='#E0EEEE',
                                  fg='black', activebackground='#C1CDCD',
                                  activeforeground='#00008B')
        self.text.tag_bind("sel", '<Button-3>', self.pop_up)

        # This is the clear button
        ResetButton = tkr.Button(frame, text="Clear", width=7, command=self.Reset)
        ResetButton.place(relx=0.1, rely=0.71)

        # This is the submit button
        SubmitButton = tkr.Button(frame, text="Submit", width=7, command=self.Submit)
        SubmitButton.place(relx=0.20, rely=0.71)

        # Dictionary Text Label
        VwDict = tkr.Label(frame, text="Dictionary:", font="none 10 normal")
        VwDict.place(relx=0.55, rely=0.26)

        # The box containing all the words from the Dictionary
        self.DictListBox = tkr.Listbox(frame, font="none 10 normal")

        for dict_word in self.dictList:
            self.DictListBox.insert(tkr.END, dict_word)

        # Scrollbar should be attached to `DictListBox`
        DictionaryDropDown = tkr.Scrollbar(self.DictListBox, orient=tkr.VERTICAL)
        DictionaryDropDown.config(command=self.DictListBox.yview)
        DictionaryDropDown.pack(side=tkr.RIGHT, fill=tkr.Y)

        # Placing the dictionary list
        self.DictListBox.pack(expand=True, fill='both')
        self.DictListBox.config(yscrollcommand=DictionaryDropDown.set)
        self.DictListBox.place(relx=0.55, rely=0.30, relwidth=0.35, relheight=0.4)

        # This is the search box below the dictionary
        self.userSearch = tkr.StringVar()
        searchBox = tkr.Entry(frame, textvariable=self.userSearch)
        searchBox.place(relx=0.55, rely=0.71, relwidth=0.23)

        SearchButton = tkr.Button(frame, text="Search", width=9, command=self.Search)
        SearchButton.place(relx=0.80, rely=0.71)

        # This is the search box below the dictionary
        self.textAddDict = tkr.StringVar()
        textAddDictBox = tkr.Entry(frame, textvariable=self.textAddDict)
        textAddDictBox.place(relx=0.55, rely=0.76, relwidth=0.23)

        TextAddDictButton = tkr.Button(frame, text="Add to Dictionary", width=15, command=self.Search)
        TextAddDictButton.place(relx=0.80, rely=0.76)
        
        # Original Text Label
        originalTextLabel = tkr.Label(frame, text="Original Text:", font="none 10 normal")
        originalTextLabel.place(relx=0.1, rely=0.77)

        # This text area below is user inputted box. It stores original text
        self.originalText = scrolled_text.ScrolledText(frame, width=50, font="Arial 10")
        self.originalText.pack(expand=True, fill='both')
        self.originalText.place(relx=0.1, rely=0.81, relwidth=0.80, relheight=0.7)

        
    def pop_up(self, event):

        if self.text_selected():
            text_selected = self.text.get(*self.selection_ind)

            if text_selected in self.non_words:
                try:
                    suggestion_count = len(self.candidate_words(text_selected))
                    self.popup_menu.delete(0, suggestion_count + 3)
                    candidate_words_list = self.candidate_words(text_selected)
                    if (suggestion_count == 0):
                        self.popup_menu.add_command(label="No suggestions.")

                    if (suggestion_count > 0):
                        self.popup_menu.add_command(label="candidate_words_list[0][1] | candidate_words_list[0][0]", command=lambda: self.select_correct_word(candidate_words_list[0][0]))
                        self.popup_menu.add_separator()
                    
                    if (suggestion_count > 1):
                            self.popup_menu.add_command(label = "candidate_words_list[1][1] | candidate_words_list[1][0]", command = lambda: self.select_correct_word(candidate_words_list[1][0]))
                    if (suggestion_count > 2):
                            self.popup_menu.add_command(label = "candidate_words_list[2][1] | candidate_words_list[2][0]", command = lambda: self.select_correct_word(candidate_words_list[2][0]))
                    if (suggestion_count > 3):
                            self.popup_menu.add_command(label = "candidate_words_list[3][1] | candidate_words_list[3][0]", command = lambda: self.select_correct_word(candidate_words_list[3][0]))
                    if (suggestion_count > 4):
                            self.popup_menu.add_command(label = "candidate_words_list[4][1] | candidate_words_list[4][0]", command = lambda: self.select_correct_word(candidate_words_list[4][0]))
                    if (suggestion_count > 5):
                            self.popup_menu.add_command(label = "candidate_words_list[5][1] | candidate_words_list[5][0]", command = lambda: self.select_correct_word(candidate_words_list[5][0]))
                    if (suggestion_count > 6):
                            self.popup_menu.add_command(label = "candidate_words_list[6][1] | candidate_words_list[6][0]", command = lambda: self.select_correct_word(candidate_words_list[6][0]))
                    if (suggestion_count > 0):
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

    # Reference : https://datascience.stackexchange.com/questions/60019/damerau-levenshtein-edit-distance-in-python
    def damerau_levenshtein_distance(checker_word, dictonary_word):

        d = {}
        lenstr1 = len(checker_word)
        lenstr2 = len(dictonary_word)
        for i in range(-1,lenstr1+1):
            d[(i,-1)] = i+1
        for j in range(-1,lenstr2+1):
            d[(-1,j)] = j+1
        
        for i in range(lenstr1):
            for j in range(lenstr2):
                if checker_word[i] == dictonary_word[j]:
                    cost = 0
                else:
                    cost = 1
                d[(i,j)] = min(
                    d[(i-1,j)] + 1, # deletion
                    d[(i,j-1)] + 1, # insertion
                    d[(i-1,j-1)] + cost, # substitution
                    )
                if i and j and checker_word[i]==dictonary_word[j-1] and checker_word[i-1] == dictonary_word[j]:
                    d[(i,j)] = min (d[(i,j)], d[i-2,j-2] + cost) # transposition

        return d[lenstr1-1,lenstr2-1]

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
        word = self.userSearch.get()
        if word in self.dictList:
            result = self.dictList.index(word)
            self.VwDictList.selection_set(result)
            self.VwDictList.see(result)
        else:
            messagebox.showerror("Not found", "No such keyword(s).")

    def candidate_words(self, error):

        return False

    def add_into_dictionary(self, word):
        if(self.existing_word(word)):
            if (word.isalpha()):
                self.dictList.append(word)
                #self.unigram_model.append(word)
                #self.counts_unigram[word] = 1
                #self.model_unigram[word] = 1 / len(self.dictList)
                word = ","+word

                with open('corpus/dictonary.csv', 'a') as f_object:
                    writer = csv.writer(f_object, delimiter = ' ')
                    # write the data
                    writer.writerow(word.split(" "))

                messagebox.showinfo("Message","The word added successfully into dictionary.")
                self.DictListBox.insert(tkr.END, word)
            else:
                messagebox.showerror("Error","Select only the word, without space or special characters.")
        else:
            messagebox.showerror("Error","The word already exist in the dictionary")
            

    def existing_word(self,word):
        with open('corpus/dictonary.csv') as f_object:
            reader = csv.reader(f_object)
            data = list(reader)
        lexicon = data[0]              
        if word in lexicon:
            print("same")
            return False
        else:
            print("not same")
            return True
        
    def select_correct_word(self, word):
        return False

    def Reset(self):
        self.text.delete("1.0",tkr.END)
        return


if __name__ == "__main__":
    spellingCheckerGUI = SpellingCheckerGUI()
    spellingCheckerGUI.mainloop()
