# Precondition
import nltk
from nltk.corpus import gutenberg
import PyPDF2 
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

#%% Extract Content from PDF
page = ""
# creating a pdf file object 
pdfFileObj = open('corpus/dictionary.pdf', 'rb') 
    
# creating a pdf reader object 
pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
    
numOfPages = pdfReader.numPages

for i in range (0, numOfPages):
    print(i)
    pageObj = pdfReader.getPage(10)
    page += pageObj.extractText()

pdfFileObj.close() 

#%% Extract Content from PDF
text_file = open("dic.txt", "w")
n = text_file.write(page)
text_file.close()


#%% Pre-processing - Remove punctuation / Remove extra white space
import string
text_p = ""

text_p = "".join([char for char in page if char not in string.punctuation])
print(text_p)

def remove_whitespace(text):
    return  " ".join(text.split())

remove_whitespace(text_p)

#%% Pre-processing - 
import string

text_p = "".join([char for char in page if char not in string.punctuation])
print(text_p)


#%% Pre-processing - Tokenization


tokens = word_tokenize(page)

porter = nltk.PorterStemmer()
lancaster = nltk.LancasterStemmer()

print("Porter:",[porter.stem(t) for t in tokens])
print("\n")
print("Lancaster:",[lancaster.stem(t) for t in tokens])

