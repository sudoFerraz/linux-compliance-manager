# linux-compliance-manager
A tool for managing machines in the same network that are in compliance with the policies
#

A documentação da modelagem dos dados será feita após os testes iniciais com o código

O banco usado está sendo PostgreSQL utilizando-se de ORM - Object Relational Mapping com SQLAlchemy e um drive do psycopg2
3 entidades principais.


#Usuários do sistema - User
Máquinas - Machine
Lista de atributos de segurança de uma máquina - Compliance_attr
#


Lista de severidade para atributos de compliance

Particionamento = 1
Timezone = 1
SELinux = 2
SenhaGrub = 2
Updated = 2
IPV6 = 1
RunLevel = 2
NTP = 3
KernelNtwrk = 2
Servicos Desnecessarios = 3
Servicos Inseguros = 3
Ctrl Alt Del = 2
Compilation Tools = 2
SuLogin = 2
AuditD = 2
Umask Padrao = 3
Root Acess = 3
Banner = 1
Ftp Config = 3
Mail Config = 2
Sysstat = 2
psacct = 2
Log Centralizado = 2
SysLog = 3
Log Permissions = 3
Bash History Datetime = 2
Last Lastb Lastlog = 3
Core Dumps = 2
Password Complexity = 2
Login Fails = 3
Usuarios sem senha = 3
SSH root Login = 4
SSh privilege separation = 3
SSh version 2 = 3
Port Forwarding = 2
SSH Strict Mode = 2
Banner SSH = 1
SSH Admins = 2
SFTP Disabled = 2
UserAccess Blank Password = 3
Root UID = 4
Log System Permissions = 3
User Exist Blank Password = 3
Nagios = 2
Trauma0 = 2
Agents config = 2
Sysstat Config = 2
