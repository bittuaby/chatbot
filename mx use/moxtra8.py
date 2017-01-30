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
        	if inputText.lower()=="hi" or inputText.lower()=="hello" :
			fname="users/"+userid
			if(os.path.isfile(fname)):
				reply="Welcome back "+str(request.json["event"]["user"]["name"])+".. Hope you are doing good.\nWhat do you want to do today ?"
			else:
				reply="Hi "+str(request.json["event"]["user"]["name"])+" .. I am HelloCiti.. \nI can help you find what you need and get things done."
				setSessionClassification(userid,"firstChat")
				file = open(fname,'w')
			responseData={'payload':reply}
			requests.post(callback,data=responseData)
			print "response posted"
		#to cancel the user journey in between
        	elif inputText.lower()=="stop" or inputText.lower()=="cancel" :
			reply="Cancelling the transaction..."
			setSessionClassification(userid,"nil")
                        setIntentSteps(userid,"step1","nil")
                        delname=userid+"_transfer.sum"
			if(os.path.isfile(delname)):
                        	os.remove(delname)
                        delname=userid+"_transaction.sum"
			if(os.path.isfile(delname)):
                        	os.remove(delname)

			responseData={'payload':reply}
			requests.post(callback,data=responseData)
			print "response posted"
		else:
			classifierResponse=getSessionClassification(userid).strip()
			print "after get response ,",classifierResponse
			#classifier is called only if there is no classification set in the session
			if classifierResponse=="nil":
				print "no classification present"
				classifierResponse=naiveclassifier.classifyTextWithScore(inputText)
				if "others" not in classifierResponse:
					setSessionClassification(userid,classifierResponse)
					setIntentSteps(userid,"step1",classifierResponse)
			elif classifierResponse=="firstChat":
				print "continuing first chat"
				classifierResponse=naiveclassifier.classifyTextWithScore(inputText)
				if "others" not in classifierResponse:
                                        setSessionClassification(userid,classifierResponse)
                                        setIntentSteps(userid,"step1",classifierResponse)
				else:
					reply="We are all setup.. To learn about what you can do,you can select any of the following\n"
					reply=reply+"\n1.Service Management\n2.Payment Management\n3.Receivable Management " 
                                        setSessionClassification(userid,"secondChat")

					responseData={'payload':reply}
					requests.post(callback,data=responseData)
					return
			elif classifierResponse=="secondChat":
				print "checking options"
				classifierResponse=naiveclassifier.classifyTextWithScore(inputText)
				if "others" not in classifierResponse:
                                        setSessionClassification(userid,classifierResponse)
                                        setIntentSteps(userid,"step1",classifierResponse)
				elif ("2" in inputText or "payment" in inputText.lower()):
                                        setSessionClassification(userid,"thirdChat")
					reply="What would you like to do under payment management ?\n\n"
					reply=reply+"1.Initiate a payment via preformat\n2.Authorize payment"
					responseData={'payload':reply}
					requests.post(callback,data=responseData)
					return
                                #elif("3" in inputText or "service" in inputText.lower()or "1"in inputText.lower()or "recievable" in inputText.lower()):
				else:        
					reply="Sorry i am not able to handle this request at the moment ?\n\n"
	                                setSessionClassification(userid,"nil")
					responseData={'payload':reply}
					requests.post(callback,data=responseData)
					return

			elif classifierResponse=="thirdChat":
				print "checking options"
				classifierResponse=naiveclassifier.classifyTextWithScore(inputText)
				if "others" not in classifierResponse:
                                        setSessionClassification(userid,classifierResponse)
                                        setIntentSteps(userid,"step1",classifierResponse)
				elif ("1" in inputText):
					print "1 came.. go"
					classifierResponse="Transfer intent"
                                        setSessionClassification(userid,"Transfer intent")
				#elif("2" in inputText or "authorize" in inputText.lower()):
				else:
					reply="Sorry.. I am unable to handle this request at the moment"
	                                setSessionClassification(userid,"nil")
                                        
					responseData={'payload':reply}
					requests.post(callback,data=responseData)
					return
	
			#loads aiml for generic conversation in case of others
			if (classifierResponse=="others"):
				reply=aiml_.getResponse(inputText)
				if reply is None:
					responseData={'payload':'I dont want to talk about it..'}
				else:
					responseData={'payload':reply}
				requests.post(callback,data=responseData)
				print "response posted"
			elif (classifierResponse=="Account intent"):
 				step=getIntentSteps(userid,"Account intent")
                                reply=accountIntent.getConversationResponse(userid,step,inputText)
                                reply=accountIntent.getReply(userid,step,inputText)
				print "reply"
				#reply="account intent"
				responseData={'payload':reply}
				requests.post(callback,data=responseData)
				print "response posted"
			elif (classifierResponse=="Transfer intent"):
				print "should come here"
				step=getIntentSteps(userid,"Transfer intent")
				reply=transferIntent.getConversationResponse(userid,step,inputText)
				if(reply=="next"):
					step=getIntentSteps(userid,"Transfer intent")
					reply=transferIntent.getConversationResponse(userid,step,inputText)
				if(reply=="aiml"):
					reply=aiml_.getResponse(inputText)

				#reply="transfer intent"
				responseData={'payload':reply}
				requests.post(callback,data=responseData)
				print "response posted"
			elif (classifierResponse=="Transaction intent"):
				step=getIntentSteps(userid,"Transaction intent")
				reply=transactionIntent.getConversationResponse(userid,step,inputText)
				if(reply=="next"):
					step=getIntentSteps(userid,"Transaction intent")
					reply=transactionIntent.getConversationResponse(userid,step,inputText)

				#reply="transaction intent"
				responseData={'payload':reply}
				requests.post(callback,data=responseData)
				print "response posted"
			elif(classifierResponse=="Book hotel"):
				requests.post(callback,files={'file': open('hotelbooking.jpg', 'rb')})
				print "image posted"
		 		setSessionClassification(userid,"nil")
                                setIntentSteps(userid,"step1","nil")
			elif(classifierResponse=="Start video"):
				requests.post(callback,files={'file': open('citivideo.mp4', 'rb')})
				print "video posted"
		 		setSessionClassification(userid,"nil")
                                setIntentSteps(userid,"step1","nil")
			elif(classifierResponse=="Account Proof"):
				#fname=generatePdf(userid)
				if (username.strip()==""):
					username="Annie"
				#pdfGenerator.createAccountConfirmationPDF("67895346","LU46034000067895346",username,"USD","CITILUX")
				reply="ok.. Here you go.."
				responseData={'payload':reply}
                                requests.post(callback,data=responseData)
                                print "response posted"

				fname='Account Proof.pdf'
				requests.post(callback,files={'file': open(fname, 'rb')})
				print "image posted"
				
				emailSend.sendMail('pankajsuresh.bande@cognizant.com','Account Proof.pdf')
				
				reply="A copy of the document is sent to your registered email also.."
				responseData={'payload':reply}
                                requests.post(callback,data=responseData)
                                print "response posted"

		 		setSessionClassification(userid,"nil")
                                setIntentSteps(userid,"step1","nil")





	else:
		print "automated responses from user to bot not allowed"

	


	

	


run(host='172.31.45.19', port=7500,server='paste')
#run(host='52.42.179.242', port=7500)
