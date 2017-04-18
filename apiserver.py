#THIS IS A WEBSERVER FOR DEMONSTRATING THE TYPES OF RESPONSES WE SEE FROM AN API ENDPOINT
from flask import Flask
import auxiliary
import flask_serialize
from flask import jsonify
from flask import request
import json
import dbmodel
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from dbmodel import User
from dbmodel import Machine
from dbmodel import Compliance_attr
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length





class LoginForm(FlaskForm):
	username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
	remember = BooleanField('remember me')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/postgres'
app.config['SECRET_KEY'] = 'postgres'

db = SQLAlchemy(app)

admin = Admin(app)

ferramenta = auxiliary.ostools()
session = ferramenta.dbconnection(11, 1, 1, 1)

class MyModelView(ModelView):
    def __init__(self, model, session, name=None, category=None, endpoint=None, url=None, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

        super(MyModelView, self).__init__(model, session, name=name, category=category, endpoint=endpoint, url=url)

    def is_accessible(self):
        # Logic
        return True

class ComplianceView(ModelView):
	column_display_pk = True
	column_hide_backrefs = False
	column_list = ('machineid', 'observacoes', 'proposito', 'particionamento')

admin.add_view(MyModelView(User, session,editable_columns=['user', 'name', 'password', 'usertype'], list_columns=['user', 'name', 'password', 'usertype']))
admin.add_view(ModelView(Machine, session))
admin.add_view(ModelView(Compliance_attr, session))


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
		jsonlist = jsonify(jsonlist)
		return jsonlist
		#for machinejson in jsonlist:
		#	jsonanswer

@app.route('/')
def getroot():
	return "Hello" 


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
    
