"""Funcoes para checagem e modificacoes de atributos da checklist de auditoria\
"""

import os
import platform

#1.1 Como definir o proposito do sistema operacional sem ter contato com o usuario
#1.2 O default de todas as instalacoes ja separa as particoes, portanto nao sei bem o que fazer sobre este item, preciso de ver se existem as particoes /boot, /var e /home somente? 
#1.8 Qual o runlevel adequado? Alguma maquina tera interface grafica? Quais as configuracoes padroes que devo manter?
#1.11 Preciso checar se nenhum dos servicos descritos esta sendo executado em todas as maquinas? Parece muito geral desabilitar todos estes servicos, portanto muito provavelmente sempre dara falha na checagem
#1.16 Preciso checar se o Laus esta instalado? / Checar se o Laus esta sendo executado na inicializacao
#1.20 Como saber o nome dos usuarios que serao enjaulados para poder checar se as configuracoes estao validas
#1.23 OK
#1.25 OK
#1.26 Como descobrir quais são os funcionarios
#1.28 OK
#1.45 Como verificar estes mods
#1.47 - 49  Nome dos plugins que nao acho com o yum



class MachineHandler(object):
	def __init__(self):
		self.machineid = get_machine_mac()
		self.machineid = auxiliary.ostools.get_hash_machine_id(machineid)
		self.dbconnection = auxiliary.dbconnection()

def timezone_check():
    out = os.popen('timedatectl | grep \'Time\( zone\|zone\)\'').read()
    guardaresultado("timezone", out)


def guardaresultado(op, res):
    f = open("resultado.txt", "a")
    f.write(op + "\n")
    f.write(res + "\n\n")
    f.close()

def guardaresultado_db(op, res):
	session = auxiliary.dbconnection(1, 1, 1, 1)

def get_machine_mac():
	out = os.popen('ifconfig | grep \"ether\"').read()
	return out



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


def check_syslog():
	out = os.popen('')

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


def check_syslogseverity():
	out = os.popen('cat /etc/syslog.conf | grep -w \"#kern.*                                                 /dev/console\"').read()
	if out:
		out = os.popen('cat /etc/syslog.conf | grep -w \"*.info;mail.none;authpriv.none;cron.none                /var/log/messages\"').read()
		if out:
			out = os.popen('cat /etc/syslog.conf | grep -w \"authpriv.*                                              /var/log/secure\"').read()
			if out:
				out = os.popen('cat /etc/syslog.conf | grep -w \"mail.*                                                  -/var/log/maillog\"').read()
				if out:
					out = os.popen('cat /etc/syslog.conf | grep -w \"cron.*                                                  /var/log/cron\"').read()
					if out:
						out = os.popen('cat /etc/syslog.conf | grep -w \"*.emerg                                                 *\"').read()
						if out:
							out = os.popen('cat /etc/syslog.conf | grep -w \"uucp,news.crit                                          /var/log/spooler\"').read()
							if out:
								out = os.popen('cat /etc/syslog.cof | grep -w \"local7.*                                                /var/log/boot.log\"').read()
								guardaresultado('SYSLOGSEVERITY', "TRUE")
	else:
		guardaresultado("SYSLOGSEVERITY", "FALSE")


def check_last():
	out = os.popen('last').read()
	if out:
		out = os.popen('lastb').read()
		if out:
			out = os.popen('lastlog').read()
			if out:
				guardaresultado("LAST", "TRUE")
			else:
				guardaresultado("LAST", "TRUE-1")
		else:
			guardaresultado("LAST", "TRUE-2")
	else:
		guardaresultado("LAST", "FALSE")

def check_psacct():
	out = os.popen('rpm -qa | egrep \"psacct\"').read()
	if out:
		out = os.popen('systemctl list-unit-files | grep \"psacct\"').read()
		if out:
			guardaresultado("PSACCT", "TRUE")
		else:
			guardaresultado("PSACCT", "TRUE-1")
	else:
		guardaresultado("PSACCT", "FALSE")



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

def check_log_centralizado():
	out = os.popen('cat /etc/syslog.conf | grep \"REPLICAR SERVIDOR DE LOG\"').read()
	if out:
		guardaresultado("LOG_CENTRALIZADO", "TRUE")
	else:
		guardaresultado("LOG_CENTRALIZADO", "FALSE")

def check_datetime_bash():
	out = os.popen('cat /etc/profile | grep \"CHECK LIST DE SEGURANCA\"').read()
	if out:
		guardaresultado("DATETIME_BASH", "TRUE")
	else:
		guardaresultado("DATETIME_BASH", "FALSE")

def check_coredumps():
	out = os.popen('cat /etc/security/limits.conf | grep \"CHECK LIST DE SEGURANCA\"').read()
	if out:
		guardaresultado("COREDUMPS", "TRUE")
	else:
		guardaresultado("COREDUMPS", "FALSE")

#Fazer para os outros sistemas operacionais
def check_passcomplexity_redhat58():
	out = os.popen('cat /etc/pam.d/system-auth | grep \"password    requisite     pam_cracklib.so try_first_pass retry=3 minlen=8 dcredit=-1 ucredit=-1 ocredit=-1 lcredit=-1\"').read()
	if out:
		guardaresultado("PASSCOMPLEXITY", "TRUE")
	else:
		guardaresultado("PASSCOMPLEXITY", "FALSE")

#Fazer para os outros sistemas operacionais
def check_bruteforce_redhat58():
	out = os.popen('cat /etc/pam.d/system-auth | grep \"auth        required      pam_tally2.so deny=5 onerr=fail unlock_time=1800\"').read()
	if out:
		out = os.popen('cat /etc/pam.d/system-auth |grep \"account     required      pam_tally.so\"').read()
		if out:
			guardaresultado("BRUTEFORCE", "TRUE")
		else:
			guardaresultado("BRUTEFORCE", "TRUE-1")
	else:
		guardaresultado("BRUTEFORCE", "FALSE")

#Fazer para os outros sistemas operacionais
def check_rememberpass_redhat58():
	out = os.popen('cat /etc/pam.d/system-auth | grep \"password    sufficient    pam_unix.so md5 shadow nullok try_first_pass use_authtok remember=15\"').read()
	if out:
		guardaresultado("REMEMBERPASS", "TRUE")
	else:
		guardaresultado("REMEMBERPASS", "FALSE")

def check_loginpolicy():
	out = os.popen('cat /etc/login.defs | grep \"CHECK LIST DE SEGURANCA\"').read()
	if out:
		out = os.popen('cat /etc/default/useradd | grep -w \"INACTIVE=2\"').read()
		if out:
			guardaresultado("LOGINPOLICY", "TRUE")
		else:
			guardaresultado("LOGINPOLICY", "TRUE-1")
	else:
		guardaresultado("LOGINPOLICY", "FALSE")

def check_nopassssh():
	out = os.popen('cat /etc/ssh/ssh_config | grep -w \"PermitEmptyPasswords no\"').read()
	if out:
		guardaresultado("NOPASSSSH", "TRUE")
	else:
		guardaresultado("NOPASSSSH", "FALSE")

def check_sshrootlogin():
	out = os.popen('cat /etc/ssh/ssh_config | grep -w \"PermitRootLogin no\"').read()
	if out:
		guardaresultado("SSHROOTLOGIN", "TRUE")
	else:
		guardaresultado("SSHROOTLOGIN", "FALSE")

def check_privilege_separation():
	out = os.popen('cat /etc/ssh/sshd_config | grep -w \"UsePrivilegeSeparation yes\"').read()
	if out:
		guardaresultado("PRIVILEGESEPARATION", "TRUE")
	else:
		guardaresultado("PRIVILEGESEPARATION", "FALSE")

def check_sshprotocol():
	out = os.popen('cat /etc/ssh/sshd_config | grep -w \"Protocol 2\"').read()
	if out:
		guardaresultado("SSHPROTOCOL", "TRUE")
	else:
		guardaresultado("SSHPROTOCOL", "FALSE")

def check_ssh_portforwarding():
	out = os.popen('cat /etc/ssh/sshd_config | grep -w \"AllowTcpForwarding no\"').read()
	if out:
		out = os.popen('cat /etc/ssh/sshd_config | grep -w \"GatewayPorst no\"').read()
		if out:
			os.popen('cat /etc/ssh/sshd_config | grep -w \"X11Forwarding no\"').read()
			if out:
				guardaresultado("SSHPORTFORWARDING", "TRUE")
			else:
				guardaresultado("SSHPORTFORWARDING", "TRUE-1")
		else:
			guardaresultado("SSHPORTFORWARDING", "TRUE-2")
	else:
		guardaresultado("SSHPORTFORWARDING", "FALSE")

#Ver se realmente e StrictModeS como no documento ou StricMode
def check_ssh_strict_mode():
	out = os.popen('cat /etc/ssh/sshd_config | grep -w \"StricModes yes\"').read()
	if out:
		guardaresultado("SSHSTRICTMODE", "TRUE")
	else:
		guardaresultado("SSHSTRICTMODE", "FALSE")

def check_ssh_bannerconf():
	out = os.popen('cat /etc/ssh/sshd_config | grep -w \"Banner /etc/issue.net\"').read()
	if out:
		guardaresultado("SSHBANNER", "TRUE")
	else:
		guardaresultado("SSHBANNER", "FALSE")


def check_sftp():
	out = os.popen('cat /etc/ssh/sshd_config | grep -w \"#Subsystem   sftp   /usr/libexec/sftp-server\"').read()
	if out:
		guardaresultado("SFTP", "TRUE")
	else:
		guardaresultado("SFTP", "FALSE")

def check_systatconfig():
	out = os.popen('cat /etc/sysconfig/sysstat | grep -w \"HISTORY=30\"').read()
	if out:
		out = os.popen('cat /etc/sysconfig/sysstat | grep -w \"COMPRESSAFTER=2\"').read()
		if out:
			out = os.popen('cat /etc/cron.d/sysstat | grep -w \"*/10 * * * * root /usr/lib64/sa/sa1 1 1\"').read()
			if out:
				out = os.popen('cat /etc/cron.d/sysstat | grep -w \"53 23 * * * root /usr/lib64/sa/sa2 -A\"').read()
				if out:
					guardaresultado("SYSSTATCONFIG", "TRUE")
				else:
					guardaresultado("SYSSTATCONFIG", "TRUE-1")
			else:
				guardaresultado("SYSSTATCONFIG", "TRUE-2")
		else:
			guardaresultado("SYSSTATCONFIG", "TRUE-3")
	else:
		guardaresultado("SYSSTATCONFIG", "FALSE")


def check_blankpass_ssh():
	out = os.popen('cat /etc/ssh/sshd_config | grep -w \"PermitEmptyPasswords no\"').read()
	if out:
		guardaresultado("BLANKSSHPASS", "TRUE")
	else:
		guardaresultado("BLANKSSHPASS", "FALSE")

def check_rootuid():
	out = os.popen('getent passwd | awk -F: \'$3 == \"0\" { print $1 }\' ').read()
	if out == "root":
		guardaresultado("ROOTUID", "TRUE")
	else:
		guardaresultado("ROOTUID", "FALSE")

def check_userwithblankpass():
	out = os.popen('cat /etc/shadow | awk -F: \'$2 == \"!!\" { print $1 }\'').read()
	if out:
		guardaresultado("USERBLANKPASS", "TRUE")
	else:
		guardaresultado("USERBLANKPASS", "FALSE")





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
check_kernel_network()
check_suwheel()
check_sysstat()
check_banner()
check_compilation()
check_coredumps()
check_crtlaltdel()
check_ftp()
check_ipv6()
check_loginpolicy()
check_mailserver()
check_nopassssh()
check_rootuid()
check_selinux()
check_sftp()
check_sshprotocol()
check_sshrootlogin()
check_sulogin()
check_suwheel()
check_sysstat()
check_systatconfig()
check_umask()
check_userwithblankpass()
check_blankpass_ssh()
check_bruteforce_redhat58()
check_datetime_bash()
check_empty_output()
check_kernel_network()
check_log_centralizado()
check_passcomplexity_redhat58()
check_privilege_separation()
check_rememberpass_redhat58()
check_ssh_bannerconf()
check_ssh_portforwarding()
check_ssh_strict_mode()
