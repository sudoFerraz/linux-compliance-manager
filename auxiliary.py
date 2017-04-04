# -*- coding: utf-8 -*-

import sys
import sqlalchemy
import os
import paramiko
import hashlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
	newuser = dbmodel.User(user=usernew, password=passnew)
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
	founduser = session.query(Users).filter_by(user=userid).first()
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

#handlers criacao de maquinas e compliances
#handlers modificacao de maquinas users e compliances
#handlers deleta dee maquinas users e compliances

def handle_cria_maquina(session, idmaquina):
	print "Adicionando maquina " + idmaquina
	print "Digite o nome que voce gostaria de atribuir a esta maquina"
	nomemachine = raw_input()
	newmachine = dbmodel.Machine(machineid=idmaquina, nome=nomemachine)
	session.add(newmachine)
	session.commit()
	session.flush()
	return newmachine

def handle_checklist(session, idmaquina):
	t = PrettyTable(['Opcao', 'O que deseja fazer agora?'])
	t.add_row(['1', 'Executar arrumacasa.sh nesta máquina remotamente agora'])
	t.add_row(['2', 'Escanear a maquina e fazer um checklist dos conformes'])
	t.add_row(['3', ''])

def handle_cria_compliance(session, idmaquina):
	print "Criando compliance da maquina " + idmaquina
	newcompliance = dbmodel.Compliance_attr(machineid=idmaquina)
	session.add(newcompliance)
	session.commit()
	session.flush()

def get_machines_compliance_true(session, idmaquina):
	"""Retornando a pretty table"""
	t = PrettyTable(['Id maquina', 'IP maquina'])
	foundmachines = session.query(Machine).filter_by(compliance=True)
	for foundmachine in foundmachines:
		t.add_row([foundmachine.machineid, foundmachine.ip])
	return t

def handler_update_machine_compliance(session, idmaquina, boolean):
	foundmachine = session.query(Machine).filter_by(machineid=idmaquina).first()
	if not foundmachine:
		return False
	foundmachine.compliance = boolean
	return foundmachine

def handler_update_machine_ip(session, idmaquina, ipnovo):
	foundmachine = session.query(Machine).filter_by(machineid=idmaquina).first()
	if not foundmachine:
		return False
	foundmachine.ip = ipnovo
	session.commit()
	session.flush()
	return foundmachine

def handler_update_user_password(session, userid, newpass):
	userfound = session.query(User).filter_by(user=userid).first()
	if not userfound:
		return False
	if userfound.user == userid:
		userfound.password = newpass
		#session.add(userfound)
		session.commit()
		session.flush()
		return userfound


def handler_update_user(session, userid):
	userfound = session.query(Users).filter_by(user=userid).first()
	if not userfound:
		return False
	if userfound.user == userid:
		t = PrettyTable(['Opcao', 'O que deseja modificar?'])
		t.add_row(['1', 'Modificar a senha'])
		t.add_row(['2', 'Modificar o tipo do usuario'])
		t.add_row(['3', 'Sair para o contexto anterior'])
		input(x)
		if x == 1:
			print "Digite a nova senha"
			raw_input(x1)
			print "Digite a nova senha novamente"
			raw_input(x2)
			if x1 == x2:
				founduser = session.query(User).filter_by(user=userid).first()
				founduser.password = x1
			else:
				print "Voce errou a senha, voltando ao menu"
				return founduser
		if x == 2:
			pass





session = dbconnection(22, 33, 44, 55)
eu = handler_update_user_password(session, "gferraz", "teste")





#os.chdir('')
#os.makedirs('')
#os.listdir()
