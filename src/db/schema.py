
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP
from pgvector.sqlalchemy import Vector

Base = declarative_base()
class TableFactory:
    def __init__(self):
        self.alito = Alito
        self.barret = Barrett
        self.breyer = Breyer
        self.ginsburg = Ginsburg
        self.gorsuch = Gorsuch
        self.jackson = Jackson
        self.kagan = Kagan
        self.kavanaugh = Kavanaugh
        self.kennedy = Kennedy
        self.roberts = Roberts
        self.scalia = Scalia
        self.sotomayor = Sotomayor
        self.thomas = Thomas
        self.court_opinion = CourtOpinion
    
    def get_table(self, table_name:str = 'court_opinion'):
        return getattr(self, table_name.lower(), None)


class CourtOpinion(Base):
    __tablename__ = 'court_opinion'
    id = Column(Integer, primary_key=True, autoincrement=True)
    embedding = Column(Vector)
    opinion = Column(String)
    created_at = Column(TIMESTAMP)

class Alito(Base):
    __tablename__ = 'alito'
    id = Column(Integer, primary_key=True, autoincrement=True)
    embedding = Column(Vector)
    opinion = Column(String)
    created_at = Column(TIMESTAMP)

class Barrett(Base):
    __tablename__ = 'barrett'
    id = Column(Integer, primary_key=True, autoincrement=True)
    embedding = Column(Vector)
    opinion = Column(String)
    created_at = Column(TIMESTAMP)

class Breyer(Base):
    __tablename__ = 'breyer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    embedding = Column(Vector)
    opinion = Column(String)
    created_at = Column(TIMESTAMP)

class Ginsburg(Base):
    __tablename__ = 'ginsburg'
    id = Column(Integer, primary_key=True, autoincrement=True)
    embedding = Column(Vector)
    opinion = Column(String)
    created_at = Column(TIMESTAMP)

class Gorsuch(Base):
    __tablename__ = 'gorsuch'
    id = Column(Integer, primary_key=True, autoincrement=True)
    embedding = Column(Vector)
    opinion = Column(String)
    created_at = Column(TIMESTAMP)

class Jackson(Base):
    __tablename__ = 'jackson'
    id = Column(Integer, primary_key=True, autoincrement=True)
    embedding = Column(Vector)
    opinion = Column(String)
    created_at = Column(TIMESTAMP)

class Kagan(Base):
    __tablename__ = 'kagan'
    id = Column(Integer, primary_key=True, autoincrement=True)
    embedding = Column(Vector)
    opinion = Column(String)
    created_at = Column(TIMESTAMP)

class Kavanaugh(Base):
    __tablename__ = 'kavanaugh'
    id = Column(Integer, primary_key=True, autoincrement=True)
    embedding = Column(Vector)
    opinion = Column(String)
    created_at = Column(TIMESTAMP)

class Kennedy(Base):
    __tablename__ = 'kennedy'
    id = Column(Integer, primary_key=True, autoincrement=True)
    embedding = Column(Vector)
    opinion = Column(String)
    created_at = Column(TIMESTAMP)

class Roberts(Base):
    __tablename__ = 'roberts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    embedding = Column(Vector)
    opinion = Column(String)
    created_at = Column(TIMESTAMP)

class Scalia(Base):
    __tablename__ = 'scalia'
    id = Column(Integer, primary_key=True, autoincrement=True)
    embedding = Column(Vector)
    opinion = Column(String)
    created_at = Column(TIMESTAMP)

class Sotomayor(Base):
    __tablename__ = 'sotomayor'
    id = Column(Integer, primary_key=True, autoincrement=True)
    embedding = Column(Vector)
    opinion = Column(String)
    created_at = Column(TIMESTAMP)

class Thomas(Base):
    __tablename__ = 'thomas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    embedding = Column(Vector)
    opinion = Column(String)
    created_at = Column(TIMESTAMP)




