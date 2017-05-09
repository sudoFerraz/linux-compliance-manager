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
from dbmodel import BossHelper
from dbmodel import Graphics
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, request, redirect
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os.path as op
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import BaseView, expose
from jinja2 import Markup
from flask import url_for
from flask_admin import form
import os
from dbmodel import Image

basedir = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.join(basedir, 'static')



class LoginForm(FlaskForm):
	username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
	remember = BooleanField('remember me')

app = Flask(__name__, template_folder='')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/postgres'
app.config['SECRET_KEY'] = 'postgres'

db = SQLAlchemy(app)

class NotificationsView(BaseView):
	@expose('/')
	def index(self):
		return self.render('admin/notify.html')

admin = Admin(app, template_mode='bootstrap3')

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



class ImageView(ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''

        return Markup(
            '<img src="%s">' %
            url_for('static',
                    filename=form.thumbgen_filename(model.path))
        )

    column_formatters = {
        'path': _list_thumbnail
    }

    form_extra_fields = {
        'path': form.ImageUploadField(
            'Image', base_path=file_path, thumbnail_size=(100, 100, True))
    }

admin.add_view(ImageView(Image, session))


@app.route('/_image-url')
def _get_image_url():
    img_id = request.args.get('img_id')
    img = Image.query.get(img_id)
    if img is None:
        response = jsonify(status='not found')
        return response
    return jsonify(img_path=img.path, status='ok')



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



path = op.join(op.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))
admin.add_view(MyModelView(User, session,editable_columns=['user', 'name', 'password', 'usertype'], list_columns=['user', 'name', 'password', 'usertype']))
admin.add_view(MyModelView(Machine, session,editable_columns=['ip', 'nome', 'compliance', 'scanned', 'to_scan', 'to_apply', 'user', 'password'], list_columns=['ip', 'nome', 'compliance', 'scanned', 'to_scan', 'to_apply']))
admin.add_view(MyModelView(Compliance_attr, session))
admin.add_view(MyModelView(BossHelper, session))
admin.add_view(NotificationsView(name='Notifications', endpoint='notify'))



#class Myform(BaseForm):
#	upload = ImageUploadField('File', thumbgen=thumb_name)

def thumb_name(filename):
	name, _ = op.splitet(filename)
	return secure_filename('%s-thumb.jpg' % name)

def prefix_name(obj, file_data):
	parts = op.splitext(file_data.filename)
	return secure_filename('file-%s%s' % parts)

#class MyForm(BaseForm):
#	upload = FileUploadField('File', namegen=prefix_name)


@app.route('/logout')
@login_required
def logout():
	logout_user()
	return "You are now logged out"

import numpy as np
from matplotlib import mlab

"""@app.route('/plotest')
def plotest():
	x0 = np.random.randn(500)
	x1 = np.random.randn(500)+1

	trace1 = go.Histogram(x=x0, histnorm='count', name='control', autobinx=False,xbins=dict(start=-3.5, end=3.0,size=0.5), marker=dict(color='#FFD7E9'), opacity=0.75)
	trace2 = go.Histogram(x=x1, name='experimental', autobinx=False, xbins=dict(start=-2.0,end=5,size=0.5), marker=dict(color='#EB89B5'), opacity=0.75)
	data = [trace1, trace2]
	layout = go.Layout(title='Sampled Resutls', xaxis=dict(title='Value'), yaxis=dict(title='Count'), bargap=0.2, bargroupgap=0.1)
	fig = go.Figure(data=data, layout=layout)
	py.iplot(fig, filename='Styled histogram')
"""
@app.route('/matplottest')
@login_required
def matplottest():
	np.random.seed(0)
	mu = 200
	sigma = 25
	n_bins = 50
	x = np.random.normal(mu, sigma, size=100)

	fig, ax = plt.subplots(figsize=(8, 4))
	n, bins, patches = ax.hist(x, n_bins, normed=1, histtype='step', cumulative=True, label='Empirical')
	y = mlab.normpdf(bins, mu, sigma).cumsum()
	y /= y[-1]

	ax.plot(bins, y, 'k--', linewidth=1.5, label='Theoretical')
	ax.hist(x, bins=bins, normed=1, histtype='step', cumulative=-1, label='Reversed emp.')

	ax.grid(True)
	ax.legend(loc='right')
	ax.set_title('Cumulative step histograms')
	ax.set_xlabel('Annual rainfall (mm)')
	ax.set_ylabel('Likelihood of occurrence')
	return plt.show()




@app.route('/positive_attr')
def media_attr():
	attr_machine_list = []
	id_machine_list = []
	foundmachines = machinehandler.get_all_machines(session)
	for machine in foundmachines:
		machine_attr_number = compliancehandler.get_number_attr_true(session, machine.id)
		attr_machine_list.append(machine_attr_number)
		id_machine_list.append(machine.nome)
	#x for x in range(len(attr_machine_list))
	"""machine_ids = [x for x in range(50)]
	bins = [x for x in range(50)]
	plt.hist(attr_machine_list, bins, histtype='stepfilled',rwidth=0.8)
	"""#return jsonify(attr_machine_list)
	#teste
	attr_machine_list.append(22)
	attr_machine_list.append(52)
	attr_machine_list.append(12)
	attr_machine_list.append(2)
	y = [x for x in range(len(attr_machine_list))]
	plt.bar(y, attr_machine_list)
	plt.xlabel('Number of positive attributes')
	plt.ylabel('Number of machines')
	legenda = mpatches.Patch(color='blue', label='X = MachineID')
	plt.legend(handles=[legenda])
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

@app.route('/severityplot')
def severityplot():
	labels = 'severity', 'machine'
	severity_machine_list = []
	id_machine_list = []
	foundmachines = machinehandler.get_all_machines(session)
	for machine in foundmachines:
		machine_severity = compliancehandler.get_severity_sum(session, machine.id)
		severity_machine_list.append(machine_severity)
		id_machine_list.append(machine.id)
	#x = [x for x in range(len(severity_machine_list))]
	#y = severity_machine_list
	#plt.bar(x, y, label='Severity-per-machine')
	#plt.show()
	#bins = [x for x in range(len(severity_machine_list))]
	#plt.hist(severity_machine_list, bins, histtype='stepfilled')
	y = [x for x in range(len(severity_machine_list))]
	y.append(y[-1]+1)
	plt.scatter(id_machine_list, severity_machine_list, color='r', s=100, marker='X')
	plt.grid(True)
	plt.xticks(y)
	plt.ylabel("Severity degree")
	plt.xlabel("Machine ID")
	return plt.show()

@app.route('/pie_severity')
def pie_severity():
	x,y,z = 0,0,0
	labels = 'Grupo de Baixo Risco', 'Grupo de Medio Risco', 'Grupo de Alto Risco'
	severity_machine_list = []
	id_machine_list = []
	foundmachines = machinehandler.get_all_machines(session)
	for machine in foundmachines:
		machine_severity = compliancehandler.get_severity_sum(session, machine.id)
		severity_machine_list.append(machine_severity)
		#RETIRAR PARA PRODUCAOO
		severity_machine_list.append(3)
	for severity in severity_machine_list:
		if severity < 20:
			x = x + 1
		elif severity >= 20 and severity <= 90:
			y = y + 1
		elif severity > 90:
			z = z + 1

	sizes = [x, y, z]
	explode = (0,0,0.1)
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


@app.route('/testelogin', methods=['POST', 'GET'])
def testelogin():
	if request.method == 'POST':
		return 


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

app.run(host='0.0.0.0')

