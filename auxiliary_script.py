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
		print machine.nome
		print machine.id
		foundcompliances = compliancehandler.get_all_compliances(session)
		for compliance in foundcompliances:
			print compliance.machineid
			if machine.id == compliance.machineid:
				checker = 1
			else:
				pass
		if checker == 0:
			compliancehandler.cria(session, machine.id)
		elif checker == 1:
			checker = 0


while True:
	session.flush()
	check_compliance_link()
	sleep(100)


