import paste
from bottle import route, run, template,request,response
import json
import requests
import naiveclassifier
import aiml_
import os
import os.path
import emailSend
import transferIntent
import transactionIntent
import accountIntent
@route('/hello')
def index():
	print "hai"
	#return template('<b>Hello </b>!')
	return "moxtra demo"


#This function gets the current classification if already present
#the classifier function will not be called on the inputText if in middle of a usecase
#By default classification is set as 'nil'
def getSessionClassification(userid):
	print "get session"
	filename="sessions/"+userid+".tx"
	if os.path.isfile(filename):
		with open(filename) as f:
                	lines = f.readlines()
			for line in lines:
				userid_session=line.split(',')[0]
				if(userid==userid_session):
					return str(line.split(',')[1])
	else:
		return "nil"

#This function sets the classification for the user based on userid
def setSessionClassification(userid,classification):
	print "set session"
	filename="sessions/"+userid+".tx"
	lines=""
	if os.path.isfile(filename):
		with open(filename) as f:
                	lines = f.readlines()
			lines[0]=userid+","+classification+"\n"
		with open(filename,'w')as f:
			f.writelines(lines)	
	else:
		file = open(filename,'w')
		file.write(userid+","+classification+"\n")
		file.close()

#This function retrieves the current step in a use case conversation
#the steps are stored in a conversation.cv file
def getIntentSteps(userid,classification):
	filename="sessions/"+userid+".tx"
        if os.path.isfile(filename):
                with open(filename) as f:
                        lines = f.readlines()
                        userid_session=lines[0].split(',')[0]
                        if(userid==userid_session):
                        	return str(lines[1].split(',')[1])
        else:
                return "nil"

#This function retrieves the current step in the middle of a conversation
def setIntentSteps(userid,step,classification):
        print "set session"
        filename="sessions/"+userid+".tx"
	lines=""
        if os.path.isfile(filename):
                with open(filename) as f:
                        lines = f.readlines()
                        lines[1]=userid+","+step+"\n"
		with open(filename,'w') as f:
			f.writelines(lines) 	
        else:
                file = open(filename,'w')
                file.write(userid+","+classification+"\n"+userid+",step1\n")
                file.close()
#This function initializes session for a user
def initSession(userid,username):
	filename="sessions/"+userid+".tx"
        if not os.path.isfile(filename):
		file = open(filename,'w')
		if username.strip()=="":
			username="Annie"
                file.write(userid+",nil\n"+userid+",step1\n"+userid+","+username+"\n"+userid+",483678945\n")
                file.close()
		print "session initialized"
	else:
		print "session not initialized"


#The /askbot url reieves the json input from moxtra webhooks when a cooment is posted based on integration
@route('/askbot',method="POST")
def askbot():
	#print json.dumps(request) 
	print request.json["message_type"]
	print request.json["callback_url"]
	callback=request.json["callback_url"]
	print "binder id :",request.json["binder_id"]
	print "user id :",request.json["event"]["user"]["id"]
	userid=str(request.json["event"]["user"]["id"])
	username=str(request.json["event"]["user"]["name"])
	initSession(userid,username)
	getSessionClassification(userid)
	print  "name :",request.json["event"]["user"]["name"]
	inputText=request.json["event"]["comment"]["text"]
	print "inputText : ",inputText
	#The askbot url will be called if user posts a message to bot and vice versa.. We dont want to handle when bot is sending
	#a response back to the user.. the below userid is of "citimoxtra bot"
	if not(userid=="UhlRgvK87fd98zCy6EcRqD4"):
		inputDict={'query':inputText,'dialog':'initial'}
		response=requests.get("http://68209509.ngrok.io/getAnswer",inputDict)
		print "request getted"
		print response.content
		answer=str(response.content)
		jsonAns=json.loads(answer)
		print jsonAns['response'][0]
		responseData={'payload':str(jsonAns['response'][0])}
		requests.post(callback,data=responseData)
		print "response posted"

	else:
		print "automated responses from user to bot not allowed"

	


	

	


run(host='172.31.45.19', port=7500,server='paste')
#run(host='52.42.179.242', port=7500)
