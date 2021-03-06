import matplotlib
import auxiliary
import dbmodel
import sqlalchemy
import numpy as np
from matplotlib import mlab
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from time import sleep
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})


machinehandler = auxiliary.machine_handler()
ferramenta = auxiliary.ostools()
session = ferramenta.dbconnection(11, 11, 11, 11)
compliancehandler = auxiliary.compliance_handlers()


def Generate_positive_attr():
	attr_machine_list = []
	id_machine_list = []
	foundmachines = machinehandler.get_all_machines(session)
	for machine in foundmachines:
		machine_attr_number = compliancehandler.get_number_attr_true(session, machine.id)
		attr_machine_list.append(machine_attr_number)
		id_machine_list.append(machine.nome)
		attr_machine_list.append(22)
		attr_machine_list.append(52)
		attr_machine_list.append(12)
		attr_machine_list.append(2)
		y = [x for x in range(len(attr_machine_list))]
		plt.bar(y, attr_machine_list)
		plt.xlabel('Number of positive attributes')
		plt.ylabel('Number of machines')
		legenda = mpatches.Patch(color='blue', label='X = MachineID')
		plt.legend(handles=[legenda])
		plt.tight_layout()
		plt.savefig('positive_attr')


def Generate_safe_pie():
	labels = 'Compliance' , 'N-Compliance'
	safecount = 0
	falsecount = 0
	foundmachines = machinehandler.get_all_safe(session)
	for machine in foundmachines:
		safecount = safecount + 1
	foundmachines = machinehandler.get_all_false(session)
	for machine in foundmachines:
		falsecount = falsecount + 1
	machinenumber = falsecount + safecount
	compliancenumber = safecount
	x = falsecount
	y = compliancenumber
	sizes = [y, x]
	explode = (0, 0.1)
	fig1, ax1 = plt.subplots()
	ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f', shadow=True, startangle=90)
	ax1.axis('equal')
	plt.tight_layout()
	plt.savefig('safe_pie')


def Generate_severity_plot():
	labels = 'severity', 'machine'
	severity_machine_list = []
	id_machine_list = []
	foundmachines = machinehandler.get_all_machines(session)
	for machine in foundmachines:
		machine_severity = compliancehandler.get_severity_sum(session, machine.id)
		severity_machine_list.append(machine_severity)
		id_machine_list.append(machine.id)
		y = [x for x in range(len(severity_machine_list))]
		y.append(y[-1]+1)
		plt.scatter(id_machine_list, severity_machine_list, color='r', s=100, marker='X')
		plt.grid(True)
		plt.xticks(y)
		plt.ylabel("Severity degree")
		plt.xlabel("Machine ID")
		plt.tight_layout()
		plt.savefig('severity_plot')


def Generate_pie_severity():
	x,y,z = 0,0,0
	labels = 'Baixo', 'Medio', 'Alto'
	severity_machine_list = []
	id_machine_list = []
	foundmachines = machinehandler.get_all_machines(session)
	for machine in foundmachines:
		machine_severity = compliancehandler.get_severity_sum(session, machine.id)
		severity_machine_list.append(machine_severity)
		#Retirar para producao
		severity_machine_list.append(3)
	for severity in severity_machine_list:
		if severity < 20:
			x = x + 1
		elif severity >= 20 and severity <= 90:
			y = y + 1
		elif severity > 90:
			z = z + 1
	sizes = [x,y,z]
	explode = (0,0,0.1)
	fig1, ax1 = plt.subplots()
	ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
	ax1.axis('equal')
	plt.tight_layout()
	plt.savefig('pie_severity')


os.chdir("/home/rh1n0/projects/linux-compliance-manager/static")
while True:
	Generate_pie_severity()
	Generate_positive_attr()
	Generate_safe_pie()
	Generate_severity_plot()
	print "Sleeping"
	sleep(100)
