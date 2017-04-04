# -*- coding: utf-8 -*-

import time
import datetime
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

class ostools(object):
	def __init__(self):
		self.os = ""
		self.user = ""
		self.ip = ""

	def executa_arruma_casa(self):
		os.system('./arrumacasa.sh')

	def rotina_atualizacao(self, ip, machineid):
		while True:
			os.system('sudo apt-get update')
			os.system('sudo apt-get upgrade')
			sleep(10000)


	def sshconnection(self, ip, port, username, password):
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(ip, port, username, password)
		return ssh

	def execute_ssh_command(self, ssh, command):
		stdin, stdout, stderr = ssh.exec_command(command)
		output = stdout.readlines()
		return output

	def dbconnection(self, ipbanco, rolebanco, nomebanco, userbanco):
		#obfsucar?
		engine = create_engine\
		('postgresql://postgres:postgres@localhost/postgres')
		Session = sessionmaker()
		Session.configure(bind=engine)
		session = Session()
		return session

	def get_user(self):
		user = os.environ.get('USER')
		return user

class user_handlers(object):
	"""Funcoes auxiliares para manejamento da tabela USER"""

	def __init__(self):
		self.user = ""
		self.logged = False


	def cria_user(self, session):
		print "Digite nome de usuario (algartelecom)"
		usernew = raw_input()
		print "Digite senha forte"
		passnew = raw_input()
		newuser = dbmodel.User(user=usernew, password=passnew)
		session.add(newuser)
		session.commit()
		session.flush()
		self.user = newuser.user
		return newuser

	def get_user(self, session, userid):
		founduser = session.query(Users).filter_by(user=userid).first()
		if not founduser:
			return False
		if founduser.user == userid:
			return founduser
		else:
			return False

	def handler_update_user_type(self, session, userid, newtype):
		"""Fazer a verificacao de permissoes previamente"""
		founduser = session.query(User).filter_by(machineid=idmaquina).first()
		if not founduser:
			return False
		founuser.usertype = newtype
		session.commit()
		session.flush()

	def handler_update_user_password(self, session, userid, newpass):
		userfound = session.query(User).filter_by(user=userid).first()
		if not userfound:
			return False
		if userfound.user == userid:
			userfound.password = newpass
			#session.add(userfound)
			session.commit()
			session.flush()
			return userfound

	def delete(self, session, userid):
		userfound = session.query(Users).filter_by(user=userid).delete()
		session.commit()
		session.flush()


	def handler_update_user(self, session, userid):
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



class machine_handler(object):
	"""Classe para ajudar na manipulação da tabela MACHINES"""
	def __init__(self):
		self.machineid = ""
		self.ip = ""

	def delete(self, session, machineid):
		foundmachine = session.query(Machines).\
		filter_by(idmachine=machineid).delete()
		session.commit()
		session.flush


	def get_machine_by_id(self, machineid, session):
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

	def get_machine_by_name(self, machinename, session):
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

	def get_all_machines(self, session):
		"""Retornando em forma de print, nao retorna nenhum objeto"""
		j = PrettyTable(['MachineID', 'Ip', 'Nome', 'Full Compliance',\
		 'Data verificacao'])
		for machine in session.query(Machines).order_by(Machines.scanned):
			j.add_row([machine.machineid, machine.ip, machine.nome, \
			machine.compliance, machine.scanned])
		print j

	def handle_cria_maquina(self, session, idmaquina, nomemachine, \
							scantime, compliancenew, ipmachine):
		newmachine = dbmodel.Machine(machineid=idmaquina, nome=nomemachine\
		, ip=ipmachine, scanned=scantime, compliance=compliancenew)
		session.add(newmachine)
		session.commit()
		session.flush()
		return newmachine

	def handle_update_machine_name(self, session, idmaquina, newnome):
		foundmachine = session.query(Machine).filter_by(machineid=idmaquina).first()
		foundmachine.nome = newnome
		session.commit()
		session.flush()

	def handle_update_machine_scan(self, session, idmaquina, newdate):
		"""Edita o horario para um novo"""
		foundmachine = session.query(Machine).filter_by(machineid=idmaquina).first()
		foundmachine.scanned = newdate
		session.commit()
		session.flush()

	def set_machine_scan_now(self, session, idmaquina):
		"""Coloca o horario atual no scanned"""
		foundmachine = session.query(Machine).filter_by(machineid=idmaquina).first()
		foundmachine.scanned = datetime.datetime
		session.commit()
		session.flush()

	def handler_update_machine_compliance(self, session, idmaquina, boolean):
		foundmachine = session.query(Machine).filter_by(machineid=idmaquina).first()
		if not foundmachine:
			return False
		foundmachine.compliance = boolean
		return foundmachine

	def handler_update_machine_ip(self, session, idmaquina, ipnovo):
		foundmachine = session.query(Machine).filter_by(machineid=idmaquina).first()
		if not foundmachine:
			return False
		foundmachine.ip = ipnovo
		session.commit()
		session.flush()
		return foundmachine

	def get_all_safe(self, session, idmaquina):
		"""Retornando a pretty table"""
		t = PrettyTable(['Id maquina', 'IP maquina'])
		foundmachines = session.query(Machine).filter_by(compliance=True)
		for foundmachine in foundmachines:
			t.add_row([foundmachine.machineid, foundmachine.ip])
		return t

	def get_all_false(self, session, idmaquina):
		"""Retornando a pretty table"""
		t = PrettyTable(['ID maquina', 'Ip maquina'])
		foundmachines = session.query(Machine).filter_by(compliance=False)
		for foundmachine in foundmachines:
			t.add_row([foundmachine.machineid, foundmachine.ip])
		return t




class compliance_handlers(object):
	"""Classe para ajudar no manuseamento da tabela COMPLIANCE_ATTR"""
	def __init__():
		self.machineid = ""

	def get_print(self, session, idmachine):
		"""Retornando print"""
		foundmachine = session.query(Compliance_attr)\
		.filter_by(machineid=idmachine).first()
		machinedict = dict((col, getattr(foundmachine, col))\
			for col in foundmachine.__table__.columns.keys())
		for key, value in custome_dict.iteritems():
			j = PrettyTable(['Nome compliance', 'Valor'])
			j.add_row([key, value])
			print j
			return j

	def delete(self, session, idmachine):
		foundcompliance = session.query(Compliance_attr).\
		filter_by(machineid=idmachine).delete()
		session.commit()
		session.flush()

	def get(self, session, idmachine):
		"""Retornando tabela full"""
		foundcompliance = session.query(Compliance_attr)\
		.filter_by(machineid=idmachine).first()
		if not foundmachine:
			return False
		if foundmachine.machineid == idmachine:
			return foundcompliance
		else:
			return False

	def update_attr(self, session, idmachine, attr):
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

	def cria(self, session, idmaquina):
		print "Criando compliance da maquina " + idmaquina
		newcompliance = dbmodel.Compliance_attr(machineid=idmaquina)
		session.add(newcompliance)
		session.commit()
		session.flush()
		return newcompliance

	def update_obs(self, session, idmaquina, newobs):
		compliancefound = session.query(Compliance_attr).\
		filter_by(machineid=idmaquina).first()
		if not compliancefound:
			return False
		compliancefound.observacoes = newobs
		session.commit()
		session.flush()
		return compliancefound

#handlers criacao de maquinas e compliances
#handlers modificacao de maquinas users e compliances
#handlers deleta dee maquinas users e compliances


def handle_checklist(session, idmaquina):
	t = PrettyTable(['Opcao', 'O que deseja fazer agora?'])
	t.add_row(['1', 'Executar arrumacasa.sh nesta máquina remotamente agora'])
	t.add_row(['2', 'Escanear a maquina e fazer um checklist dos conformes'])
	t.add_row(['3', ''])



ferramenta = ostools()
session = ferramenta.dbconnection(22, 33, 44, 55)
now = time.strftime("%c")
print now



#os.chdir('')
#os.makedirs('')
#os.listdir()
