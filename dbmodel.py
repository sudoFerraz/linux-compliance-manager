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
    id = Column(Integer, ForeignKey('machines.id'))
    # pegar atributos do compliance com o boss

class
