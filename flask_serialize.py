"""serializing data for the flask endpoint"""
import dbmodel
import auxiliary
#import checklist
import apiserver
import jsonify
from flask import jsonify

machinehandler = auxiliary.machine_handler()
userhandler = auxiliary.user_handlers()
ferramenta = auxiliary.ostools()
compliancehandler = auxiliary.compliance_handlers()


session = ferramenta.dbconnection(11, 11, 11, 11)

def return_machine_serialized(machineid):
	foundmachine = machinehandler.get_machine_by_id(machineid, session)
	if foundmachine:
		return foundmachine
	else:
		return False

def return_allmachines():
	foundmachines = machinehandler.get_all_machines(session)
	return foundmachines