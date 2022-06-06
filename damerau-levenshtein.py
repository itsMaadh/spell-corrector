"""
@author: Eric
Description
    - Function for Damerau Levenshtein algorithm
"""

#%% 
import csv

#%%

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


#%% Unit testing
damerau_levenshtein_distance("string", "string")
damerau_levenshtein_distance("string1", "string")
damerau_levenshtein_distance("strivf", "string")
damerau_levenshtein_distance("strasd", "string")

#%% Integration Testing
with open('corpus/dictonary.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
lexicon = data[0]
print(data)


cost_one = []
cost_two = []
cost_three = []
error_word = "currency"

for word in lexicon:
    distance = damerau_levenshtein_distance(error_word,word)

    if distance == 0:
        print("Found the exact word with 0 distance")
        print(f"Input word: {error_word} = Dic Word : {word}" )
        break
    else:
        if distance == 1:
            cost_one.append(word)
            print(f"Cost 1 : {word}")
        elif distance == 2:
            cost_two.append(word)
            print(f"Cost 2 : {word}")
        elif distance == 3:
            cost_three.append(word)
            print(f"Cost 3 : {word}")