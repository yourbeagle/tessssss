from sqlalchemy import Column, Integer, String, ForeignKey, orm
from database import Base

class Pegawai(Base):
    __tablename__ = 'pegawai'
    
    id = Column(Integer, primary_key=True, index=True)
    nama_pegawai = Column(String(255))
    email = Column(String(255))
    nomer_hp = Column(String(255))
    alamat = Column(String(255))
    divisi_id = Column(Integer)
    
class Divisi(Base):
    __tablename__ = 'divisi'
    
    id = Column(Integer, primary_key=True, index=True)
    nama_divisi = Column(String(255))