#!/bin/bash

# TESTE 
echo "Configurando o securitty"

cp /etc/securetty /etc/securetty-bkp
> /etc/securetty

echo "console
vc/1
vc/2
vc/3
vc/4
vc/5
vc/6
vc/7
vc/8
vc/9
vc/10
vc/11
tty1
tty2
tty3
tty4
tty5
tty6
tty7
tty8
tty9
tty10
tty11 " >> /etc/securetty

mkdir /root/.ssh/
> /root/.ssh/authorized_keys
echo "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA8KTC19ikg8W02KZHPohnWOBmGzQGXrFlzDzQJFvwZrlzBwAlMmOxTzEffDNEFChBho1o477BVSkObkzsA1NibBg9rikBxnh6nUMUWSvPxhyLocsdzEHyjomkasORS0QP9/4qs4LxPHeaV4wwUOc3O77CN4M3j/gFS0PuEyMPkYCPJPCDfXory989XDxdvjqm422hwIMGEujkB6w7LscLQjy9RFX4M5rwDU1m9cVMcxev8ysHwqRo+ZKhi1vaL/ykcrh8KzkZ6huD7aHyb7pWofxaefhI8zd05ITrXKnEr/2F6rlIiQxnBjG2PYaeIb0bc/H4RS7LCMSv7DVope9goQ== root@rsyslogprd
ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAIEArgwfoHfyyELt+WWlIYYZB3bXnXPGi7f6hGB8+er1XvHCaD8VgwGPOcj15q0E0go/5fZB+19SedeSz6IpQ6aUlsj756Vjl65aGmzKM2q8zuG9RZ6NF+cNX2ZmQiOmPr1aUsXRgY648YHLkA0dN92MrSBkm5z8PSNXXmZI5ETQPZk= root@usrv07
" >> /root/.ssh/authorized_keys

echo "Configurando o usuarios"

usermod -p '$1$mYEH1G3d$TrgYorY8V89OlKo/nMYgD/' root
userdel -rf opsocsi
useradd opsocsi
usermod -p '$1$d4XdEN60$el51DS4UtjgFCl/1rzHxv0' opsocsi
usermod -p '$1$do7G6mDm$HwbghaEwlvrgTB69vS.I1/' nagios

USUARIOSDEL=" andreo sthefano andrev euclides roseval marlley gislainea leandros franklin osmar jarbasf romulof josermp luiz wagner paulohac matias thiago danielf rendricson paulo paulovictor tinoco jeisonm andrevinicius opsocti opsoctbc rodrigojm thiagoa rodrigogs rodrigoroca ikaror ikaro davidfr volneif heitorfta polianaal bryanct diogojp jodsomwo fabiohs ericrr thiagoa_datacom gregorio gregorios henriquegz rewry nivaldoor spolti enio jonatan camilapizzi rodrigoc claudysonj luizhr fernandob nivaldo vanderz luizgustavo viniciusb thiagoas andrelj enoque renatodm " 
for del in $USUARIOSDEL; do 
        userdel -rf ${del} 
done 

cd /home
useradd testezim
USUARIOSADD=" andreo fillipe sthefano andrev pedrov vasconcelos fabriocios euclides roseval leandros osmar claudiaa gabrielandre matheusau jarbasf josermp luiz gferraz wagner  rendricson "
for cria in $USUARIOSADD; do 
        cp -r /home/testezim /home/$cria
		chown -R $cria:root $cria
done 
userdel -rf testezim

echo "Configurando servicos"
SERVICO_DIS=" acpid arptables_jf atd autofs avahi-daemon bluetooth cpuspeed cups cups-config-daemon gpm haldaemon ip6tables iptables irdairqbalance isdn krb5-telnet mdmonitor messagebus microcode_ctl netfs nfs nfslock pcgssd rsync pcmcia portmap readahead readahead_early readahead_later rpcgssd rpcidmapd smartd wdaemon xfs ypbind"
for DISABLEDSERVICO in $SERVICO_DIS; do
chkconfig --level 12345 $DISABLEDSERVICO off
done

echo "Configurando o access"
cp /etc/security/access.conf /etc/security/access.conf-bkp
> /etc/security/access.conf
echo "
- : root : ALL EXCEPT 10.11.148.53 rsyslogprd 10.32.14.13 usrv07 tty1 172.23.4.1 172.23.16.1 127.0.0.1 LOCAL
+ : ALL : cron crond " >>  /etc/security/access.conf

echo "Configurando o grub"
rm -rf /tmp/grub.conf
cat /etc/grub.conf  | grep -v 'password --md5' > /tmp/grub.conf
sed -i -e "s/timeout=5/timeout=5\npassword --md5 \$1\$pnpAU1\$z0thj45iKl\/MBf\/XkrtNb1/g" /tmp/grub.conf
rm -rf /etc/grub.conf
cp /tmp/grub.conf /etc/grub.conf

echo "Configurando a crontab"
rm -rf /var/spool/cron/root-bkp
/usr/sbin/ntpdate -u 10.32.9.230 && /sbin/hwclock --systohc
cat /var/spool/cron/root  | grep -v ntpdate | grep -v hwclock | grep -v 'Check List' | grep -v '################' > /var/spool/cron/root-bkp
rm -rf /var/spool/cron/root
echo "
######### Check List de Seguranca #################
0,15,30,45 * * * * /usr/sbin/ntpdate -u 10.32.9.230
0,15,30,45 * * * * /sbin/hwclock --systohc
###################################################" >> /var/spool/cron/root-bkp
cp /var/spool/cron/root-bkp /var/spool/cron/root

echo "Configurando os grupos"
groupdel admapp
groupdel suplinux
groupdel especialistas
groupdel implantacao
groupdel cliente
groupdel terceiros
groupdel admlinux
groupdel monitoramento
groupdel rootmembers

cp /etc/group /tmp/group
cat /etc/group | grep -v wheel > /tmp/group-bkp
cp --reply=yes /tmp/group-bkp /etc/group 
cp /tmp/group-bkp /etc/group 
echo "wheel:x:10:root,andreo,andrev,pedrov,fabricios,vasconcelos,gferraz,fillipe,sthefano,opsocsi" >> /etc/group

echo "Configurando o Sudo"
cp /etc/sudoers /etc/sudoers-bkp
cat /etc/sudoers | grep -v rootmembers | grep -v algaroperacao | grep -v admlinux | grep -v monitoramento | grep -v admapp | grep -v '###'  > /tmp/sudoers
rm -rf /etc/sudoers
cp /tmp/sudoers /etc/sudoers

echo "
##########################  PERMITE EXECUTAR TODOS OS COMANDOS EXCETO OS ABAIXO EXPECIFICADOS ########################
%algaroperacao ALL=(ALL) NOPASSWD:   ALL
%algarso  ALL=(ALL) NOPASSWD:   ALL
%algarapp ALL=(ALL) NOPASSWD:   ALL
opsocsi  ALL=(ALL) NOPASSWD:   ALL
##########################  PERMITE EXECUTAR TODOS OS COMANDOS EXCETO OS ABAIXO EXPECIFICADOS ########################
" >> /etc/sudoers

echo "Configurando o History"
cat /etc/profile | grep -v HISTTIMEFORMAT | grep -v TMOUT | grep -v 'HISTTIMEFORMAT TMOUT' | grep -v '####' | grep -v '## CHECK' > /tmp/profile
cp --reply=yes /tmp/profile /etc/profile
cp /tmp/profile /etc/profile
echo "
######### CHECK-LIST DE SEGURANCA ##########
HISTTIMEFORMAT=\"%c -> \"
TMOUT=1800
export HISTTIMEFORMAT TMOUT
umask 077
############################################
" >> /etc/profile
source /etc/profile 

echo "Configurando o SSH"
cp /etc/ssh/sshd_config /etc/ssh/sshd_config-bkp
sed -i -e 's/^PermitRootLogin .*$/PermitRootLogin yes/' /etc/ssh/sshd_config
sed -i -e 's/^AuthorizedKeysFile .*$/AuthorizedKeysFile   .ssh\/authorized_keys/' /etc/ssh/sshd_config
sed -i -e '/^Banner/ d' /etc/ssh/sshd_config
sed -i -e 's/^StrictModes yes/StrictModes yes\nBanner \/etc\/issue.net /g' /etc/ssh/sshd_config

cat /etc/ssh/sshd_config | grep -q -e '^PermitRootLogin .*$'
if [ $? -eq 1 ]; then
      echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
fi                                      
cat /etc/ssh/sshd_config | grep -q -e '^AuthorizedKeysFile .*$'
if [ $? -eq 1 ]; then
      echo "AuthorizedKeysFile   .ssh/authorized_keys" >> /etc/ssh/sshd_config
fi
sed -i "s/AllowUsers/#AllowUsers/g" /etc/ssh/sshd_config 

/etc/init.d/sshd restart

echo "Configurado PAM"
cat /etc/pam.d/sshd | grep -v pam_access >> /tmp/pam_d_sshd
sed -i -e "s/pam_nologin.so/pam_nologin.so\naccount    required     pam_access.so/g" /tmp/pam_d_sshd
cp --reply=yes /tmp/pam_d_sshd /etc/pam.d/sshd
cp /tmp/pam_d_sshd /etc/pam.d/sshd

echo "Configurando o hosts"

IPMAQ=`ifconfig | grep "inet addr" | grep 10 | awk '{ print $2 }' | cut -d ':' -f 2`
NOMEMAQ=`hostname`
echo "$IPMAQ         $NOMEMAQ        $NOMEMAQ.network.ctbc" >> /etc/hosts
echo "127.0.0.1      localhost.localdomain localhost" >> /etc/hosts
echo "" >> /etc/hosts
echo "
############### SERVIDOR DE GRIDCTL ##################################
10.11.133.51 gridctlivc.network.ctbc gridctlivc
######################################################################

############### RELAY ################################################
10.11.133.229    imss-cm01  imss-cm01.network.ctbc
######################################################################

############### SERVIDOR DE ACESSO ###################################
10.11.148.53    rsyslogprd
######################################################################

############## SERVIDOR DE SYSLOG ####################################
10.32.15.62     loghost
######################################################################

######### SERVIDOR DE REPOSITORIO ####################################
10.11.132.149   lxmrepo01 lxmrepo01.network.ctbc
10.11.132.150 spacewalk01 spacewalk01.network.ctbc
######################################################################

############### SERVIDOR DE CONTROL M ################################
10.11.151.9     ctm64prd01
######################################################################"  >> /etc/hosts

/usr/sbin/ntpdate -u 10.32.9.230
date 

echo "Permissoes Gerais"
chmod 400 /var/spool/cron 
chmod 400 /etc/shadow 
chmod 400 /etc/crontab
chmod 600 /etc/securetty
chmod 640 /etc/syslog.conf
chmod 640 /etc/sysctl.conf
chmod 640 /var/log/wtmp
chmod 640 /var/log/lastlog
chmod 664 /etc/security/limits.conf
chmod 664 /etc/csh.login
chmod 644 /etc/group 
chmod 644 /etc/passwd 
service psacct restart
chkconfig psacct on
service sysstat restart
chkconfig auditd on
service auditd restart
chkconfig sysstat on
chkconfig sendmail on
touch /var/log/secure
touch /var/log/btmp
chmod 600 /var/log/secure

ARQUITETURA=`uname -i`
ARQZ="s390x"
if [ "$ARQUITETURA" == "$ARQZ" ]; then
chkconfig rsyslog on
/etc/init.d/rsyslog restart
echo "Restartado RSYSLOG"
else
chkconfig syslog on
/etc/init.d/syslog start 
echo "Restartado SYSLOG"
fi


echo "Banner Configuracao"
> /etc/motd
> /etc/issue.net
> /etc/issue

cat >> /etc/issue.net << EOF
************ Permitido o uso somente para pessoas autorizadas **************
        Individuos que utilizarem este equipamento sem
        autorizacao, ou em operacoes que excedam o nivel de
        autorizacao permitido, estarao sujeitos a penalizacoes
        e rigores da legislacao aplicavel.

        Qualquer um que utilize este sistema concorda previamente
        com o monitoramento e esta ciente que se atividades ilicitas
        e/ou criminais forem reveladas a partir deste, podera ser
        objeto de processo judicial e/ou criminal.
****************************************************************************
EOF

cat >> /etc/issue << EOF
************ Permitido o uso somente para pessoas autorizadas **************
        Individuos que utilizarem este equipamento sem
        autorizacao, ou em operacoes que excedam o nivel de
        autorizacao permitido, estarao sujeitos a penalizacoes
        e rigores da legislacao aplicavel.

        Qualquer um que utilize este sistema concorda previamente
        com o monitoramento e esta ciente que se atividades ilicitas
        e/ou criminais forem reveladas a partir deste, podera ser
        objeto de processo judicial e/ou criminal.
****************************************************************************
EOF

cat >> /etc/motd << EOF
************ Permitido o uso somente para pessoas autorizadas **************
        Individuos que utilizarem este equipamento sem
        autorizacao, ou em operacoes que excedam o nivel de
        autorizacao permitido, estarao sujeitos a penalizacoes
        e rigores da legislacao aplicavel.

        Qualquer um que utilize este sistema concorda previamente
        com o monitoramento e esta ciente que se atividades ilicitas
        e/ou criminais forem reveladas a partir deste, podera ser
        objeto de processo judicial e/ou criminal.
****************************************************************************
EOF
chmod 0440 /etc/sudoers

chage -m 99999 -M 99999 -E never ora11g
chage -m 99999 -M 99999 -E never ora10g
chage -m 99999 -M 99999 -E never producao
chage -m 99999 -M 99999 -E never jboss 
chage -m 99999 -M 99999 -E never ora12c
chage -m 99999 -M 99999 -E never nagios
chage -m 99999 -M 99999 -E never controlm

grpck 
sleep 3
grpck 
sleep 3
grpck 
sleep 3
grpck 
sleep 3
grpck 
sleep 3
