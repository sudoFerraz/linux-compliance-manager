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

def check_empty_output(out):
    if out is None:
        return True
    else:
        return False
    
def grubconfig():
    out = os.popen('rm -rf /var/spool/cron/root-bkp').read()
    if out:
        out = "ERROR"
        guardaresultado("GRUB", out)
    
    


gatherinfo()
timezone()
update()
selinux()
