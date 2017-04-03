import sys
import sqlalchemy
import os
import paramiko
import hashlib
from sqlalchemy import create_engine
from sqlalchemy import sessionmaker
from pexpect import pxssh


dbip = 1.1.1.1
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
	('postgresql://banco:role@localhost/banco')
	Session = sessionmaker()
	Session.configure(bind=engine)
	session = Session()
	return session

def handle_cria_user(session):
	pass


def notificate(offense, user):
	pass


def investigation(path, wordlist, user):
	for dirpath, dirnames, filenames in os.walk(path):
		print 'Caminho atual' + dirpath
		print 'Diretorios' + str(dirnames)
		print 'Arquivos' + str(filenames)
		if dirname in wordlist for dirname in dirnames:
			notificate(dirname, user)
		if filename in wordlist for filename in filenames:
			notificate(filename, user)

def get_user():
	user = os.environ.get('USER')
	return user







#os.chdir('')
#os.makedirs('')
#os.listdir()