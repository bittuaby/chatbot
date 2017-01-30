import pandas as pd
import nltk
from nltk.corpus import stopwords
stop = stopwords.words('english')
import re
import numpy as np

def number_removal(row):
    data = row['Summary']
    #print data
    #tokens = nltk.wordpunct_tokenize(data)
    #print type(data)
    if type(data)!=int:
        line = re.sub(r"[^A-Za-z\s]", " ", data.strip())
        tokens = line.split()
    else:
        tokens=[]
    #tokens =[token for token in tokens if token in english_vocab]
    #token_list = []
    #for token in tokens:
    #result = ''.join([i for i in token if not i.isdigit() and i.isalnum()])
    #token_list.append(result.lower())
    return ' '.join(tokens)


frequency_words_wo_stop = {}
def generate_word_frequency(row):
    data = row['Summary']
    tokens = nltk.wordpunct_tokenize(data)
    token_list = []
    for token in tokens:
        if token.lower() not in stop:
            token_list.append(token.lower())
            if token.lower() in frequency_words_wo_stop:
                count = frequency_words_wo_stop[token.lower()]
                count = count + 1
                frequency_words_wo_stop[token.lower()] = count
            else:
                frequency_words_wo_stop[token.lower()] = 1
    
    return ','.join(token_list)

from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()


def receieve(query):
    data=pd.DataFrame([query])
    data.columns=['Summary']
    data['Summary'] = data.apply(number_removal,axis=1)
    
    data['tokens'] = data.apply(generate_word_frequency,axis=1)
    
    big=[]
    for i in data['tokens']:
        st=''
        ls=[]
        for j in i.split(','):
            #print j
            ls.append(wordnet_lemmatizer.lemmatize(j))
        #print ls
        big.append(' '.join(ls))
    data['Summary_lem']=big
    return data['Summary_lem']