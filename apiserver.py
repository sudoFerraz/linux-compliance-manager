#THIS IS A WEBSERVER FOR DEMONSTRATING THE TYPES OF RESPONSES WE SEE FROM AN API ENDPOINT
from flask import Flask
import auxiliary
import flask_serialize
from flask import jsonify
from flask import request
import json
app = Flask(__name__)


#GET REQUEST

@app.route('/readHello')
def getRequestHello():
	return "Hi, I got your GET Request!"

@app.route('/getmachine/<int:id>')
def getmachinesid(id):
	if request.method == 'GET':
		foundmachine = flask_serialize.return_machine_serialized(id)
		serialized = jsonify(machineid=foundmachine.machineid, ip=foundmachine.ip, nome=foundmachine.nome, compliance=foundmachine.compliance, scanned=foundmachine.scanned)
		return serialized

@app.route('/getallmachines')
def getallmachines():
	if request.method == 'GET':
		foundmachines = flask_serialize.return_allmachines()
		jsonlist = []
		for machine in foundmachines:
			jsonlist.append(jsonify(machineid=machine.machineid, ip=machine.ip, nome=machine.nome, compliance=machine.compliance, scanned=machine.scanned))
		print jsonlist
		jsonlist = jsonify(machines=jsonlist)
		return jsonlist
		#for machinejson in jsonlist:
		#	jsonanswer

		


#POST REQUEST
@app.route('/createHello', methods = ['POST'])
def postRequestHello():
	return "I see you sent a POST message :-)"
#UPDATE REQUEST
@app.route('/updateHello', methods = ['PUT'])
def updateRequestHello():
	return "Sending Hello on an PUT request!"

#DELETE REQUEST
@app.route('/deleteHello', methods = ['DELETE'])
def deleteRequestHello():
	return "Deleting your hard drive.....haha just kidding! I received a DELETE request!"
""""
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)	"""
    
