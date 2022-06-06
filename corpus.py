# Precondition
# https://vitalflux.com/python-extract-text-pdf-file-using-pdfminer/

import numpy as np
from pdfminer.high_level import extract_text
from nltk.probability import FreqDist
from nltk.tokenize import RegexpTokenizer
import csv

#%% Pre-processing - Stemming

def process_pdf(path, save_to="corpus/default.csv"):
    
    """
    Description: extract PDF file contents to produce the corpus data
    Parameters:
        - path (str): PDF directory
    Return:
        - array (string) : unique words from PDF
    """ 
    # ref https://vitalflux.com/python-extract-text-pdf-file-using-pdfminer/
    
    text = extract_text(path)
    tokenizer = RegexpTokenizer('\w+')
    tokens = np.unique(tokenizer.tokenize(text))
    freqdist = FreqDist(tokens)
    
    tokens = [words for words in tokens if len(words) > 0 and freqdist[words] > 0]
    print("Extract complete")
    
    return tokens

path = "corpus/an-introduction-to-business-v1.0.pdf"
pdf_conent = process_pdf(path)

len(np.unique(pdf_conent))
#%% Pre-processing - Stemming

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

#%% Pre-processing - Stemming

