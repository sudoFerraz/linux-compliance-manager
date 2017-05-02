#THIS IS A WEBSERVER FOR DEMONSTRATING THE TYPES OF RESPONSES WE SEE FROM AN API ENDPOINT
from flask import Flask, render_template
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
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, request, redirect
import matplotlib.pyplot as plt






class LoginForm(FlaskForm):
	username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
	remember = BooleanField('remember me')

app = Flask(__name__, template_folder='')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/postgres'
app.config['SECRET_KEY'] = 'postgres'

db = SQLAlchemy(app)

admin = Admin(app)

ferramenta = auxiliary.ostools()
session = ferramenta.dbconnection(11, 1, 1, 1)
userhandler = auxiliary.user_handlers()
machinehandler = auxiliary.machine_handler()
compliancehandler = auxiliary.compliance_handlers()
login_manager = LoginManager()
login_manager.init_app(app)

def get_machine_graph():
	safecount = 0
	falsecount = 0
	foundmachines = machinehandler.get_all_safe(session)
	for machine in foundmachines:
		safecount = safecount + 1
	foundmachines = machinehandler.get_all_false(session)
	for machine in foundmachines:
		falsecount = falsecount + 1
	machinenumber = falsecount + safecount
	compliancenumber = safecount
	return falsecount, compliancenumber



@app.teardown_request
def app_teardown(response_or_exc):
    # Assuming that `session` is your scoped session 
    session.remove()
    return response_or_exc


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
admin.add_view(MyModelView(Machine, session,editable_columns=['ip', 'nome', 'compliance', 'scanned', 'to_scan', 'to_apply', 'user', 'password'], list_columns=['ip', 'nome', 'compliance', 'scanned', 'to_scan', 'to_apply']))
admin.add_view(MyModelView(Compliance_attr, session))

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return "You are now logged out"

@app.route('/media_attr')
def media_attr():
	attr_machine_list = []
	foundmachines = machinehandler.get_all_machines(session)
	for machine in foundmachines:
		machine_attr_number = compliancehandler.get_number_attr_true(session, machine.id)
		attr_machine_list.append(machine_attr_number)
	#x for x in range(len(attr_machine_list))
	machine_ids = [x for x in range(50)]
	bins = [x for x in range(50)]
	plt.hist(attr_machine_list, bins, histtype='stepfilled',rwidth=0.8)
	plt.xlabel('N of machines with y TRUE attributes')
	plt.ylabel('Number of attributes per machine')
	plt.legend
	#return jsonify(attr_machine_list)
	return plt.show()

@app.route('/testeplot')
def testeplot():
	labels = 'Compliance', 'N-Compliance'
	x, y = get_machine_graph()
	sizes = [y, x]
	explode = (0, 0.1)
	fig1, ax1 = plt.subplots()
	ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
	ax1.axis('equal')
	return plt.show()


@app.route('/teste')
@login_required
def teste():
	return "Testefunfa"

@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == 'GET':
		return render_template('/login.html')
	if request.method == 'POST':
		username = request.form['Username']
		password = request.form['Password']
		user = userhandler.get_user(session, username)
		if user:
			if user.password == password:
				login_user(user)
		elif user == False:
			return '<h1> User not found</h1>'

		return '<h1> You are logged now</h1>'


@app.route('/')
def index():
	#pegar o user com um formulario
	#login_user(user)
	return redirect('/login')


#GET REQUEST

@app.route('/readHello')
def getRequestHello():
	return "Hi, I got your GET Request!"
	session.flush()

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
    
