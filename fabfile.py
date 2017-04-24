from fabric.api import task, run, local, put
import os
import platform
import argparse

listofitens = []

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
def checklist():
    output = run('timedatectl | grep \'Time\( zone|zone\)\'')
    #PEGAR QUAL O TIMEZONE CERTO PARA AS MAQUINAS
    if output == "TIMEZONECERTO":
        pass
    else:
        listofitens.append("timezone")
    output = run('cat /etc/yum.conf | grep \'exclude(=kernel| =kernel| = kernel)\'')
    if output:
        output = run('yum check-update')
        if "All up to date" in output:
            pass
        else:
            listofitens.append("update_check")
    else:
        listofitens.append("update_check")
    output = run('cat /etc/selinux/config')
    if "SELINUX=enforcing" in output:
        pass
    else:
        listofitens.append("SELINUX")
    out = run('cat /etc/syslog.conf | grep -w \"#kern.*                                                 /dev/console\"')
    if out:
        if out:
        out = run('cat /etc/syslog.conf | grep -w \"*.info;mail.none;authpriv.none;cron.none                /var/log/messages\"')
        if out:
            out = run('cat /etc/syslog.conf | grep -w \"authpriv.*                                              /var/log/secure\"')
            if out:
                out = run('cat /etc/syslog.conf | grep -w \"mail.*                                                  -/var/log/maillog\"')
                if out:
                    out = run('cat /etc/syslog.conf | grep -w \"cron.*                                                  /var/log/cron\"')
                    if out:
                        out = run('cat /etc/syslog.conf | grep -w \"*.emerg                                                 *\"')
                        if out:
                            out = run('cat /etc/syslog.conf | grep -w \"uucp,news.crit                                          /var/log/spooler\"')
                            if out:
                                out = run('cat /etc/syslog.conf | grep -w \"local7.*                                                /var/log/boot.log\"')
                                if out:
                                    pass
    else:
        listofitens.append("syslogseverity")
        else:
            listofitens.append("syslogseverity")
            else:
                listofitens.append("syslogseverity")
                else:
                    listofitens.append("syslogseverity")
                    else:
                        listofitens.append("syslogseverity")
                        else:
                            listofitens.append("syslogseverity")
                            else:
                                listofitens.append("syslogseverity")
                                else:
                                    listofitens.append("syslogseverity")
    output = run('last')
    if output:
        output = run('lastb')
        if output:
            output = run('lastlog')
            if output:
                pass
    else:
        listofitens.append("check_last")
        else:
            listofitens.append("check_last")
            else:
                listofitens.append("check_last")
    output = run('rpm -qa | egrep \"psacct\"')
    if output:
        output = run('systemctl list-unit-files | grep \"psacct\"')
        if output:
            pass
    else:
        listofitens.append("psacct")
        else:
            listofitens.append("psacct")
    output = run('rm -rf /var/spool/cron/root-bkp')
    if output == "":
        output = run('cat  /etc/grub.conf | grep -v \'password --md5\' > /tmp/grub.conf')
        if output == "":
            output = run('sed -i -e \"s/timeout=5/npassword --md5 \$1\$pnpAU1\$z0thj45iKl\/MBf\/XkrtNb1/g\" /tmp/grub.conf')
            if output == "":
                output = run('rm -rf /etc/grub.conf')
                if output == "":
                    output = run('cp /tmp/grub.conf /etc/grub.conf')
                    if output == "":
                        pass
                    else:
                        listofitens.append("grub_config")
                else:
                    listofitens.append("grub_config")
            else:
                listofitens.append("grub_config")
        else:
            listofitens.append("grub_config")
    else:
        listofitens.append("grub_config")
    output = run('cat /etc/sysctl.conf | grep \"ipv6\"')
    if "net.ipv6.conf.all.disable_ipv6=1" in output:
        if "net.ipv6.conf.default.disable_ipv6=1" in output:
            pass
        else:
            listofitens.append("check_ipv6")
    else:
        listofitens.append("check_ipv6")
    output = run('cat /var/spool/cron/root')
    if "######### Check List de Seguranca #################\n0,15,30,45 * * * * /usr/sbin/ntpdate -u 10.32.9.230\n0,15,30,45 * * * * /sbin/hwclock --systohc\n###################################################" in output:
        pass
    else:
        listofitens.append("crontab_check")
    output = run('cat /etc/inittab | grep \"#ca:12345:ctrlaltdel\"')
    if output:
        pass
    else:
        listofitens.append("ctrlaltdel")
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
            listofitens.append("umask")
    else:
        listofitens.append("umask")
    output = run('cat /etc/syslog.conf | grep \"REPLICAR SERVIDOR DE LOG\"')
    if output:
        pass
    else:
        listofitens.append("log_centralizado")
    output = run('cat /etc/profile | grep \"CHECK LIST DE SEGURANCA\"')
    if output:
        pass
    else:
        listofitens.append("datetime_bash")
    output = run('cat /etc/security/limits.conf | grep \"CHECK LIST DE SEGURANCA\"')
    if output:
        pass
    else:
        listofitens.append("coredumps")
    output = run('cat /etc/pam.d/system-auth | grep \"password    requisite     pam_cracklib.so try_first_pass retry=3 minlen=8 dcredit=-1 ucredit=-1 ocredit=-1 lcredit=-1\"')
    if output:
        pass
    else:
        listofitens.append("passcomplexity")
    output = run('cat /etc/pam.d/system-auth | grep \"auth        required      pam_tally2.so deny=5 onerr=fail unlock_time=1800\"')
    if output:
        output = run('cat /etc/pam.d/system-auth |grep \"account     required      pam_tally.so\"')
        if output:
            pass
        else:
            listofitens.append("bruteforce")
    else:
        listofitens.append("bruteforce")
    output = run('cat /etc/pam.d/system-auth | grep \"password    sufficient    pam_unix.so md5 shadow nullok try_first_pass use_authtok remember=15\"')
    if output:
        pass
    else:
        listofitens.append("rememberpass")
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
        listofitens.append("nopassssh")
    output = run('cat /etc/ssh/ssh_config | grep -w \"PermitRootLogin no\"')
    if output:
        pass
    else:
        listofitens.append("sshrootlogin")
    output = run('cat /etc/ssh/sshd_config | grep -w \"UsePrivilegeSeparation yes\"')
    if output:
        pass
    else:
        listofitens.append("privilege_separation")
    output = run('cat /etc/ssh/sshd_config | grep -w \"Protocol 2\"')
    if output:
        pass
    else:
        listofitens.append("ssh_protocol")
    output = run('cat /etc/ssh/sshd_config | grep =w \"AllowTcpForwarding no\"')
    if output:
        output = run('cat /etc/ssh/sshd_config | grep -w \"GatewayPorts no\"')
        if output:
            output = run('cat /etc/ssh/sshd_config | grep -w \"X11Forwarding no\"')
            if output:
                pass
            else:
                listofitens.append("ssh_portforwarding")
        else:
            listofitens.append("ssh_portforwarding")
    else:
        listofitens.append("ssh_portforwarding")
    output = run('cat /etc/ssh/sshd_config | grep =w \"StricModes yes\"')
    if output:
        pass
    else:
        listofitens.append("ssh_stric_mode")
    output = run('cat /etc/ssh/sshd_config | grep =w \"Banner /etc/issue.net\"')
    if output:
        pass
    else:
        listofitens.append("ssh_bannerconf")
    output = run('cat /etc/ssh/sshd_config | grep -w \"#Subsystem   sftp   /usr/libexec/sftp-server\"')
    if output:
        pass
    else:
        listofitens.append("sftp")
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
                    listofitens.append("sysstatconfig")
            else:
                listofitens.append("sysstatconfig")
        else:
            listofitens.append("sysstatconfig")
    else:
        listofitens.append("sysstatconfig")
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
                                                        listofitens.append("systempermissions")
                                                else:
                                                    listofitens.append("systempermissions")
                                            else:
                                                listofitens.append("systempermissions")
                                        else:
                                            listofitens.append("systempermissions")
                                    else:
                                        listofitens.append("systempermissions")
                                else:
                                    listofitens.append("systempermissions")
                            else:
                                listofitens.append("systempermissions")
                        else:
                            listofitens.append("systempermissions")
                    else:
                        listofitens.append("systempermissions")
                else:
                    listofitens.append("systempermissions")
            else:
                listofitens.append("systempermissions")
        else:
            listofitens.append("systempermissions")
    else:
        listofitens.append("systempermissions")




    output = run('')
    output = run('')
    output = run('')
    output = run('')
    output = run('')






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

