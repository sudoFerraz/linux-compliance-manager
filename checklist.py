import os
import subprocess

def timezone():
    out = os.popen('timedatectl | grep \'Time\( zone\|zone\)\'').read()
    guardaresultado("timezone", out)
    print out


def guardaresultado(op, res):
    f = open("resultado.txt", "w")
    f.write(op)
    f.write(res)
    f.close()


def update():
    proc = subprocess.Popen(["yum", "-y", "update"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.comunicate()
    print "program output:", out

timezone()
