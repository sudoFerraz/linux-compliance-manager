"""Modelagem do banco de dados postgreSQL com SQLAlchemy para uso da ferramenta"""

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
Base = declarative_base()

class User(Base):

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    usertype = Column(String)

    def __repr__(self):
        return "<User(name='%s', password='%s', usertype='%s')>" %(
            self.name, self.password, self.usertype)

class Machine(Base):

    __tablename__ = 'machines'
    id = Column(Integer, primary_key=True)
    ip = Column(String)
    nome = Column(String)
    compliance = Column(Boolean)
    scanned = Column(Boolean)

class Compliance_attr(Base):

    __tablename__ = "compliance_attr"
    id = Column(Integer, primary_key=True,ForeignKey('machines.id'))
    observacoes = Column(String)
    proposito = Column(String)
    particionamento = Column(Boolean)
    timezone = Column(Boolean)
    selinux = Column(Boolean)
    senhagrub = Column(Boolean)
    updated = Column(Boolean)
    ipv6 = Column(Boolean)
    runlevel = Column(Boolean)
    ntp = Column(Boolean)
    kernelntwrk = Column(Boolean)
    servicos_desnecessarios = Column(Boolean)
    servicos_inseguros = Column(Boolean)
    ctrl_alt_del = Column(Boolean)
    compilation_tools = Column(Boolean)
    sulogin = Column(Boolean)
    auditd = Column(Boolean)
    umask_padrao = Column(Boolean)
    root_access = Column(Boolean)
    banner = Column(Boolean)
    ftp_config = Column(Boolean)
    mail_config = Column(Boolean)
    sysstat = Column(Boolean)
    psacct = Column(Boolean)
    log_centralizado = Column(Boolean)
    syslog = Column(Boolean)
    log_permissions = Column(Boolean)
    bash_history_datetime = Column(Boolean)
    last_lastb_lastlog = Column(Boolean)
    core_dumps = Column(Boolean)
    password_complexity = Column(Boolean)
    login_fails = Column(Boolean)
    old_passwords = Column(Boolean)
    login_policy = Column(Boolean)
    usuarios_sem_senha = Column(Boolean)
    ssh_root_login = Column(Boolean)
    ssh_privilege_separation = Column(Boolean)
    ssh_version_2 = Column(Boolean)
    port_forwarding = Column(Boolean)
    ssh_strict_mode = Column(Boolean)
    banner_ssh = Column(Boolean)
    ssh_admins = Column(Boolean)
    sftp_disabled = Column(Boolean)
    useraccess_blank_password = Column(Boolean)
    root_uid = Column(Boolean)
    log_system_permissions = Column(Boolean)
    user_exist_blank_password = Column(Boolean)
    nagios = Column(Boolean)
    trauma0 = Column(Boolean)
    agents_config = Column(Boolean)
    sysstat_config = Column(Boolean)

