import auxiliary
import dbmodel
from time import sleep

ferramenta = auxiliary.ostools()
session = ferramenta.dbconnection(1, 1, 1, 1)
userhandler = auxiliary.user_handlers()
machinehandler = auxiliary.machine_handler()
compliancehandler = auxiliary.compliance_handlers()


def check_compliance_link():
	checker = 0
	foundmachines = machinehandler.get_all_machines(session)
	for machine in foundmachines:
		foundcompliances = compliancehandler.get_all_compliances(session)
		for compliance in foundcompliances:
			if machine.id == compliance.machineid:
				checker = 1
			else:
				pass
		if checker == 0:
			compliancehandler.cria(session, machine.id)
		elif checker == 1:
			pass


while True:
	check_compliance_link()
	sleep(100)


