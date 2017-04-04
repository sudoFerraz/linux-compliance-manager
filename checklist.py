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
    f.write(res + "\n")
    f.close()


def update():
    proc = subprocess.Popen(["yum", "-y", "update"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.comunicate()
    print "program output:", out

def gatherinfo():
    out = []
    out.append(platform.uname())
    out.append(platform.platform())
    out.append(platform.system())
    out = str(out)
    guardaresultado("SO", out)
    print out

timezone()
gatherinfo()
