import auxiliary
import os
import datetime
from time import sleep

machinehandler = auxiliary.machine_handler()
userhandler = auxiliary.user_handlers()
ferramenta = auxiliary.ostools()
compliancehandler = auxiliary.compliance_handlers()

#user = "centos"
#password = "animal"

session = ferramenta.dbconnection(11, 11, 11, 11)

notifications = []

def fabric_checklist_scan(session, ip, user, password):
	out = os.popen('sudo fab -H'+user+'@'+ip+' -p '+password+' checklist:\''+ip+'\'').read()
def fabric_checklist_apply(session, ip):
	pass

def notifications_refresh(evento, source, tempo):
	if evento == "scan":
		notifications.append("Escaneando maquina " + source)
	elif evento == "erro":
		notifications.append("Erro durante o procedimento " + source)
	elif evento == "graphics":
		notifications.append("Gerando grafico " + source)
	elif evento == "new":
		notifications.append("Nova maquina no destino " + source)
	elif evento == "":
		pass

def alimenta_template():
	session.



while True:
	foundmachines = machinehandler.get_all_machines(session)
	for machine in foundmachines:
		if machine.compliance == True:
			pass
		elif machine.to_scan == True:
			fabric_checklist_scan(session, machine.ip, machine.user, machine.password)
			machine.scanned = datetime.datetime.now()
			session.commit()
			session.flush()
		elif machine.to_apply == True:
			fabric_checklist_apply(session, machine.ip)
	sleep(10)



