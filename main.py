from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class PegawaiBase(BaseModel):
    nama_pegawai:str
    email:str
    nomer_hp:str
    alamat:str
    divisi_id:int
    
class DivisiBase(BaseModel):
    nama_divisi:str
    

def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

database_dependency = Annotated[Session, Depends(get_database)]

@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse("/docs", status_code=308)
    

@app.get("/pegawai/", status_code= status.HTTP_200_OK)
async def listPegawai(db : database_dependency):
    get_all = db.query(models.Pegawai).order_by(models.Pegawai.nama_pegawai.asc()).all()
    if get_all:
        return {
            "message" : "Get All Data Pegawai Success",
            "data" : get_all
        }
    return {
        "error": "There is No Data Pegawai"
    }

@app.post("/pegawai/", status_code = status.HTTP_201_CREATED)
async def addPegawai(pegawai: PegawaiBase, db: database_dependency):
    create_pegawai = models.Pegawai(**pegawai.dict())
    if create_pegawai:
        db.add(create_pegawai)
        db.commit()
        return {
            "message" : "Create Pegawai Success"
        }
          
@app.get("/pegawai/{id}", status_code= status.HTTP_200_OK)
async def getPegawaiByID(id:int, db:database_dependency):
    get_pegawai = db.query(models.Pegawai).filter(models.Pegawai.id == id).first()
    if get_pegawai is None:
        raise HTTPException(status_code=404, detail = "Data Pegawai Tidak Ditemukan")
    return {
        "message" : "Get Data Pegawai Success",
        "data" : get_pegawai
    }
    

@app.get("/pegawai/divisi/{id}", status_code=status.HTTP_200_OK)
async def getDataByDivisiID(id:int, db:database_dependency):
    get_pegawai_divisi = db.query(models.Pegawai).filter(models.Pegawai.divisi_id == id).all()
    if get_pegawai_divisi is None:
        raise HTTPException(status_code=404, detail="Tidak ada pegawai di divisi tersebut")
    return {
        "message" : "Sukses Get Data Pegawai",
        "data" : get_pegawai_divisi
    }

@app.put("/pegawai/{id}", status_code= status.HTTP_200_OK)
async def updatePegawai(id:int, db:database_dependency, pegawai: PegawaiBase):
    update_pegawai = db.query(models.Pegawai).filter(models.Pegawai.id == id).first()
    if update_pegawai:
        update_pegawai.nama_pegawai = pegawai.nama_pegawai
        update_pegawai.email = pegawai.email
        update_pegawai.nomer_hp = pegawai.nomer_hp
        update_pegawai.alamat = pegawai.alamat
        update_pegawai.divisi_id = pegawai.divisi_id
        db.commit()
        db.refresh(update)
        return {
            "message" : "Update Data Pegawai Success",
            "data": update_pegawai
        }
    return {
        "error" : "ID Not Exist"
    }

@app.delete("/pegawai/{id}", status_code=status.HTTP_200_OK)
async def deletePegawai(id:int, db:database_dependency):
    delete_pegawai = db.query(models.Pegawai).filter(models.Pegawai.id == id).first()
    if delete_pegawai is None:
        raise HTTPException(status_code=404, detail="Data Pegawai Tidak Ditemukan")
    db.delete(delete_pegawai)
    db.commit()
    return {
        "message" : "Berhasil Hapus Data Pegawai"
    }
    
