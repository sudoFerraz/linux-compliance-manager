import sys
import sqlalchemy
import os
import paramiko
import hashlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pexpect import pxssh
from dbmodel import User, Machine, Compliance_attr
from prettytable import PrettyTable
import dbmodel
from sqlalchemy import inspect


dbip = 11111111111
arrumacasa = './arrumacasa.sh'

def executa_arruma_casa():
	os.system('./arrumacasa.sh')

def sshconnection(ip, port, username, password):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ip, port, username, password)
	return ssh

def execute_ssh_command(ssh, command):
	stdin, stdout, stderr = ssh.exec_command(command)
	output = stdout.readlines()
	return output

def dbconnection(ipbanco, rolebanco, nomebanco, userbanco):
	#obfsucar?
	engine = create_engine\
	('postgresql://postgres:postgres@localhost/postgres')
	Session = sessionmaker()
	Session.configure(bind=engine)
	session = Session()
	return session

def handle_cria_user(session):
	print "Digite nome de usuario (algartelecom)"
	usernew = raw_input()
	print "Digite senha forte"
	passnew = raw_input()
	newuser = dbmodel.User(user=usernew, passw=passnew)
	session.add(newuser)
	session.commit()
	session.flush()
	return newuser.user

def handle_logon(session):
	print "Digite usuario (algartelecom)"
	usertry = raw_input()
	print "Digite senha"
	passtry = raw_input()
	founduser = session.query(User).filter_by(user=usertry).first()
	if not founduser:
		print "Login incorreto, tente novamente"
		return False
	if founduser.user == usertry:
		if founduser.password == passtry:
			print "Login efetuado com sucesso como" + founduser.user
			return founduser.user
		else:
			print "Login incorreto, tente novamente"
			return False
	else:
		print "Login incorreto, tente novamente"
		return False

def get_machine_by_id(machineid, session):
	foundmachine = session.query(Machines).filter_by(idmachine=machineid).first()
	if not foundmachine:
		print "Maquina nao encontrada, tente novamente"
		return False
	if foundmachine.idmachine == machineid:
		#print prettytable
		return foundmachine
	else:
		print "Maquina nao encontrada, tente novamente"
		return False


def get_machine_by_name(machinename, session):
	foundmachine = session.query(Machines).filter_by(nome=machinename).first()
	if not foundmachine:
		print "Maquina nao encontrada, tente novamente"
		return False
	if foundmachine.nome == machinename:
		#print prettytable
		return foundmachine
	else:
		print "Maquina nao encontrada, tente novamente"
		return False

def get_all_machines(session):
	"""Retornando em forma de print, nao retorna nenhum objeto"""
	j = PrettyTable(['MachineID', 'Ip', 'Nome', 'Full Compliance',\
	 'Data verificacao'])
	for machine in session.query(Machines).order_by(Machines.scanned):
		j.add_row([machine.machineid, machine.ip, machine.nome, machine.compliance,\
		 machine.scanned])
	print j

def get_machine_compliance_print(session, idmachine):
	"""Retornando print"""
	foundmachine = session.query(Compliance_attr)\
	.filter_by(machineid=idmachine).first()
	machinedict = dict((col, getattr(foundmachine, col))\
		for col in foundmachine.__table__.columns.keys())
	for key, value in custome_dict.iteritems():
		j = PrettyTable(['Nome compliance', 'Valor'])
		j.add_row([key, value])
		print j

def get_machine_compliance(session, idmachine):
	foundmachine = session.query(Compliance_attr)\
	.filter_by(machineid=idmachine).first()
	if not foundmachine:
		return False
	if foundmachine.machineid == idmachine:
		return foundmachine
	else:
		return False

def update_machine_compliance(session, idmachine, attr):
	foundmachine = session.query(Compliance_attr)\
	.filter_by(machineid=idmachine).first()
	if not foundmachine:
		return False
	if foundmachine.machineid == idmachine:
		inst = inspect(Compliance_attr)
		attr_names = [c_attr.key for c_attr in inst.mapper.columns_attrs]
		if attr in attr_names:
			if foundmachine.attr == True:
				foundmachine.attr = False
				session.add(foundmachine)
				session.commit()
				session.flush()
			if foundmachine.attr == False:
				foundmachine.attr = True
				session.add(foundmachine)
				session.commit()
				session.flush()
	else:
		return False


def get_user(session, userid):
	founduser = sesison.query(Users).filter_by(user=userid).first()
	if not founduser:
		return False
	if founduser.user == userid:
		return founduser
	else:
		return False




def notificate(offense, user):
	pass


def investigation(path, wordlist, user):
	for dirpath, dirnames, filenames in os.walk(path):
		print 'Caminho atual' + dirpath
		print 'Diretorios' + str(dirnames)
		print 'Arquivos' + str(filenames)
		for dirname in dirnames:
			if dirname in wordlist:
				notificate(dirname, user)
		for filename in filenames:
			if filename in wordlist:
				notificate(filename, user)

def get_user():
	user = os.environ.get('USER')
	return user

session = dbconnection(22, 33, 44, 55)
usernew = "gferraz"
namenew = "Gabriel Ferraz"
passwordnew = "123"
usertypenew = "admin"
#newuser = dbmodel.User(user=usernew, password=passwordnew, \
#	usertype=usertypenew, name=namenew)
#session.add(newuser)
eu = session.query(User).filter_by(user=usernew).first()
doido = "usertype"
eu.doido = "LUL"
session.add(eu)
session.commit()
session.flush()
print eu.usertype




#os.chdir('')
#os.makedirs('')
#os.listdir()