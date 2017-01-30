from bottle import response,request,route,run
from json import dumps
import ConfigParser
import pickle
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import pickle

from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
def fun(dat):
    big=[]
    for i in dat['Summary']:
        st=''
        ls=[]
        for j in i.split(','):
            #print j
            ls.append(wordnet_lemmatizer.lemmatize(j))
        #print ls
        big.append(' '.join(ls))
    return big




#Initialization starts
#configParser=ConfigParser.RawConfigParser()
#configFilePath="Config.cfg"
#configParser.read(configFilePath)
#Host=configParser.get('file','host')
#Port=configParser.get('file','port')

#Config read ends


#This method trains and creates a classifier from training data in csv file
@route('/trainBot',method='POST')
def trainBot():
    response.content_type='application/json'
    data2=[]
    print "training...."
    data=pd.read_csv('trainData.csv',header=None)
    import preprocess
    from preprocess import number_removal,generate_word_frequency
    import re
   #print data
    data.columns=['Intent','Summary']
        
    data['Summary']=data.apply(number_removal,axis=1)
    data['Summary'] = data.apply(generate_word_frequency,axis=1)
        
    data['Summary']=fun(data)
        
    from nltk.corpus import stopwords
    stop = stopwords.words('english')
    stop.extend(('.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}','/','-'))
        
    for i in ['ask','alexa','allexa','tel','tell']:
        stop.append(i)
            
    le=LabelEncoder()
    X=data['Summary'].fillna('')
    y=data['Intent'].fillna('')
    y=le.fit_transform(y)
    
    classifier = Pipeline([
    ('vec',CountVectorizer(strip_accents='unicode',stop_words=stop)),
    ('tfidf', TfidfTransformer()),
    ('clf', RandomForestClassifier(n_estimators=10,random_state=0))])
    
    classifier=classifier.fit(X, y)
    
    
    f = open('random_forest_model.pickle', 'wb')
    pickle.dump(classifier, f)
    f.close()
    
    f = open('label.pickle', 'wb')
    pickle.dump(le, f)
    f.close()
        
    print "training completed"
    item={"result":"training completed"}
    data2.append(item)
    return dumps(data2)

	
#This method classifies the input text based on the trained classifier
@route('/classify2',method='POST')
def classify2():
    # read python dict back from the file
    f = open('random_forest_model.pickle', 'rb')
    classifier=pickle.load(f)
    f.close()
    
    f = open('label.pickle', 'rb')
    label=pickle.load(f)
    f.close()
    response.content_type='application/json'
    data=[]
    inputText=request.json["input"]
    print "input text : ",inputText
    confidence=classifier.predict_proba([inputText])
    index=np.argmax(confidence)
    
    predicted_class=label.inverse_transform(classifier.predict([inputText]))
    
    print str(round(confidence[0][index],2))+" "+ predicted_class[0]
    
    item={"result":str(round(confidence[0][index],2))+" "+ predicted_class[0]}
    data.append(item)
    return dumps(data)


#This method classifies and returns others based on confidence score
def classifyTextWithScore(inputText):
    f = open('random_forest_model.pickle', 'rb')
    classifier=pickle.load(f)
    f.close()
    
    f = open('label.pickle', 'rb')
    label=pickle.load(f)
    f.close()
    
    confidence=classifier.predict_proba([inputText])
    index=np.argmax(confidence)
    
    predicted_class=label.inverse_transform(classifier.predict([inputText]))
    
    
    print round(confidence[0][index],2),predicted_class
    if (round(confidence[0][index],2)<0.7):
        return "others"
    elif(len(inputText.split(" "))<2):
	return "others"
    else:
	return predicted_class[0]
	
#run(host='172.31.45.19', port=7500)
#print "hai"
print classifyTextWithScore("payments made last week where remitter bank wants to stop the payment")


#run(host='192.168.1.7',port=8000)

