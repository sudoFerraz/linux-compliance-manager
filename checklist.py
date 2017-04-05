import os
#import subprocess
import platform

def timezone():
    out = os.popen('timedatectl | grep \'Time\( zone\|zone\)\'').read()
    guardaresultado("timezone", out)


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
    if out is "":
        return True
    else:
        return False

def grubconfig():
    out = os.popen('rm -rf /var/spool/cron/root-bkp').read()
    if out <> "":
        guardaresultado("GRUB", out)
    out = os.popen('cat /etc/grub.conf | grep -v \'password --md5\' > /tmp/grub.conf').read()
    if out <> "":
        guardaresultado("GRUB", out)
    out = os.popen('sed -i -e \"s/timeout=5/npassword --md5 \$1\$pnpAU1\$z0thj45iKl\/MBf\/XkrtNb1/g\" /tmp/grub.conf').read()
    if out <> "":
        guardaresultado("GRUB", out)
    out = os.popen('rm -rf /etc/grub.conf').read()
    if out <> "":
        guardaresultado("GRUB", out)
    out = os.popen('cp /tmp/grub.conf /etc/grub.conf').read()
    if out == "":
        guardaresultado("GRUB", "OK")



