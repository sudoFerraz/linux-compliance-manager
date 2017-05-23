"""Modelagem do banco de dados postgreSQL com SQLAlchemy para uso da ferramenta"""

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, LargeBinary
from sqlalchemy import ForeignKey
from sqlalchemy.types import LargeBinary
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from jinja2 import Markup
#from flask.ext.login import UserMixin
#from flask_login import UserMixin
import os
from flask.ext.admin import Admin
from flask_admin.contrib.sqla import ModelView



basedir = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.join(basedir, 'static')
Base = declarative_base()



class Notifications(Base):
    __tablename__ = "Notifications"
    id = Column(Integer, primary_key=True)
    evento = Column(String)
    source = Column(String)
    tempo = Column(DateTime, server_default=func.now())

class Image(Base):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    path = Column(String, unique=True)

    def __repr__(self):
        return self.name

class Graphics(Base):

    __tablename__ = 'Graphics'
    id = Column(Integer, primary_key=True)
    last_updated = Column(DateTime, server_default=func.now())
    name = Column(String)
    image = Column(LargeBinary)
    path = Column(String)

class User(Base):

    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    user = Column(String)
    name = Column(String)
    password = Column(String)
    usertype = Column(String)

    def __repr__(self):
        return "<User(name='%s', password='%s', usertype='%s')>" %(
            self.name, self.password, self.usertype)

class BossHelper(Base):
    __tablename__ = "BossHelper"
    id = Column(Integer, primary_key=True)
    observacoes = Column(String)
    data_desta = Column(DateTime, server_default=func.now())

class Machine(Base):

    __tablename__ = 'Machine'
    id = Column(Integer, primary_key=True)

    ip = Column(String)
    nome = Column(String)
    user = Column(String, server_default='centos')
    password = Column(String, server_default='animal')
    compliance = Column(Boolean)
    scanned = Column(DateTime, server_default=func.now())
    to_scan = Column(Boolean)
    to_apply = Column(Boolean)
    severity = Column(Integer)
    compliance_nro = Column(Integer)

    def __repr__(self):
        return "Machine Nome : %s, Ip : %s " %(self.nome, self.ip)

class Compliance_attr(Base):

    __tablename__ = "Compliance_attr"
    machineid = Column(Integer, ForeignKey('Machine.id'))
    id = Column(Integer, primary_key=True)
    machine = relationship("Machine")
    observacoes = Column(String)
    proposito = Column(String)
    particionamento = Column(Boolean, default=False)
    timezone = Column(Boolean, default=False)
    selinux = Column(Boolean, default=False)
    senhagrub = Column(Boolean, default=False)
    updated = Column(Boolean, default=False)
    ipv6 = Column(Boolean, default=False)
    runlevel = Column(Boolean, default=False)
    ntp = Column(Boolean, default=False)
    kernelntwrk = Column(Boolean, default=False)
    servicos_desnecessarios = Column(Boolean, default=False)
    servicos_inseguros = Column(Boolean, default=False)
    ctrl_alt_del = Column(Boolean, default=False)
    compilation_tools = Column(Boolean, default=False)
    sulogin = Column(Boolean, default=False)
    auditd = Column(Boolean, default=False)
    umask_padrao = Column(Boolean, default=False)
    root_access = Column(Boolean, default=False)
    banner = Column(Boolean, default=False)
    ftp_config = Column(Boolean, default=False)
    mail_config = Column(Boolean, default=False)
    sysstat = Column(Boolean, default=False)
    psacct = Column(Boolean, default=False)
    log_centralizado = Column(Boolean, default=False)
    syslog = Column(Boolean, default=False)
    log_permissions = Column(Boolean, default=False)
    bash_history_datetime = Column(Boolean, default=False)
    last_lastb_lastlog = Column(Boolean, default=False)
    core_dumps = Column(Boolean, default=False)
    password_complexity = Column(Boolean, default=False)
    login_fails = Column(Boolean, default=False)
    old_passwords = Column(Boolean, default=False)
    login_policy = Column(Boolean, default=False)
    usuarios_sem_senha = Column(Boolean, default=False)
    ssh_root_login = Column(Boolean, default=False)
    ssh_privilege_separation = Column(Boolean, default=False)
    ssh_version_2 = Column(Boolean, default=False)
    port_forwarding = Column(Boolean, default=False)
    ssh_strict_mode = Column(Boolean, default=False)
    banner_ssh = Column(Boolean, default=False)
    ssh_admins = Column(Boolean, default=False)
    sftp_disabled = Column(Boolean, default=False)
    useraccess_blank_password = Column(Boolean, default=False)
    root_uid = Column(Boolean, default=False)
    log_system_permissions = Column(Boolean, default=False)
    user_exist_blank_password = Column(Boolean, default=False)
    nagios = Column(Boolean, default=False)
    trauma0 = Column(Boolean, default=False)
    agents_config = Column(Boolean, default=False)
    sysstat_config = Column(Boolean, default=False)

engine = create_engine('postgresql://postgres:postgres@localhost/postgres')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
