from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
from bottle import response,request,route,run
from json import dumps
#import pandas as pd
import ConfigParser
import pickle

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
	data=pd.read_csv('trainData_faq.csv',header=None)
	
	classList=[]
	for i in range(0,len(data)):
		print i
		print data[1][i],data[0][i]
		tup=()
		#tuple of description,classification
		tup=(data[1][i],data[0][i])
		classList.append(tup)
	naiveClassifier=NaiveBayesClassifier(classList)
	
	output = open('naivemodel_test.pkl', 'wb')
	pickle.dump(naiveClassifier, output)
	output.close()
	print "training completed"
	item={"result":"training completed"}
	data2.append(item)
	return dumps(data2)

#This method trains without pandas
@route('/trainBot2',method='POST')
def trainBot2():
	response.content_type='application/json'
	data2=[]
	print "training...."
	with open('trainData_faq.csv') as f:
		lines = f.readlines()
		classList=[]
		for i in range(0,len(lines)):
			print lines[i].split(',')[1],"------------",lines[i].split(',')[0]
			tup=()
			tup=(lines[i].split(',')[1],lines[i].split(',')[0])
			classList.append(tup)
		
	naiveClassifier=NaiveBayesClassifier(classList)
	
	output = open('naivemodel_test.pkl', 'wb')
	pickle.dump(naiveClassifier, output)
	output.close()
	print "training completed"
	item={"result":"training completed"}
	data2.append(item)
	return dumps(data2)

#This method classifies the input text based on the trained classifier
@route('/classify',method='POST')
def classify():
	# read python dict back from the file
	pkl_file = open('naivemodel_test.pkl', 'rb')
	naiveClassifier = pickle.load(pkl_file)
	pkl_file.close()
	response.content_type='application/json'
	data=[]
	inputText=request.json["input"]
	print "input text : ",inputText
	predictedClass=naiveClassifier.classify(inputText)
	item={"result":str(predictedClass)}
	data.append(item)
	return dumps(data)
	
#This method classifies the input text based on the trained classifier
@route('/classify2',method='POST')
def classify2():
	# read python dict back from the file
	pkl_file = open('naivemodel_test.pkl', 'rb')
	naiveClassifier = pickle.load(pkl_file)
	pkl_file.close()
	response.content_type='application/json'
	data=[]
	inputText=request.json["input"]
	print "input text : ",inputText
	#predictedClass=naiveClassifier.classify(inputText)
	prob_dist = naiveClassifier.prob_classify(inputText)
	confidence=round(prob_dist.prob(prob_dist.max()), 2)
	print str(confidence)+" "+str(prob_dist.max())
	item={"result":str(confidence)+" "+str(prob_dist.max())}
	data.append(item)
	return dumps(data)
#Method to classify input text
def classifyText(inputText):
	pkl_file = open('naivemodel_test.pkl', 'rb')
	naiveClassifier = pickle.load(pkl_file)
	pkl_file.close()
	predictedClass=naiveClassifier.classify(inputText)
	return str(predictedClass)
#This method classifies and returns others based on confidence score
def classifyTextWithScore(inputText):
	pkl_file = open('naivemodel_test.pkl', 'rb')
	naiveClassifier = pickle.load(pkl_file)
	pkl_file.close()
	prob_dist = naiveClassifier.prob_classify(inputText)
	confidence=round(prob_dist.prob(prob_dist.max()), 2)
	print confidence,prob_dist.max()
	if (confidence<0.92):
		return "others"
	elif(len(inputText.split(" "))<2):
		return "others"
	else:
		return str(prob_dist.max())
	
	
run(host='172.31.45.19', port=7500)


#run(host='192.168.1.7',port=8000)

