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
from sqlalchemy.orm.scoping import scoped_session

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

	def get_hash_machine_id(macaddress):
		machineid = hashlib.sha256(macaddress).hexdigest()
		return machineid



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
		Session = scoped_session(sessionmaker())
		Session.configure(bind=engine)
		session = Session
		return session

	def get_user(self):
		user = os.environ.get('USER')
		return user

class user_handlers(object):
	"""Funcoes auxiliares para manejamento da tabela USER"""

	def __init__(self):
		self.user = ""
		self.logged = False

	def login(self):
		print "Digite usuario (algartelecom)"
		usertry = raw_input()
		print "Digite senha"
		passtry = raw_input()
		founduser = session.query(User).filter_by(user=usertry).first()
		if not founduser:
			return ""
		if founduser.password == passtry:
			print "Login efetuado com sucesso"
			self.user = founduser
			self.logged = True
			return founduser.user
		else:
			print "Login nao efetuado, tente novamente"
			return ""


	def cria_user(self, session):
		print "Digite nome de usuario (@algartelecom.com.br)"
		usernew = raw_input()
		print "Digite senha forte"
		passnew = raw_input()
		print "Digite seu nome"
		nomenew = raw_input()
		newuser = dbmodel.User(user=usernew, password=passnew, name=nomenew)
		session.add(newuser)
		session.commit()
		session.flush()
		self.user = newuser.user
		return newuser

	def get_user(self, session, username):
		founduser = session.query(User).filter_by(user=username).first()
		if not founduser:
			return False
		if founduser.user == username:
			return founduser
		else:
			return False

	def handler_update_user_type(self, session, userid, newtype):
		"""Fazer a verificacao de permissoes previamente"""
		founduser = session.query(User).filter_by(id=userid).first()
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
		foundmachine = session.query(Machine).\
		filter_by(id=machineid).delete()
		session.commit()
		session.flush


	def get_machine_by_id(self, idmachine, session):
		foundmachine = session.query(Machine).filter_by(id=idmachine).first()
		if not foundmachine:
			print "Maquina nao encontrada, tente novamente"
			return False
		if foundmachine.id == idmachine:
			#print prettytable
			return foundmachine
		else:
			print "Maquina nao encontrada, tente novamente"
			return False

	def get_machine_by_name(self, machinename, session):
		foundmachine = session.query(Machine).filter_by(nome=machinename).first()
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
		j = PrettyTable(['MachineID', 'Ip', 'Nome', 'Full Compliance',\
		 'Data verificacao'])
		foundmachines = session.query(Machine).order_by(Machine.scanned)
		for machine in foundmachines:
			j.add_row([machine.id, machine.ip, machine.nome, \
			machine.compliance, machine.scanned])
		return foundmachines

	def handle_cria_maquina(self, session, idmaquina, nomemachine, \
							scantime, compliancenew, ipmachine):
		newmachine = dbmodel.Machine(id=idmaquina, nome=nomemachine\
		, ip=ipmachine, scanned=scantime, compliance=compliancenew)
		session.add(newmachine)
		session.commit()
		session.flush()
		return newmachine

	def handle_update_machine_name(self, session, idmaquina, newnome):
		foundmachine = session.query(Machine).filter_by(id=idmaquina).first()
		foundmachine.nome = newnome
		session.commit()
		session.flush()

	def handle_update_machine_scan(self, session, idmaquina, newdate):
		"""Edita o horario para um novo"""
		foundmachine = session.query(Machine).filter_by(id=idmaquina).first()
		foundmachine.scanned = newdate
		session.commit()
		session.flush()

	def set_machine_scan_now(self, session, idmaquina):
		"""Coloca o horario atual no scanned"""
		foundmachine = session.query(Machine).filter_by(id=idmaquina).first()
		foundmachine.scanned = datetime.datetime
		session.commit()
		session.flush()

	def handler_update_machine_compliance(self, session, idmaquina, boolean):
		foundmachine = session.query(Machine).filter_by(id=idmaquina).first()
		if not foundmachine:
			return False
		foundmachine.compliance = boolean
		return foundmachine

	def handler_update_machine_ip(self, session, idmaquina, ipnovo):
		foundmachine = session.query(Machine).filter_by(id=idmaquina).first()
		if not foundmachine:
			return False
		foundmachine.ip = ipnovo
		session.commit()
		session.flush()
		return foundmachine

	def get_all_safe(self, session):
		"""Retornando a pretty table e depois a lista"""
		foundmachines = session.query(Machine).filter_by(compliance=True)
		return foundmachines

	def get_all_false(self, session):
		"""Retornando a pretty table e depois a lista"""
		foundmachines = session.query(Machine).filter_by(compliance=False)
		return foundmachines




class compliance_handlers(object):
	"""Classe para ajudar no manuseamento da tabela COMPLIANCE_ATTR"""
	def __init__(self):
		self.machineid = ""

	def get_all_compliances(self, session):
		foundcompliances = session.query(Compliance_attr)
		return foundcompliances

	def get_severity_sum(self, session, idmachine):
		foundmachine = session.query(Compliance_attr)\
		.filter_by(machineid=idmachine)
		severitysum = 0
		for machine in foundmachine:
			if machine.particionamento == False:
				severitysum = severitysum + 1
			if machine.timezone == False:
				severitysum = severitysum + 1
			if machine.selinux == False:
				severitysum = severitysum + 2
			if machine.senhagrub == False:
				severitysum = severitysum + 2
			if machine.updated == False:
				severitysum = severitysum + 2
			if machine.ipv6 == False:
				severitysum = severitysum + 1
			if machine.runlevel == False:
				severitysum = severitysum + 2
			if machine.ntp == False:
				severitysum = severitysum + 3
			if machine.kernelntwrk == False:
				severitysum = severitysum + 2
			if machine.servicos_desnecessarios == False:
				severitysum = severitysum + 3
			if machine.servicos_inseguros == False:
				severitysum = severitysum + 3
			if machine.ctrl_alt_del == False:
				severitysum = severitysum + 2
			if machine.compilation_tools == False:
				severitysum = severitysum + 2
			if machine.sulogin == False:
				severitysum = severitysum + 2
			if machine.auditd == False:
				severitysum = severitysum + 2
			if machine.umask_padrao == False:
				severitysum = severitysum + 3
			if machine.root_access == False:
				severitysum = severitysum + 3
			if machine.banner == False:
				severitysum = severitysum + 1
			if machine.ftp_config == False:
				severitysum = severitysum + 3
			if machine.mail_config == False:
				severitysum = severitysum + 2
			if machine.sysstat == False:
				severitysum = severitysum + 2
			if machine.psacct == False:
				severitysum = severitysum + 2
			if machine.log_centralizado == False:
				severitysum = severitysum + 2
			if machine.syslog == False:
				severitysum = severitysum + 3
			if machine.log_permissions == False:
				severitysum = severitysum + 3
			if machine.bash_history_datetime == False:
				severitysum = severitysum + 2
			if machine.last_lastb_lastlog == False:
				severitysum = severitysum + 3
			if machine.core_dumps == False:
				severitysum = severitysum + 2
			if machine.password_complexity == False:
				severitysum = severitysum + 2
			if machine.login_fails == False:
				severitysum = severitysum + 3
			if machine.usuarios_sem_senha == False:
				severitysum = severitysum + 3
			if machine.ssh_root_login == False:
				severitysum = severitysum + 4
			if machine.ssh_privilege_separation == False:
				severitysum = severitysum + 3
			if machine.ssh_version_2 == False:
				severitysum = severitysum + 3
			if machine.port_forwarding == False:
				severitysum = severitysum + 2
			if machine.ssh_strict_mode == False:
				severitysum = severitysum + 2
			if machine.banner_ssh == False:
				severitysum = severitysum + 1
			if machine.ssh_admins == False:
				severitysum = severitysum + 2
			if machine.sftp_disabled == False:
				severitysum = severitysum + 2
			if machine.useraccess_blank_password == False:
				severitysum = severitysum + 3
			if machine.root_uid == False:
				severitysum = severitysum + 4
			if machine.log_system_permissions == False:
				severitysum = severitysum + 3
			if machine.user_exist_blank_password == False:
				severitysum = severitysum + 3
			if machine.nagios == False:
				severitysum = severitysum + 2
			if machine.trauma0 == False:
				severitysum = severitysum + 2
			if machine.agents_config == False:
				severitysum = severitysum + 2
			if machine.sysstat_config == False:
				severitysum = severitysum + 2
		return severitysum





	def get_number_attr_true(self, session, idmachine):
		foundmachine = session.query(Compliance_attr)\
		.filter_by(machineid=idmachine)
		attr_number = 0
		for machine in foundmachine:
			if machine.particionamento == True:
				attr_number = attr_number + 1
			if machine.timezone == True:
				attr_number = attr_number + 1
			if machine.selinux == True:
				attr_number = attr_number + 1
			if machine.senhagrub == True:
				attr_number = attr_number + 1
			if machine.updated == True:
				attr_number = attr_number + 1
			if machine.ipv6 == True:
				attr_number = attr_number + 1
			if machine.runlevel == True:
				attr_number = attr_number + 1
			if machine.ntp == True:
				attr_number = attr_number + 1
			if machine.kernelntwrk == True:
				attr_number = attr_number + 1
			if machine.servicos_desnecessarios == True:
				attr_number = attr_number + 1
			if machine.servicos_inseguros == True:
				attr_number = attr_number + 1
			if machine.ctrl_alt_del == True:
				attr_number = attr_number + 1
			if machine.compilation_tools == True:
				attr_number = attr_number + 1
			if machine.sulogin == True:
				attr_number = attr_number + 1
			if machine.auditd == True:
				attr_number = attr_number + 1
			if machine.umask_padrao == True:
				attr_number = attr_number + 1
			if machine.root_access == True:
				attr_number = attr_number + 1
			if machine.banner == True:
				attr_number = attr_number + 1
			if machine.ftp_config == True:
				attr_number = attr_number + 1
			if machine.mail_config == True:
				attr_number = attr_number + 1
			if machine.sysstat == True:
				attr_number = attr_number + 1
			if machine.psacct == True:
				attr_number = attr_number + 1
			if machine.log_centralizado == True:
				attr_number = attr_number + 1
			if machine.syslog == True:
				attr_number = attr_number + 1
			if machine.log_permissions == True:
				attr_number = attr_number + 1
			if machine.bash_history_datetime == True:
				attr_number = attr_number + 1
			if machine.last_lastb_lastlog == True:
				attr_number = attr_number + 1
			if machine.core_dumps == True:
				attr_number = attr_number + 1
			if machine.password_complexity == True:
				attr_number = attr_number + 1
			if machine.login_fails == True:
				attr_number = attr_number + 1
			if machine.old_passwords == True:
				attr_number = attr_number + 1
			if machine.login_policy == True:
				attr_number = attr_number + 1
			if machine.usuarios_sem_senha == True:
				attr_number = attr_number + 1
			if machine.ssh_root_login == True:
				attr_number = attr_number + 1
			if machine.ssh_privilege_separation == True:
				attr_number = attr_number + 1
			if machine.ssh_version_2 == True:
				attr_number = attr_number + 1
			if machine.port_forwarding == True:
				attr_number = attr_number + 1
			if machine.ssh_strict_mode == True:
				attr_number = attr_number + 1
			if machine.banner_ssh == True:
				attr_number = attr_number + 1
			if machine.ssh_admins == True:
				attr_number = attr_number + 1
			if machine.sftp_disabled == True:
				attr_number = attr_number + 1
			if machine.useraccess_blank_password == True:
				attr_number = attr_number + 1
			if machine.root_uid == True:
				attr_number = attr_number + 1
			if machine.log_system_permissions == True:
				attr_number = attr_number + 1
			if machine.user_exist_blank_password == True:
				attr_number = attr_number + 1
			if machine.nagios == True:
				attr_number = attr_number + 1
			if machine.trauma0 == True:
				attr_number = attr_number + 1
			if machine.agents_config == True:
				attr_number = attr_number + 1
			if machine.sysstat_config == True:
				attr_number = attr_number + 1
			return attr_number



	def get_print(self, session, idmachine):
		"""Retornando print"""
		foundmachine = session.query(Compliance_attr)\
		.filter_by(id=idmachine).first()
		machinedict = dict((col, getattr(foundmachine, col))\
			for col in foundmachine.__table__.columns.keys())
		for key, value in custome_dict.iteritems():
			j = PrettyTable(['Nome compliance', 'Valor'])
			j.add_row([key, value])
			print j
			return j

	def delete(self, session, idmachine):
		foundcompliance = session.query(Compliance_attr).\
		filter_by(id=idmachine).delete()
		session.commit()
		session.flush()

	def get(self, session, idmachine):
		"""Retornando tabela full"""
		foundcompliance = session.query(Compliance_attr)\
		.filter_by(id=idmachine).first()
		if not foundmachine:
			return False
		if foundmachine.id == idmachine:
			return foundcompliance
		else:
			return False

	def update_attr(self, session, idmachine, attr):
		foundmachine = session.query(Compliance_attr)\
		.filter_by(id=idmachine).first()
		if not foundmachine:
			return False
		if foundmachine.id == idmachine:
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
		newcompliance = dbmodel.Compliance_attr(machineid=idmaquina)
		session.add(newcompliance)
		session.commit()
		session.flush()
		return newcompliance

	def update_obs(self, session, idmaquina, newobs):
		compliancefound = session.query(Compliance_attr).\
		filter_by(id=idmaquina).first()
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
