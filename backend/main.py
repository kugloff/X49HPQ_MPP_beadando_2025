from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import engine, SessionLocal, Base
from backend.models import db_models, pydantic_models

# Adatbázis létrehozása
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Beadandó Microservice")

# DB kapcsolat
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Lista minden itemről
@app.get("/items/", response_model=list[pydantic_models.ItemRead])
def read_items(db: Session = Depends(get_db)):
    return db.query(db_models.Item).all()

# Új item létrehozása
@app.post("/items/", response_model=pydantic_models.ItemRead)
def create_item(item: pydantic_models.ItemCreate, db: Session = Depends(get_db)):
    db_item = db_models.Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item