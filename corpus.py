# Precondition
# https://vitalflux.com/python-extract-text-pdf-file-using-pdfminer/

import numpy as np
from pdfminer.high_level import extract_text
from nltk.probability import FreqDist
from nltk.tokenize import RegexpTokenizer
import csv
import re

#%%
def process_pdf(path, save_to="corpus/dictonary.csv"):
    
    """
    Description: extract PDF file contents to produce the corpus data
    Parameters:
        - path (str): PDF directory
        - save_to (str): exported CSV file directory
    Return:
        - list (string) : filtered unique tokens from PDF
    """ 
    # ref https://vitalflux.com/python-extract-text-pdf-file-using-pdfminer/
    
    #-----------------------------------
    # Preprocessing                    #
    #-----------------------------------
    
    text = extract_text(path) # high level api function - to extract pdf text using pdfminer
    tokenizer = RegexpTokenizer('[A-z]\w+') # create a regex token object
    tokens = tokenizer.tokenize(text) # tokenize the text
    unique_tokens = np.unique(tokens) # extract the unique tokens as the vocab dictonary
    freqdist = FreqDist(tokens) # get the frequency distribution of the corpus
    
    #-----------------------------------
    # Generating the lexicon/dictonary #
    #-----------------------------------
    
    # Remove text shorter than N and freq less than M
    filtered_unique_tokens = [words for words in unique_tokens if len(words) > 1 and freqdist[words] > 5]

    # Exporting to CSV File
    with open(save_to, 'w') as f:
        write = csv.writer(f)
        write.writerow(filtered_unique_tokens)
    
    #-----------------------------------
    # Generating the corpus            #
    #-----------------------------------
      
    cleanCorpus = re.sub('[^A-Za-z0-9]+',' ', text) 
    
    text_file = open("corpus/corpus.txt", "w")
    text_file.write(cleanCorpus)  # write string to file
    text_file.close() #close file
 

    # Provide a simple statistics of the PDF   
    print(f"Number of Words in PDF               : {len(text)}")
    print(f"Number of tokens                     : {len(tokens)}")
    print(f"Number of unique tokens              : {len(unique_tokens)}")
    print(f"Number of filtered unique tokens     : {len(filtered_unique_tokens)}")
    print("Extract complete")
    
    return filtered_unique_tokens

path = "corpus/covid19.pdf"
pdf_conent = process_pdf(path)


#%%

def stemming(data, stemmer):
    """
    Description: breaking the raw text into small chunks
    Parameters:
        - data: raw text data
        - stemmer: nltk stemmer object
    Return:
        - list/array of stemmed text
    """
    return [stemmer.stem(t) for t in data]

#%%
import pandas as pd
read_file = pd.read_csv (r'corpus/dictonary.txt')
read_file.to_csv (r'corpus/dictonary.csv', index=None)


