import os
#
#import subprocess
import platform

def timezone_check():
    out = os.popen('timedatectl | grep \'Time\( zone\|zone\)\'').read()
    guardaresultado("timezone", out)


def guardaresultado(op, res):
    f = open("resultado.txt", "a")
    f.write(op + "\n")
    f.write(res + "\n\n")
    f.close()


def update_check():
    out = os.popen('cat /etc/yum.conf | grep \'exclude(=kernel| =kernel| = kernel)\'').read()
    out = check_empty_output(out)
    guardaresultado("UPDATE", out)

def update():
#checar se o asterisco fica no comando
    out = os.popen('yum -y update').read()
    if out == "":
        out = "OK"
    out = os.popen('echo exclude=kernel* >> /etc/yum.conf').read()
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

def check_selinux():
    out = os.popen('cat /etc/selinux/config').read()
    string = "SELINUX=enforcing"
    if string in out:
        guardaresultado("SELINUX", "TRUE")
    else:
        guardaresultado("SELINUX", "TRUE")

def selinux():
    out = os.popen('echo \'SELINUX=enforcing\' >> /etc/selinux/config').read()
    if out == "":
        out = "OK"
    guardaresultado("selinux", out)

def check_empty_output(out):
    if out == "":
        return "OK"
    if out is None:
        return "OK"
    if out == '':
        return "OK"
    else:
        return "ERRO"

def grub_config():
    out = os.popen('rm -rf /var/spool/cron/root-bkp').read()
    if out <> "":
        guardaresultado("GRUB", out)
        return False
    out = os.popen('cat /etc/grub.conf | grep -v \'password --md5\' > /tmp/grub.conf').read()
    if out <> "":
        guardaresultado("GRUB", out)
        return False
    out = os.popen('sed -i -e \"s/timeout=5/npassword --md5 \$1\$pnpAU1\$z0thj45iKl\/MBf\/XkrtNb1/g\" /tmp/grub.conf').read()
    if out <> "":
        guardaresultado("GRUB", out)
        return False
    out = os.popen('rm -rf /etc/grub.conf').read()
    if out <> "":
        guardaresultado("GRUB", out)
        return False
    out = os.popen('cp /tmp/grub.conf /etc/grub.conf').read()
    if out == "":
        guardaresultado("GRUB", "OK")

def check_ipv6():
    out = os.popen('cat /etc/sysctl.conf | grep \"ipv6\"').read()
    string = "net.ipv6.conf.default.disable_ipv6=1"
    if string in out:
        string = "net.ipv6.conf.all.disable_ipv6=1"
        if string in out:
            guardaresultado("IPV6", "TRUE")
        else:
            guardaresultado("IPV6", "TRUE-1")
    else:
        guardaresultado("IPV6", "FALSE")

def disable_ipv6():
    out = os.popen('sysctl -w net.ipv6.conf.default.disable_ipv6=1').read()
    out = os.popen('sysctl -w net.ipv6.conf.all.disable_ipv6=1').read()
    out = os.popen('echo net.ipv6.conf.all.disable_ipv6=1 >> /etc/sysctl.conf').read()
    out = os.popen('echo net.ipv6.conf.default.disable_ipv6=1 >> /etc/sysctl.conf').read()
    out = os.popen('echo net.ipv6.conf.lo.disable_ipv6=1 >> /etc/sysctl.conf').read()
    out = check_empty_output(out)
    guardaresultado("IPV6", out)

def crontab_check():
    out = os.popen('cat /var/spool/cron/root').read()
    string = "######### Check List de Seguranca #################\n0,15,30,45 * * * * /usr/sbin/ntpdate -u 10.32.9.230\n0,15,30,45 * * * * /sbin/hwclock --systohc\n###################################################"
    if string in out:
        guardaresultado("CRONTAB", "TRUE")
    else:
        guardaresultado("CRONTAB", "TRUE")

def crontab_config():
    out = os.popen('yum -y install ntpdate').read()
    out = os.popen('rm -rf /var/spool/cron/root-bkp').read()
    out = os.popen('/usr/sbin/ntpdate -u 10.32.9.230 && /sbin/hwclock --systohc').read()
    out = os.popen('cat /var/spool/cron/root | grep -v ntpdate | grep -v hwclock | grep -v \
\'Check List\' | grep -v \'################\' > /var/spool/cron/root-bkp').read()
    out = os.popen('rm -rf /var/spool/cron/root').read()
    out = os.popen('echo \"######### Check List de Seguranca #################\n0,15,30,45 * * * * /usr/sbin/ntpdate -u 10.32.9.230\n0,15,30,45 * * * * /sbin/hwclock --systohc\n###################################################\" >> /var/spool/cron/root-bkp').read()
    out = os.popen('cp /var/spool/cron/root-bkp /var/spool/cron/root').read()
    print out
    out = check_empty_output(out)
    guardaresultado("CRONTAB", out)

check_ipv6()
