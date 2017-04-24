import auxiliary
import os
from fabric.api import *


machinehandler = auxiliary.machine_handler()
userhandler = auxiliary.user_handlers()
ferramenta = auxiliary.ostools()
compliancehandler = auxiliary.compliance_handlers()


session = ferramenta.dbconnection(11, 11, 11, 11)

def fabric_checklist_scan(session, ip):
	with settings(host_string="10.51.202.72", user = "centos"):
		output = run('uname -a')
def fabric_checklist_apply(session, ip):
	pass

while True:
	foundmachines = machinehandler.get_all_machines(session)
	for machine in foundmachines:
		if machine.compliance == True:
			pass
		elif machine.to_scan == True:
			fabric_checklist_host(session, machine.ip)
		elif machine.to_apply == True:
			fabric_checklist_apply(session, machine.ip)
	sleep(100)


if __name__ == '__main__':
	fabric_checklist_scan(2, 2)

