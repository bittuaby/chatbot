from bottle import static_file,route,run
import bottle

@route('/hello')
def tre():
	print "hai"
@route('/static/<filename>')
def send_image(filename):
	print "came inside" 
	return static_file(filename, root='/home/ubuntu/moxtra/static/AccountProofs')
run(host='0.0.0.0',port=8545)
