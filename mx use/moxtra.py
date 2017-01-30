from bottle import route, run, template,request,response
import json
import requests
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
			reply="Sorry.. I have no answer for that at the moment.."
                	responseData={'payload':reply}
                	requests.post(callback,data=responseData)
                	print "response posted"
	else:
		print "automated responses from user to bot not allowed"

	print "coming jkhjdhd"
run(host='172.31.45.19', port=7500)
#run(host='52.42.179.242', port=7500)
