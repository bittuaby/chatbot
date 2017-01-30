from flask import Flask,make_response,render_template, request, jsonify, json,jsonify,send_from_directory
from flask.ext.cors import CORS, cross_origin
import requests
app = Flask(__name__)  
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
@app.route('/getAnswer')    
@cross_origin() 
def getAnswer():
    """ Server side end point from user """
    userQuery = request.args.get("query") 
    userDialog = request.args.get("dialog") # handles the user diaog
	
    #print (request.environ['REMOTE_ADDR'])
    print (userDialog,userQuery)
    '''res=answer(userQuery)
    print (res,userDialog)
    if 'Oops try again' in res:
        print ('in if')
        #response,userDialog=getReply(userQuery,userDialog)'''
        
    response="hello"
    response=requests.post('http://192.168.1.8:7500/askbot',json={ "message_id": "2889",
    "message_type": "comment_posted",
    "binder_id": "BAGUChIRH7P7eBdR9h9nyR5",
    "callback_url": "https://api.moxtra.com/webhooks/CAEqBS8wcXkzehdCQUdVQ2hJUkg3UDdlQmRSOWg5bnlSNYABvBaQAxQ",
  	"userid":"Utkj3YC5BxRHCCaq9widP67",
  	"username":"Bittu Aby",
  	"inputText":userQuery})
    print "giving response : ",str(response.content)
    answer=str(response.content)
    return jsonify(response=answer,id="1",status="suc",dialog=userDialog)
    '''else:
        return jsonify(response=res,id="1",status="suc",dialog=userDialog)'''
  

@app.route('/')
@app.route('/index')
@cross_origin()
def index():
    #return make_response(send())
    #headers = {'Content-Type': 'text/html'}    
    return make_response(render_template('index.html'),200)
	
if __name__ == '__main__':
	app.run(host='0.0.0.0',processes=True,debug=True,port=8000)