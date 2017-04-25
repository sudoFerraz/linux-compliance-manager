import auxiliary
import os
import datetime
from time import sleep

machinehandler = auxiliary.machine_handler()
userhandler = auxiliary.user_handlers()
ferramenta = auxiliary.ostools()
compliancehandler = auxiliary.compliance_handlers()

user = "centos"
password = "animal"

session = ferramenta.dbconnection(11, 11, 11, 11)

def fabric_checklist_scan(session, ip):
	out = os.popen('sudo fab -H'+user+'@'+ip+' -p '+password+' checklist:\''+ip+'\'').read()
def fabric_checklist_apply(session, ip):
	pass

while True:
	foundmachines = machinehandler.get_all_machines(session)
	for machine in foundmachines:
		if machine.compliance == True:
			pass
		elif machine.to_scan == True:
			fabric_checklist_scan(session, machine.ip)
			machine.scanned = datetime.datetime.now()
			session.commit()
			session.flush()
		elif machine.to_apply == True:
			fabric_checklist_apply(session, machine.ip)
	sleep(10)



