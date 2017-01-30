import requests
import json
inputText="how are you"


def getTensorFlowResponse(inputText):
	inputDict={'query':inputText,'dialog':'initial'}
	response=requests.get("http://1aca3d6e.ngrok.io/getAnswer",inputDict)
	print "request getted"
	print response.content
	answer=str(response.content)
	jsonAns=json.loads(answer)
	print jsonAns['response'][0]
	return str(jsonAns['response'][0])
