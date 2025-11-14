from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import engine, SessionLocal, Base
from backend.models import db_models, pydantic_models

# Adatbázis létrehozása
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Beadandó Microservice - TODO-list")

# DB kapcsolat
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD

# todo lista
@app.get("/items/", response_model=list[pydantic_models.ItemRead])
def read_items(db: Session = Depends(get_db)):
    return db.query(db_models.Item).all()

# Új todo létrehozása
@app.post("/items/", response_model=pydantic_models.ItemRead)
def create_item(item: pydantic_models.ItemCreate, db: Session = Depends(get_db)):
    db_item = db_models.Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Egy todo lekérése ID alapján
@app.get("/items/{item_id}", response_model=pydantic_models.ItemRead)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(db_models.Item).filter(db_models.Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="TODO nem található")
    return db_item

# todo frissítése
@app.put("/items/{item_id}", response_model=pydantic_models.ItemRead)
def update_item(item_id: int, item: pydantic_models.ItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(db_models.Item).filter(db_models.Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="TODO nem található")
    if item.name is not None:
        db_item.name = item.name
    if item.description is not None:
        db_item.description = item.description
    if item.status is not None:
        db_item.status = item.status
    db.commit()
    db.refresh(db_item)
    return db_item

# todo törlése
@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(db_models.Item).filter(db_models.Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="TODO nem található")
    db.delete(db_item)
    db.commit()
    return {"detail": "TODO törölve"}