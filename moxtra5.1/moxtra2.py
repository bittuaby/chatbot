from bottle import route, run, template,request,response
import json
import requests
import naiveclassifier
import aiml_
@route('/hello')
def index():
	print "hai"
	#return template('<b>Hello </b>!')
	return "moxtra demo"

@route('/askbot',method="POST")
def askbot():
	print "coming ddb"
	#print str (request.body)
	#print json.dumps(request) 
	print request.json["message_type"]
	print request.json["callback_url"]
	callback=request.json["callback_url"]
	print "binder id :",request.json["binder_id"]
	print "user id :",request.json["event"]["user"]["id"]
	userid=str(request.json["event"]["user"]["id"])
	print  "name :",request.json["event"]["user"]["name"]
	inputText=request.json["event"]["comment"]["text"]
	if not(userid=="UhlRgvK87fd98zCy6EcRqD4"):
        	if inputText.lower()=="hi" or inputText.lower()=="hello" :
			reply="hello "+str(request.json["event"]["user"]["name"])+" .. How can i help you.. !"
			responseData={'payload':reply}
			requests.post(callback,data=responseData)
			print "response posted"
		else:
			classifierResponse=naiveclassifier.classifyTextWithScore(inputText)
			if (classifierResponse=="others"):
				reply=aiml_.getResponse(inputText)
				if reply is None:
					responseData={'payload':'I dont want to talk about it..'}
				else:
					responseData={'payload':reply}
				requests.post(callback,data=responseData)
				print "response posted"
			elif (classifierResponse=="Account intent"):
				reply="account intent"
				responseData={'payload':reply}
				requests.post(callback,data=responseData)
				print "response posted"
			elif (classifierResponse=="Transfer intent"):
				reply="transfer intent"
				responseData={'payload':reply}
				requests.post(callback,data=responseData)
				print "response posted"
			elif (classifierResponse=="Transaction intent"):
				reply="transaction intent"
				responseData={'payload':reply}
				requests.post(callback,data=responseData)
				print "response posted"


	else:
		print "automated responses from user to bot not allowed"

	print "coming jkhjdhd"
run(host='172.31.45.19', port=7500)
#run(host='52.42.179.242', port=7500)
