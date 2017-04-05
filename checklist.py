import os
import subprocess
import platform

def timezone():
    out = os.popen('timedatectl | grep \'Time\( zone\|zone\)\'').read()
    guardaresultado("timezone", out)
    print out


def guardaresultado(op, res):
    f = open("resultado.txt", "a")
    f.write(op + "\n")
    f.write(res + "\n\n")
    f.close()


def update():
    out = os.popen('yum -y update').read()
    if out == "":
        out = "OK"
    guardaresultado("update", out)

def gatherinfo():
    out = []
    out.append(platform.uname())
    out.append(platform.platform())
    out.append(platform.system())
    out = str(out)
    guardaresultado("SO", out)

def selinux():
    out = os.popen('echo \'SELINUX=enforcing\' >> /etc/selinux/config').read()
    if out == "":
        out = "OK"
    guardaresultado("selinux", out)
    

gatherinfo()
timezone()
update()
selinux()
