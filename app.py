import re
import math
from collections import Counter
from nltk.util import ngrams
from nltk.metrics.distance  import edit_distance
import csv

import tkinter as tkr
import tkinter.scrolledtext as scrolled_text
from tkinter import END, messagebox

class SpellingCheckerGUI(tkr.Tk):

    def __init__(self):
        print("Initializing...")

        super(SpellingCheckerGUI, self).__init__()
        self.title("Spelling Checker")
        self.minsize(800, 600)

        # read dictionary
        with open('corpus/dictonary.txt', encoding='iso-8859-1') as file:
            lines = file.readlines()
            lexicon = [line.rstrip() for line in lines]

        # create dict list
        self.dictList= sorted(lexicon)
        self.non_real_words = []  # empty list of non-words

        # read corpus
        with open('corpus/corpus.txt', encoding='iso-8859-1') as file:
            lines = file.readlines()
            corpus_text = lines[0].split(' ')

        self.unigram = []
        for word in corpus_text:
            # Only include alphanumeric words that are not numeric and not single letters
            if re.match("\w+", word) and not word.isnumeric() and len(word) != 1:
                self.unigram.append(word.lower())

        # Create unigram model
        N_u = len(lexicon)
        self.counts_u = dict(Counter(self.unigram))
	
        model_u = {}
        for (key,value) in zip(self.counts_u.keys(), self.counts_u.values()):
            model_u[key] = value/N_u
        self.model_u = model_u

        # create bigram
        self.bigramsl = list(ngrams(self.unigram, 2))
        self.counts_bl = dict(Counter(self.bigramsl))

        self.initUI()

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
        ins1 = tkr.Label(frame, text="1. Input text in the given text area.", anchor='w')
        ins1.place(relx=0.1, rely=0.10, relwidth=0.60)
        ins2 = tkr.Label(frame, text="2. Click on the 'Clear' button to clear the text area.", anchor='w')
        ins2.place(relx=0.1, rely=0.13, relwidth=0.60)
        ins3 = tkr.Label(frame, text="3. Click on the 'Submit' button to proceed.", anchor='w')
        ins3.place(relx=0.1, rely=0.16, relwidth=0.60)
        ins4 = tkr.Label(frame, text="4. Double-click a highlighted word to select it.", anchor='w')
        ins4.place(relx=0.1, rely=0.19, relwidth=0.60)
        ins5 = tkr.Label(frame, text="5. Right-click the highlighted error word.", anchor='w')
        ins5.place(relx=0.1, rely=0.22, relwidth=0.60)
        ins6 = tkr.Label(frame, text="6. Choose one candidate correction word, or add the selected word into dictionary.", anchor='w')
        ins6.place(relx=0.1, rely=0.25, relwidth=0.70)


        # Text Label
        textlabel = tkr.Label(frame, text="Enter input here (500 words max)", font="none 10 normal")
        textlabel.place(relx=0.1, rely=0.30)
        
        # This is the big text box where user puts in their input
        self.text = scrolled_text.ScrolledText(frame, width=50, font="Arial 10")
        self.text.pack(expand=True, fill='both')
        self.text.place(relx=0.1, rely=0.34, relwidth=0.35, relheight=0.4)

        # Add right-click menu code, binding the right-click to selected text only
        self.right_click_menu = tkr.Menu(self, tearoff=0, background='#E0EEEE',
                                  fg='black', activebackground='#C1CDCD',
                                  activeforeground='#00008B')
        self.text.tag_bind("sel", '<Button-3>', self.right_click_pop_up_menu)

        # This is the clear button
        ResetButton = tkr.Button(frame, text="Clear", width=7, command=self.Reset)
        ResetButton.place(relx=0.1, rely=0.75)

        # This is the submit button
        SubmitButton = tkr.Button(frame, text="Submit", width=7, command=self.Submit)
        SubmitButton.place(relx=0.20, rely=0.75)

        # Dictionary Text Label
        VwDict = tkr.Label(frame, text="Dictionary:", font="none 10 normal")
        VwDict.place(relx=0.55, rely=0.30)

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
        self.DictListBox.place(relx=0.55, rely=0.34, relwidth=0.35, relheight=0.4)

        # This is the search box below the dictionary
        self.userSearch = tkr.StringVar()
        searchBox = tkr.Entry(frame, textvariable=self.userSearch)
        searchBox.place(relx=0.55, rely=0.75, relwidth=0.23)

        SearchButton = tkr.Button(frame, text="Search", width=9, command=self.Search)
        SearchButton.place(relx=0.80, rely=0.75)
        
        # Original Text Label
        originalTextLabel = tkr.Label(frame, text="Original Text:", font="none 10 normal")
        originalTextLabel.place(relx=0.1, rely=0.83)

        # This text area below is user inputted box. It stores original text
        self.originalText = scrolled_text.ScrolledText(frame, width=50, font="Arial 10")
        self.originalText.pack(expand=True, fill='both')
        self.originalText.place(relx=0.1, rely=0.80, relwidth=0.80, relheight=0.2)


    def right_click_pop_up_menu(self, evt):

        if self.highlighted_text():
            highlighted_text = self.text.get(*self.selection_ind).lower()

            if highlighted_text in self.non_real_words:
                try:
                    suggestion_count = len(self.candidate_words(highlighted_text))
                    self.right_click_menu.delete(0, suggestion_count + 3)
                    candidate_words_list = self.candidate_words(highlighted_text)
                    if (suggestion_count == 0):
                        self.right_click_menu.add_command(label="No suggestions.")

                    if (suggestion_count > 0):
                        self.right_click_menu.add_command(label=f"{candidate_words_list[0][1]} | {candidate_words_list[0][0]}", command=lambda: self.select_correct_word(candidate_words_list[0][0]))
                        self.right_click_menu.add_separator()
                    
                    if (suggestion_count > 1):
                            self.right_click_menu.add_command(label = f"{candidate_words_list[1][1]} | {candidate_words_list[1][0]}", command = lambda: self.select_correct_word(candidate_words_list[1][0]))
                    if (suggestion_count > 2):
                            self.right_click_menu.add_command(label = f"{candidate_words_list[2][1]} | {candidate_words_list[2][0]}", command = lambda: self.select_correct_word(candidate_words_list[2][0]))
                    if (suggestion_count > 3):
                            self.right_click_menu.add_command(label = f"{candidate_words_list[3][1]} | {candidate_words_list[3][0]}", command = lambda: self.select_correct_word(candidate_words_list[3][0]))
                    if (suggestion_count > 4):
                            self.right_click_menu.add_command(label = f"{candidate_words_list[4][1]} | {candidate_words_list[4][0]}", command = lambda: self.select_correct_word(candidate_words_list[4][0]))
                    if (suggestion_count > 5):
                            self.right_click_menu.add_command(label = f"{candidate_words_list[5][1]} | {candidate_words_list[5][0]}", command = lambda: self.select_correct_word(candidate_words_list[5][0]))
                    if (suggestion_count > 0):
                        self.right_click_menu.add_separator()
                        self.right_click_menu.add_command(label="Add into dictionary", command=lambda: self.add_into_dictionary(highlighted_text))

                    self.right_click_menu.tk_popup(evt.x_root, evt.y_root)
                finally:
                    self.right_click_menu.grab_release()

    def make_bigram_model(self):

        model_bl = {}
        for key, value in zip(self.counts_bl.keys(), self.counts_bl.values()):
            model_bl[key] = value / self.counts_u[key[0]]

        return model_bl


    def Submit(self):
        self.non_real_words = []

        # Clear textbox that displays original input
        self.originalText.configure(state = 'normal')
        self.originalText.delete('1.0', tkr.END)

        # Re-colour all text black
        self.text.tag_delete("red_tag")

        # get the user input (ui)
        user_input = self.text.get('1.0', 'end-1c')

        # sanitizing input by removing non-alphanumerics from the input
        sanitized_input = re.sub("[^a-zA-Z0-9\s\-']+", "", user_input)
        # remove any extra whitespaces
        sanitized_input = re.sub(" +", " ", sanitized_input)
        # sanitizing input by turning all the letters to lowercase
        sanitized_input = sanitized_input.lower()
        # split input by whitespaces
        ui = sanitized_input.split(" ")

        # Testing with
        # The Latest reaches on COVID 19 Treatments and Medications

        print("\nSanitized and split user input:")
        print(ui)

        # make unigrams and bigrams out of user input
        uni = [w for w in ui if not w.isdigit()]
        bigram = list(ngrams(uni, 2))

        # make bigram out of corpus
        bigram_model = self.make_bigram_model()
        # print(bigram_model)

        score_list = [] # this is the score list for real-word errors
        for u in uni:
            # non-word spellchecking
            if u not in self.dictList:
                self.non_real_words.append(u)

        # print(self.dictList)
        print("\nNon-real words found:")
        print(self.non_real_words)

        # real-word spellchecking
        # only occurs if there are no non-word errors
        # uses bigram model
        if not self.non_real_words:
            for b in bigram:
                d = 0.4
                ll = 1 # 0.25  # weighting on bigram
                threshold = 6e-5  # threshold score to be considered a real-word error
                if len(b[0]) == 1:
                    continue

                if b in bigram_model:
                    p_bl = bigram_model[b]
                elif b[0] in self.model_u:
                    p_bl = d*self.model_u[b[0]]

                score = ll*p_bl
                score = round(score, 3 - int(math.floor(math.log10(abs(score)))) - 1)
                score_list.append(score)
                if score < threshold:
                    self.non_real_words.append(b[0])
                
        
        # https://stackoverflow.com/questions/24819123/how-to-get-the
        # -index-of-word-being-searched-in-tkinter-text-box
        # code from above website
        self.text.tag_config("red_tag", foreground = "#FF0000")
        for err in self.non_real_words:
            offset = '+%dc' % len(err)
            pos_start = self.text.search(err, '1.0', tkr.END, nocase=True)
            while pos_start:
                pos_end = pos_start + offset
                self.text.tag_add("red_tag", pos_start, pos_end)
                pos_start = self.text.search(err, pos_end, tkr.END, nocase=True)
        
        self.originalText.insert(tkr.INSERT, user_input)
        self.originalText.configure(state = 'disabled')

        print("\nScore list")
        if not self.non_real_words:
            print(score_list)
            print("No non-word errors.\n")
        else:
            print(score_list)
            print('\n')

        return self.non_real_words

    def highlighted_text(self):
        if self.non_real_words:
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
            self.DictListBox.selection_set(result)
            self.DictListBox.see(result)
        else:
            messagebox.showerror("Not found", "No such keyword(s).")

    def candidate_words(self, word):
        temp = [(w, edit_distance(word, w, 2, True)) for w in self.dictList if w[0]==word[0]]
        # get a sorted listed of edit distances for each word
        # print(sorted(temp, key = lambda val:val[1]))
        all_candidates = sorted(temp, key = lambda val:val[1])
        if all_candidates[0][1] == 0:
            all_candidates.pop(0)
        
        # if it is a non-real word, get top 5 from dictionary
        # else get top 5 edit distance and use the unigram model as well
        if word in self.non_real_words:
            print('Candidates\n', all_candidates[:5])
            return all_candidates[:5]
        else:
            # create a list of candidates that are within the edit distance threshold
            distance_one = []
            distance_two = []
            distance_three = []

            for candidate in all_candidates:
                    # if the edit distance is 1, add the word to the list
                    # and the unigram probability of the word appearing
                    # in the dictionary
                    if(candidate[1] == 1):
                        distance_one.append((candidate[0], candidate[1], self.model_u[candidate[0]] if candidate[0] in self.unigram else 0))
                    elif(candidate[1] == 2):
                        distance_two.append((candidate[0], candidate[1], self.model_u[candidate[0]] if candidate[0] in self.unigram else 0))
                    elif(candidate[1] == 3):
                        distance_three.append((candidate[0], candidate[1], self.model_u[candidate[0]] if candidate[0] in self.unigram else 0))
                    else:
                        pass

            def sort_by_unigram_probability(val):
                return val[2]

            # sort the list of candidates by the unigram probability
            distance_one = sorted(distance_one, key=sort_by_unigram_probability, reverse=True)
            distance_two = sorted(distance_two, key=sort_by_unigram_probability, reverse=True)
            distance_three = sorted(distance_three, key=sort_by_unigram_probability, reverse=True)

            # combine all the lists of candidates
            candidates = distance_one + distance_two + distance_three

            # return the top 5 candidates
            print('Candidates\n', candidates[:5])
            return candidates[:5]

    def add_into_dictionary(self, word):
        if(self.non_existing_word(word)):
            self.dictList.append(word)

            with open('corpus/dictonary.txt', 'a', newline='', encoding="ISO-8859-1") as f_object:
                f_object.write(word + "\n")
                f_object.close()
                    
            messagebox.showinfo("Message","The word added successfully into dictionary.")
            self.DictListBox.insert(tkr.END, word.replace(",",""))

        else:
            messagebox.showerror("Error","The word already exist in the dictionary")

    def non_existing_word(self,word):
        #with open('corpus/dictonary.txt', encoding="ISO-8859-1") as f_object:
        #    reader = csv.reader(f_object)
        #    data = list(reader)
        #    lexicon = data[0]
        with open('corpus/dictonary.txt', encoding='iso-8859-1') as file:
            lines = file.readlines()
            lexicon = [line.rstrip() for line in lines]
            if word in lexicon:
                return False
            else:
                return True
        
    def select_correct_word(self, word):
        self.text.delete(*self.selection_ind)
        self.text.insert(tkr.INSERT, word)

    def Reset(self):
        self.text.delete("1.0",tkr.END)
        return


if __name__ == "__main__":
    spellingCheckerGUI = SpellingCheckerGUI()
    spellingCheckerGUI.mainloop()
