import re
import math
import string
import nltk
from collections import Counter
from nltk.util import ngrams
from nltk.metrics.distance  import edit_distance
from nltk.tokenize import regexp_tokenize
import csv

import tkinter as tkr
from tkinter import ttk
import tkinter.scrolledtext as scrolled_text
from tkinter import messagebox

from nltk.corpus import abc, stopwords

# https://www.nltk.org/nltk_data/
nltk.download('punkt')
nltk.download('abc')  # Australian Broadcasting Commission
nltk.download('stopwords')

class SpellingCheckerGUI(tkr.Tk):

    def __init__(self):
        print("Initializing...")

        super(SpellingCheckerGUI, self).__init__()
        self.title("Spelling Checker")
        self.minsize(800, 600)

        # reading the corpus/dictonary.csv, updated to correct encoding.
    
        with open('corpus/dictonary.csv', encoding='iso-8859-1') as f_object:
            reader = csv.reader(f_object)
            data = list(reader)
        lexicon = data[0]

        # create dict list
        self.dictList= sorted(lexicon)
        self.non_words = []  # empty list of non-words

        """ Modelling """
        # https://www.geeksforgeeks.org/n-gram-language-modelling-with-nltk/

        # input the ABC sentences
        sents = abc.sents()

        # write the removal characters such as : Stopwords and punctuation
        stop_words = set(stopwords.words('english'))
        string.punctuation = string.punctuation +'"'+'"'+'-'+'''+'''+'—'
        removal_list = list(stop_words) + list(string.punctuation)+ ['lt','rt']

        # generate unigrams bigrams trigrams
        self.unigram=[]
        bigram=[]
        trigram=[]
        tokenized_text=[]
        for sentence in sents:
            sentence = list(map(lambda x:x.lower(),sentence))
            for word in sentence:
                if word== '.':
                    sentence.remove(word)
                else:
                    self.unigram.append(word)
        
            tokenized_text.append(sentence)
            bigram.extend(list(ngrams(sentence, 2,pad_left=True, pad_right=True)))
            trigram.extend(list(ngrams(sentence, 3, pad_left=True, pad_right=True)))
        
        # remove the n-grams with removable words
        def remove_stopwords(x):    
            y = []
            for pair in x:
                count = 0
                for word in pair:
                    if word in removal_list:
                        count = count or 0
                    else:
                        count = count or 1
                if (count==1):
                    y.append(pair)
            return (y)

        # print(len(unigram))
        # unigram = remove_stopwords(unigram)
        # bigram = remove_stopwords(bigram)
        # trigram = remove_stopwords(trigram)

        # print(len(unigram))

        # Create unigram model
        N_u = len(lexicon)
        self.counts_u = dict(Counter(self.unigram))
	
        model_u = {}
        for (key,value) in zip(self.counts_u.keys(), self.counts_u.values()):
            model_u[key] = value/N_u
        self.model_u = model_u

        # create left bigrams (the usual bigram), right bigrams and trigrams
        self.bigramsl = list(ngrams(self.unigram, 2))
        self.bigramsr = [(w1,w2) for (w1,w2) in zip(self.unigram[1:],
                                                    self.unigram[:-1])]
        self.counts_bl = dict(Counter(self.bigramsl))
        self.counts_br = dict(Counter(self.bigramsr))
        N_b = len(self.bigramsl)

        self.trigrams = list(ngrams(self.unigram, 3))
        self.counts_t = dict(Counter(self.trigrams))

        # print(self.trigrams)

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
        ins5 = tkr.Label(frame, text="5. Right-click the selected error word.", anchor='w')
        ins5.place(relx=0.1, rely=0.22, relwidth=0.60)
        ins6 = tkr.Label(frame, text="6. Choose one candidate correction word, or add the selected word to dictionary.", anchor='w')
        ins6.place(relx=0.1, rely=0.25, relwidth=0.60)


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

        # This is the search box below the dictionary
        #self.textAddDict = tkr.StringVar()
        #textAddDictBox = tkr.Entry(frame, textvariable=self.textAddDict)
        #textAddDictBox.place(relx=0.55, rely=0.80, relwidth=0.23)

        #TextAddDictButton = tkr.Button(frame, text="Add to Dictionary", width=15, command=self.Search)
        #TextAddDictButton.place(relx=0.80, rely=0.80)
        
        # Original Text Label
        originalTextLabel = tkr.Label(frame, text="Original Text:", font="none 10 normal")
        originalTextLabel.place(relx=0.1, rely=0.83)

        # This text area below is user inputted box. It stores original text
        self.originalText = scrolled_text.ScrolledText(frame, width=50, font="Arial 10")
        self.originalText.pack(expand=True, fill='both')
        self.originalText.place(relx=0.1, rely=0.80, relwidth=0.80, relheight=0.2)


    def right_click_pop_up_menu(self, evt):

        if self.highlighted_text():
            highlighted_text = self.text.get(*self.selection_ind)

            if highlighted_text in self.non_words:
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
                    if (suggestion_count > 6):
                            self.right_click_menu.add_command(label = f"{candidate_words_list[6][1]} | {candidate_words_list[6][0]}", command = lambda: self.select_correct_word(candidate_words_list[6][0]))
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

        model_br = {}
        for key, value in zip(self.counts_br.keys(), self.counts_br.values()):
            model_br[key] = value / self.counts_u[key[0]]

        return model_bl, model_br


    def make_trigram_model(self):

        model_t = {}
        for key, value in zip(self.counts_t.keys(), self.counts_t.values()):
            model_t[key] = value / ((self.counts_bl[key[:2]] + self.counts_br[key[-1:-3:-1]]) / 2)

        return model_t

    def Submit(self):
        self.non_words = []

        # Clear textbox that displays original input
        self.originalText.configure(state = 'normal')
        self.originalText.delete('1.0', tkr.END)

        # get the user input (ui)
        user_input = self.text.get('1.0', 'end-1c')

        ui = user_input.lower()
        ui.replace("?", ".")
        ui.replace("!", '.')
        sent_list = ui.split('.')

        for i in range(len(sent_list)):
            sent_list[i] = 'OSO ' + sent_list[i] + ' OEO'

        ui = ' '.join(sent_list)
        ui = re.sub('\s+', ' ', ui)
        ui = regexp_tokenize(ui, "[\w']+")
        print("Split user input")
        print(ui)

        # make unigrams, bigrams and trigrams out of user input
        uni = [w for w in ui if not w.isdigit()]
        bl = list(ngrams(uni, 2))
        br = [(w1,w2) for (w1,w2) in zip(uni[1:],uni[:-1])]
        tri = list(ngrams(uni, 3))

        # make bigrams and trigrams out of corpus
        left_bi, right_bi = self.make_bigram_model()
        tri_model = self.make_trigram_model()

        utext = ' '.join(uni)

        score_list = [] # this is the score list for real-word errors
        for t in tri:
            # non-word spellchecking
            if t[1] not in self.dictList:
                self.non_words.append(t[1])

        # print(self.dictList)
        print("non real words")
        print(self.non_words)

        # real-word spellchecking
        # only occurs if there are no non-word errors
        # uses Stupid Backoff with weighted scoring on trigrams,
        # left bigrams, and right bigrams
        if not self.non_words:
            for t in tri:
                d = 0.4    # backoff discount
                ll = 0.25  # weighting on left bigram
                lt = 0.5   # weighting on trigram
                lr = 0.25  # weighting on right bigram
                threshold = 0.0002 # 6e-5  # threshold score to be considered a real-word error
                    
                if t in tri_model:
                    p_t = tri_model[t]
                elif ((t[:2] in left_bi) and (t[-1:-3:-1] in right_bi)):
                    p_t = (d/2)*(left_bi[t[:2]] + right_bi[t[-1:-3:-1]])
                elif (t[:2] in left_bi):
                    p_t = d*left_bi[t[:2]]
                elif (t[-1:-3:-1] in right_bi):
                    p_t = d*right_bi[t[-1:-3:-1]]
                else:
                    p_t = d*d*self.model_u[t[1]]

                if t[:2] in left_bi:
                    p_bl = left_bi[t[:2]]
                else:
                    p_bl = d*self.model_u[t[1]]

                if t[-1:-3:-1] in right_bi:
                    p_br = right_bi[t[-1:-3:-1]]
                else:
                    p_br = d*self.model_u[t[1]]

                score = ll*p_bl + lt*p_t + lr*p_br
                score = round(score, 3 - int(math.floor(math.log10(abs(score)))) - 1)
                score_list.append(score)
                if score < threshold:
                    self.non_words.append(t[1])
                
        
        # https://stackoverflow.com/questions/24819123/how-to-get-the
        # -index-of-word-being-searched-in-tkinter-text-box
        # code from above website
        self.text.tag_config("red_tag", foreground = "red")
        for err in self.non_words:
            offset = '+%dc' % len(err)
            pos_start = self.text.search(err, '1.0', tkr.END)
            while pos_start:
                pos_end = pos_start + offset
                self.text.tag_add("red_tag", pos_start, pos_end)
                pos_start = self.text.search(err, pos_end, tkr.END)
        
        self.originalText.insert(tkr.INSERT, user_input)
        self.originalText.configure(state = 'disabled')

        print("Score list")
        if not self.non_words:
            print(score_list)
            print("No non-word errors.\n")
        else:
            print(score_list)
            print('\n')

        return self.non_words

    def highlighted_text(self):
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
            self.DictListBox.selection_set(result)
            self.DictListBox.see(result)
        else:
            messagebox.showerror("Not found", "No such keyword(s).")

    def check_non_real_word_errors(self, word):
        temp = [(w, edit_distance(word, w, 2, True)) for w in self.dictList if w[0]==word[0]] # Why must the first letter stay the same?
        return sorted(temp, key = lambda x: x[1])[:6]
        # print(sorted(temp, key = lambda val:val[0])[0][1])

    def candidate_words(self, error):
        candidates_ = self.check_non_real_word_errors(error)
        if candidates_[0][1] == 0:
            candidates_.pop(0)
        print("Candidates")
        print(candidates_[:5])

        return candidates_[:5]

    def add_into_dictionary(self, word):
        if(self.existing_word(word)):
            if (word.isalpha()):
                self.dictList.append(word)
                #self.unigram_model.append(word)
                #self.counts_unigram[word] = 1
                #self.model_unigram[word] = 1 / len(self.dictList)
                
                word = ","+word

                with open('corpus/dictonary.csv', 'a', newline='', encoding="ISO-8859-1") as f_object:
                    writer = csv.writer(f_object, delimiter = ' ',  lineterminator='')
                    # write the data
                    writer.writerow(word.split(" "))
                f_object.close()
                
                messagebox.showinfo("Message","The word added successfully into dictionary.")
                self.DictListBox.insert(tkr.END, word.replace(",",""))
            else:
                messagebox.showerror("Error","Select only the word, without space or special characters.")
        else:
            messagebox.showerror("Error","The word already exist in the dictionary")

    def existing_word(self,word):
        with open('corpus/dictonary.csv', encoding="ISO-8859-1") as f_object:
            reader = csv.reader(f_object)
            data = list(reader)
        lexicon = data[0]              
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
