"""Funcoes para checagem e modificacoes de atributos da checklist de auditoria\
"""

import os
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
    if out:
        out = os.popen('yum check-update').read()
        #Olhar como realmente e a resposta do centos para mudar a string
        string = "All up to date"
        if string in out:
            guardaresultado("UPDATED", "TRUE")
        else:
            guardaresultado("UPDATED", "TRUE-1")
    else:
        guardaresultado("UPDATED", "FALSE")

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

def config_selinux():
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

def grub_check():
    out = os.popen("cat /etc/grub.conf").read()
    string = ""
    if string in out:
        guardaresultado("GRUB", "TRUE")
    else:
        guardaresultado("GRUB", "TRUE")

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
    string = "net.ipv6.conf.all.disable_ipv6=1"
    if string in out:
        string = "net.ipv6.conf.default.disable_ipv6=1"
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

def check_crtlaltdel():
    out = os.popen('cat /etc/inittab | grep \"#ca:12345:ctrlaltdel\"').read()
    if out:
        guardaresultado("CTRLALTDEL", "TRUE")
    else:
        guardaresultado("CTRLALTDEL", "FALSE")

def check_compilation():
    out = os.popen('rpm -qa | egrep \"^gcc|java|bin86|dev86|cc|flex|bison|nasm\"').read()
    if out:
        guardaresultado("COMPILADORES", "FALSE")
    else:
        guardaresultado("COMPILADORES", "TRUE")

def check_sulogin():
    out = os.popen('cat /etc/inittab | grep \"~~:S:wait:/sbin/sulogin\"').read()
    if out:
        guardaresultado("SULOGIN", "TRUE")
    else:
        guardaresultado("SULOGIN", "FALSE")

def check_umask():
    out = os.popen('cat /etc/profile | grep \"CHECK LIST\"').read()
    if out:
        out = os.popen('cat /etc/csh.login | grep \"CHECK LIST\"').read()
        if out:
            guardaresultado("UMASK", "TRUE")
        else:
            guardaresultado("UMASK", "TRUE-1")
    else:
        guardaresultado("UMASK", "FALSE")

def check_banner():
    out = os.popen('cat /etc/issue | grep \"Permitido o uso somente\"').read()
    if out:
        out = os.popen('cat /etc/issue.net | grep \"Permitido o uso somente\"').read()
        if out:
            out = os.popen('cat /etc/motd | grep \"Permitido o uso somente\"').read()
            if out:
                guardaresultado("BANNER", "TRUE")
            else:
                guardaresultado("BANNER", "TRUE-1")
        else:
            guardaresultado("BANNER", "TRUE-2")
    else:
        guardaresultado("BANNER", "FALSE")

def check_ftp():
    pass

def check_mailserver():
    out = os.popen('cat /etc/mail/sendmail.mc').read()
    string = "DAEMON_OPTIONS(`Port=smtp,Addr=127.0.0.1, Name=MTA')dnl"
    if string in out:
        out = os.popen('cat /etc/mail/sendmail.cf').read()
        if out:
            guardaresultado("MAILSERVER", "TRUE")
        else:
            guardaresultado("MAILSERVER", "TRUE-1")
    else:
        guardaresultado("MAILSERVER", "FALSE")

def check_sysstat():
    out = os.popen('yum list installed sysstat').read()
    if out == True:
        guardaresultado("SYSSTAT", "TRUE")
    else:
        guardaresultado("SYSSTAT", "FALSE")



def check_suwheel():
    out = os.popen('cat /etc/pam.d/su')
    string = "auth required pam wheel.so use uid"
    if string in out:
        guardaresultado("SUWHEEL", "TRUE")
    else:
        guardaresultado("SUWHEEL", "FALSE")


def check_kernel_network():
    out = os.popen('cat /etc/sysctl.d/100-backlog.conf | grep \"Check List\"')
    if out:
        out = os.popen('cat /etc/sysctl.conf | grep \"Check List\"').read()
        if out:
            guardaresultado("KERNEL_NET", "TRUE")
    else:
        guardaresultado("KERNEL_NET", "FALSE")




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
