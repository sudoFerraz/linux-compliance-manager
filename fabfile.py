from fabric.api import task, run, local, put, settings, abort
import os
import platform
import argparse
import auxiliary
from dbmodel import Machine, Compliance_attr

listofitens = []
ferramenta = auxiliary.ostools()
machinehandler = auxiliary.machine_handler()
compliancehandler = auxiliary.compliance_handlers()
session = ferramenta.dbconnection(11, 11, 11, 11)



@task()
def update_all(reboot_host='false'):
    """
    Yum update a host
    :param reboot_host:
        (false|no|true|yes)
        reboot the host if its true
    """
    run("yum update -y")
    if reboot_host == 'true' or reboot_host == 'yes':
        run("reboot")

@task()
def hello():
    print("hello")
    put('/home/rh1n0/projects/linux-compliance-manager/checklist.py', '~/')
    output = run('uname -a')
    if output == "doido":
        print("doido")
    else:
        print("loco")
        print output

@task()
def checklist(ipmaquina):
    with settings(warn_only=True):
        output = run('timedatectl | egrep \'Time( zone|zone)\'')
    #PEGAR QUAL O TIMEZONE CERTO PARA AS MAQUINAS
        if output:
            pass
        else:
            listofitens.append("timezone")
        print listofitens
        output = run('cat /etc/yum.conf | egrep \'exclude(=kernel| =kernel| = kernel)\'')
        if output:
            output = run('yum check-update')
            if "All up to date" in output:
                pass
            else:
                listofitens.append("updated")
        else:
            listofitens.append("updated")
        output = run('cat /etc/selinux/config')
        if "SELINUX=enforcing" in output:
            pass
        else:
            listofitens.append("selinux")
        out = run('cat /etc/syslog.conf | egrep -w \"#kern.*                                                 /dev/console\"')
        if out:
            if out:
                out = run('cat /etc/syslog.conf | egrep -w \"*.info;mail.none;authpriv.none;cron.none                /var/log/messages\"')
                if out:
                    out = run('cat /etc/syslog.conf | egrep -w \"authpriv.*                                              /var/log/secure\"')
                    if out:
                        out = run('cat /etc/syslog.conf | egrep -w \"mail.*                                                  -/var/log/maillog\"')
                        if out:
                            out = run('cat /etc/syslog.conf | egrep -w \"cron.*                                                  /var/log/cron\"')
                            if out:
                                out = run('cat /etc/syslog.conf | egrep -w \"*.emerg                                                 *\"')
                                if out:
                                    out = run('cat /etc/syslog.conf | egrep -w \"uucp,news.crit                                          /var/log/spooler\"')
                                    if out:
                                        out = run('cat /etc/syslog.conf | egrep -w \"local7.*                                                /var/log/boot.log\"')
                                        if output:
                                            pass
                                        else:
                                            listofitens.append("syslog")
                                    else:
                                        listofitens.append("syslog")
                                else:
                                    listofitens.append("syslog")
                            else:
                                listofitens.append("syslog")
                        else:
                            listofitens.append("syslog")
                    else:
                        listofitens.append("syslog")
                else:
                    listofitens.append("syslog")
            else:
                listofitens.append("syslog")
        else:
            listofitens.append("syslog")
        output = run('last')
        if output:
            output = run('lastb')
            if output:
                output = run('lastlog')
                if output:
                    pass
                else:
                    listofitens.append("last_lastb_lastlog")
            else:
                listofitens.append("last_lastb_lastlog")
        else:
            listofitens.append("last_lastb_lastlog")
        output = run('rpm -qa | egrep \"psacct\"')
        if output:
            output = run('systemctl list-unit-files | egrep \"psacct\"')
            if output:
                pass
            else:
                listofitens.append("psacct")
        else:
            listofitens.append("psacct")
        output = run('rm -rf /var/spool/cron/root-bkp')
        if output == "":
            output = run('cat  /etc/grub.conf | egrep -v \'password --md5\' > /tmp/grub.conf')
            if output == "":
                output = run('sed -i -e \"s/timeout=5/npassword --md5 \$1\$pnpAU1\$z0thj45iKl\/MBf\/XkrtNb1/g\" /tmp/grub.conf')
                if output == "":
                    output = run('rm -rf /etc/grub.conf')
                    if output == "":
                        output = run('cp /tmp/grub.conf /etc/grub.conf')
                        if output == "":
                            pass
                        else:
                            listofitens.append("senhagrub")
                    else:
                        listofitens.append("senhagrub")
                else:
                    listofitens.append("senhagrub")
            else:
                listofitens.append("senhagrub")
        else:
            listofitens.append("senhagrub")
        output = run('cat /etc/sysctl.conf | grep \"ipv6\"')
        if "net.ipv6.conf.all.disable_ipv6=1" in output:
            if "net.ipv6.conf.default.disable_ipv6=1" in output:
                pass
            else:
                listofitens.append("ipv6")
        else:
            listofitens.append("ipv6")
        output = run('cat /var/spool/cron/root')
        if "######### Check List de Seguranca #################\n0,15,30,45 * * * * /usr/sbin/ntpdate -u 10.32.9.230\n0,15,30,45 * * * * /sbin/hwclock --systohc\n###################################################" in output:
            pass
        else:
            listofitens.append("ntp")
        output = run('cat /etc/inittab | grep \"#ca:12345:ctrlaltdel\"')
        if output:
            pass
        else:
            listofitens.append("ctrl_alt_del")
        output = run('rpm -qa | egrep \"^gcc|java|bin86|dev86|cc|flex|bison|nasm\"')
        if output:
            listofitens.append("compiladores")
        else:
            pass
        output = run('cat /etc/inittab | grep \"~~:S:wait:/sbin/sulogin\"')
        if output:
            pass
        else:
            listofitens.append("sulogin")
        output = run('cat /etc/profile | grep \"CHECK LIST\"')
        if output:
            output = run('cat /etc/csh.login | grep \"CHECK LIST\"')
            if output:
                pass
            else:
                listofitens.append("umask_padrao")
        else:
            listofitens.append("umask_padrao")
        output = run('cat /etc/syslog.conf | grep \"REPLICAR SERVIDOR DE LOG\"')
        if output:
            pass
        else:
            listofitens.append("log_centralizado")
        output = run('cat /etc/profile | grep \"CHECK LIST DE SEGURANCA\"')
        if output:
            pass
        else:
            listofitens.append("bash_history_datetime")
        output = run('cat /etc/security/limits.conf | grep \"CHECK LIST DE SEGURANCA\"')
        if output:
            pass
        else:
            listofitens.append("core_dumps")
        output = run('cat /etc/pam.d/system-auth | grep \"password    requisite     pam_cracklib.so try_first_pass retry=3 minlen=8 dcredit=-1 ucredit=-1 ocredit=-1 lcredit=-1\"')
        if output:
            pass
        else:
            listofitens.append("password_complexity")
        output = run('cat /etc/pam.d/system-auth | grep \"auth        required      pam_tally2.so deny=5 onerr=fail unlock_time=1800\"')
        if output:
            output = run('cat /etc/pam.d/system-auth |grep \"account     required      pam_tally.so\"')
            if output:
                pass
            else:
                listofitens.append("login_fails")
        else:
            listofitens.append("login_fails")
        output = run('cat /etc/pam.d/system-auth | grep \"password    sufficient    pam_unix.so md5 shadow nullok try_first_pass use_authtok remember=15\"')
        if output:
            pass
        else:
            listofitens.append("old_passwords")
        output = run('cat /etc/login.defs | grep \"CHECK LIST DE SEGURANCA\"')
        if output:
            output = run('cat /etc/default/useradd | grep -w \"INACTIVE=2\"')
            if output:
                pass
            else:
                listofitens.append("login_policy")
        else:
            listofitens.append("login_policy")
        output = run('cat /etc/ssh/ssh_config | grep -w \"PermitEmptyPasswords no\"')
        if output:
            pass
        else:
            listofitens.append("usuarios_sem_senha")
        output = run('cat /etc/ssh/ssh_config | grep -w \"PermitRootLogin no\"')
        if output:
            pass
        else:
            listofitens.append("ssh_root_login")
        output = run('cat /etc/ssh/sshd_config | grep -w \"UsePrivilegeSeparation yes\"')
        if output:
            pass
        else:
            listofitens.append("ssh_privilege_separation")
        output = run('cat /etc/ssh/sshd_config | grep -w \"Protocol 2\"')
        if output:
            pass
        else:
            listofitens.append("ssh_version_2")
        output = run('cat /etc/ssh/sshd_config | grep =w \"AllowTcpForwarding no\"')
        if output:
            output = run('cat /etc/ssh/sshd_config | grep -w \"GatewayPorts no\"')
            if output:
                output = run('cat /etc/ssh/sshd_config | grep -w \"X11Forwarding no\"')
                if output:
                    pass
                else:
                    listofitens.append("port_forwarding")
            else:
                listofitens.append("port_forwarding")
        else:
            listofitens.append("port_forwarding")
        output = run('cat /etc/ssh/sshd_config | grep =w \"StricModes yes\"')
        if output:
            pass
        else:
            listofitens.append("ssh_strict_mode")
        output = run('cat /etc/ssh/sshd_config | grep =w \"Banner /etc/issue.net\"')
        if output:
            pass
        else:
            listofitens.append("banner_ssh")
        output = run('cat /etc/ssh/sshd_config | grep -w \"#Subsystem   sftp   /usr/libexec/sftp-server\"')
        if output:
            pass
        else:
            listofitens.append("sftp_disabled")
        output = run('cat /etc/sysconfig/sysstat | grep -w \"HISTORY=30\"')
        if output:
            output = run('cat /etc/sysconfig/sysstat | grep -w \"COMPRESSAFTER=2\"')
            if output:
                output = run('cat /etc/cron.d/sysstat | grep -w \"*/10 * * * * root /usr/lib64/sa/sa1 1 1\"')
                if output:
                    output = run('cat /etc/cron.d/sysstat | grep -w \"53 23 * * * root /usr/lib64/sa/sa2 -A\"')
                    if output:
                        pass
                    else:
                        listofitens.append("sysstat_config")
                else:
                    listofitens.append("sysstat_config")
            else:
                listofitens.append("sysstat_config")
        else:
            listofitens.append("sysstat_config")
        out = run('stat -c \"%a\" /var/spool/cron')
        if out == "400":
            out = run('stat -c \"%a\" /etch/shadow')
            if out == "400":
                out = run('stat -c \"%a\" /etc/crontab')
                if out == "400":
                    out = run('stat -c \"%a\" /etc/securetty')
                    if out == "600":
                        out = run('stat -c \"%a\" /etc/syslog.conf')
                        if out == "640":
                            out = run('stat -c \"%a\" /etc/rsyslog.conf')
                            if out == "640":
                                out = run('stat -c \"%a\" /etc/sysctl.conf')
                                if out == "640":
                                    out = run('stat -c \"%a\" /var/log/wtmp')
                                    if out == "640":
                                        out = run('stat -c \"%a\" /var/log/lastlog')
                                        if out == "640":
                                            out = run('stat -c \"%a\" /etc/security/limits.conf')
                                            if out == "644":
                                                out = run('stat -c \"%a\" /etc/csh.logn')
                                                if out == "644":
                                                    out = run('stat -c \"%a\" /etc/group')
                                                    if out == "644":
                                                        out = run('stat -c \"%a\" /etc/passwd')
                                                        if out == "644":
                                                            pass
                                                        else:
                                                            listofitens.append("log_system_permissions")
                                                    else:
                                                        listofitens.append("log_system_permissions")
                                                else:
                                                    listofitens.append("log_system_permissions")
                                            else:
                                                listofitens.append("log_system_permissions")
                                        else:
                                            listofitens.append("log_system_permissions")
                                    else:
                                        listofitens.append("log_system_permissions")
                                else:
                                    listofitens.append("log_system_permissions")
                            else:
                                listofitens.append("log_system_permissions")
                        else:
                            listofitens.append("log_system_permissions")
                    else:
                        listofitens.append("log_system_permissions")
                else:
                    listofitens.append("log_system_permissions")
            else:
                listofitens.append("log_system_permissions")
        else:
            listofitens.append("log_system_permissions")
        output = run('cat /etc/ssh/sshd_config | grep -w \"PermitEmpyPasswords no\"')
        if output:
            pass
        else:
            listofitens.append("useraccess_blank_password")
        output = run('getent passwd | awk -F: \'$3 == \"0\" { print $1 }\' ')
        if output == "root":
            pass
        else:
            listofitens.append("root_uid")
        output = run('cat /etc/shadow | awk -F: \'$2 == \"!!\" { print $1 }\'')
        if output:
            pass
        else:
            listofitens.append("user_exist_blank_password")
        output = run('systemctl get-default')
        if output == "multi-user.target":
            pass
        else:
            listofitens.append("runlevel")
        output = run('cat /etc/issue | grep \"Permitido o uso somente')
        if output:
            output = run('cat /etc/issue.net | grep \"Permitido o uso somente\"')
            if output:
                output = run('cat /etc/motd | grep \"Permitido o uso somente\"')
                if output:
                    pass
                else:
                    listofitens.append("banner")
            else:
                listofitens.append("banner")
        else:
            listofitens.append("banner")
        output = run('cat /etc/mail/sendmail.mc')
        if "DAEMON_OPTIONS('Port=smtp,Addr=127.0.0.1, Name=MTA')dnl" in output:
            output = run('cat /etc/mail/sendmail.cf')
            if output:
                pass
            else:
                listofitens.append("mail_config")
        else:
            listofitens.append("mail_config")
        output = run('yum list installed sysstat')
        if output == True:
            pass
        else:
            listofitens.append("sysstat")
        output = run('cat /etc/pam.d/su')
        if "auth required pam wheel.so use uid" in output:
            pass
        else:
            listofitens.append("root_access")
        output = run('cat /etc/sysctl.d/100-backlog.conf | grep \"Check List\"')
        if output:
            output = run('cat /etc/sysctl.conf | grep \"Check List\"')
            if output:
                pass
            else:
                listofitens.append("kernelntwrk")
        else:
            listofitens.append("kernelntwrk")
        #FAZER O UPDATE NA TABELA
        print listofitens
        foundmachine = session.query(Machine).filter_by(ip=ipmaquina).first()
        foundcompliance = session.query(Compliance_attr).filter_by(machineid=foundmachine.id).first()
        for item in listofitens:
            if item == "particionamento":
                foundcompliance.particionamento = False
            elif "particionamento" not in listofitens:
                foundcompliance.particionamento = True
            if item == "timezone":
                foundcompliance.timezone = False
            elif "timezone" not in listofitens:
                foundcompliance.timezone = True
            if item == "selinux":
                foundcompliance.selinux = False
            elif "selinux" not in listofitens:
                foundcompliance.selinux = True
            if item == "senhagrub":
                foundcompliance.senhagrub = False
            elif "senhagrub" not in listofitens:
                foundcompliance.senhagrub = True
            if item == "updated":
                foundcompliance.senhagrub = False
            elif "updated" not in listofitens:
                foundcompliance.updated = True
            if item == "ipv6":
                foundcompliance.ipv6 = False
            elif "ipv6" not in listofitens:
                foundcompliance.ipv6 = True
            if item == "runlevel":
                foundcompliance.runlevel = False
            elif "runlevel" not in listofitens:
                foundcompliance.runlevel = True
            if item == "ntp":
                foundcompliance.ntp = False
            elif "ntp" not in listofitens:
                foundcompliance.ntp = True
            if item == "kernelntwrk":
                foundcompliance.kernelnetwrk = False
            elif "kernelnetwrk" not in listofitens:
                foundcompliance.kernelnetwrk = True
            if item == "servicos_desnecessarios":
                foundcompliance.servicos_desnecessarios = False
            elif "servicos_desnecessarios" not in listofitens:
                foundcompliance.servicos_desnecessarios = True
            if item == "servicos_inseguros":
                foundcompliance.servicos_inseguros = False
            elif "servicos_inseguros" not in listofitens:
                foundcompliance.servicos_desnecessarios = True
            if item == "ctrl_alt_del":
                foundcompliance.ctrl_alt_del = False
            elif "ctrl_alt_del" not in listofitens:
                foundcompliance.ctrl_alt_del = True
            if item == "compilation_tools":
                foundcompliance.compilation_tools = False
            elif "compilation_tools" not in listofitens:
                foundcompliance.compilation_tools =  True
            if item == "sulogin":
                foundcompliance.sulogin = False
            elif "sulogin" not in listofitens:
                foundcompliance.sulogin = True
            if item == "auditd":
                foundcompliance.auditd = False
            elif "auditd" not in listofitens:
                foundcompliance.auditd = True
            if item == "umask_padrao":
                foundcompliance.umask_padrao = False
            elif "umask_padrao" not in listofitens:
                foundcompliance.umask_padrao = True
            if item == "root_access":
                foundcompliance.root_access = False
            elif "root_access" not in listofitens:
                foundcompliance.root_access = True
            if item == "banner":
                foundcompliance.banner = False
            elif "banner" not in listofitens:
                foundcompliance.banner = True
            if item == "ftp_config":
                foundcompliance.ftp_config = False
            elif "ftp_config" not in listofitens:
                foundcompliance.ftp_config = True
            if item == "mail_config":
                foundcompliance.mail_config = False
            elif "mail_config" not in listofitens:
                foundcompliance.mail_config = True
            if item == "sysstat":
                foundcompliance.sysstat = False
            elif "sysstat" not in listofitens:
                foundcompliance.sysstat = True
            if item == "psacct":
                foundcompliance.psacct = False
            elif "psacct" not in listofitens:
                foundcompliance.psacct = True
            if item == "log_centralizado":
                foundcompliance.log_centralizado = False
            elif "log_centralizado" not in listofitens:
                foundcompliance.log_centralizado = True
            if item == "syslog":
                foundcompliance.syslog = False
            elif "syslog" not in listofitens:
                foundcompliance.syslog = True
            if item == "log_permissions":
                foundcompliance.log_permissions = False
            elif "log_permissions" not in listofitens:
                foundcompliance.log_permissions = True
            if item == "bash_history_datetime":
                foundcompliance.bash_history_datetime = False
            elif "bash_history_datetime" not in listofitens:
                foundcompliance.bash_history_datetime = True
            if item == "last_lastb_lastlog":
                foundcompliance.last_lastb_lastlog = False
            elif "last_lastb_lastlog" not in listofitens:
                foundcompliance.last_lastb_lastlog = True
            if item == "core_dumps":
                foundcompliance.core_dumps = False
            elif "core_dumps" not in listofitens:
                foundcompliance.core_dumps = True
            if item == "password_complexity":
                foundcompliance.password_complexity = False
            elif "password_complexity" not in listofitens:
                foundcompliance.password_complexity = True
            if item == "login_fails":
                foundcompliance.login_fails = False
            elif "login_fails" not in listofitens:
                foundcompliance.login_fails = True
            if item == "old_password":
                foundcompliance.old_password = False
            elif "old_password" not in listofitens:
                foundcompliance.old_password = True
            if item == "login_policy":
                foundcompliance.login_policy = False
            elif "login_policy" not in listofitens:
                foundcompliance.login_policy = True
            if item == "usuarios_sem_senha":
                foundcompliance.usuarios_sem_senha = False
            elif "usuarios_sem_senha" not in listofitens:
                foundcompliance.usuarios_sem_senha = True
            if item == "ssh_root_login":
                foundcompliance.ssh_root_login = False
            elif "ssh_root_login" not in listofitens:
                foundcompliance.ssh_root_login = True
            if item == "ssh_privilege_separation":
                foundcompliance.ssh_privilege_separation = False
            elif "ssh_privilege_separation" not in listofitens:
                foundcompliance.ssh_privilege_separation = True
            if item == "ssh_version_2":
                foundcompliance.ssh_version_2 = False
            elif "ssh_version_2" not in listofitens:
                foundcompliance.ssh_version_2 = True
            if item == "port_forwarding":
                foundcompliance.port_forwarding = False
            elif "port_forwarding" not in listofitens:
                foundcompliance.port_forwarding = True
            if item == "ssh_strict_mode":
                foundcompliance.ssh_strict_mode = False
            elif "ssh_strict_mode" not in listofitens:
                foundcompliance.ssh_stric_mode = True
            if item == "banner_ssh":
                foundcompliance.banner_ssh = False
            elif "banner_ssh" not in listofitens:
                foundcompliance.banner_ssh = True
            if item == "ssh_admins":
                foundcompliance.ssh_admins = False
            elif "ssh_admins" not in listofitens:
                foundcompliance.ssh_admins = True
            if item == "sftp_disabled":
                foundcompliance.sftp_disabled = False
            elif "sftp_disabled" not in listofitens:
                foundcompliance.sftp_disabled = True
            if item == "useraccess_blank_password":
                foundcompliance.useraccess_blank_password = False
            elif "useraccess_blank_password" not in listofitens:
                foundcompliance.useraccess_blank_password = True
            if item == "root_uid":
                foundcompliance.root_uid = False
            elif "root_uid" not in listofitens:
                foundcompliance.root_uid = True
            if item == "log_system_permissions":
                foundcompliance.log_system_permissions = False
            elif "log_system_permissions" not in listofitens:
                foundcompliance.log_system_permissions = True
            if item == "user_exist_blank_password":
                foundcompliance.user_exist_blank_password = False
            elif "user_exist_blank_password" not in listofitens:
                foundcompliance.user_exist_blank_password = True
            if item == "nagios":
                foundcompliance.nagios =  False
            elif "nagios" not in listofitens:
                foundcompliance.nagios = True
            if item == "trauma0":
                foundcompliance.trauma0 = False
            elif "trauma0" not in listofitens:
                foundcompliance.trauma0 = True
            if item == "agents_config":
                foundcompliance.agents_config = False
            elif "agents_config" not in listofitens:
                foundcompliance.agents_config = True
            if item == "sysstat_config":
                foundcompliance.sysstat_config = False
            elif "sysstat_config" not in listofitens:
                foundcompliance.sysstat_config = True
        if len(listofitens) == 0:
            foundmachine.compliance == True
        session.commit()
        session.flush()





@task()
def delete_checklist():
    print("deletando...")
    output = run('sudo rm -r checklist.py')
    print output

@task()
def fab_scan():
    print("scanning...")
    output = run('python checklist.py')
    print output

