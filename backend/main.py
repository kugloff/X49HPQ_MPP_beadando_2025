from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pydantic import BaseModel
from datetime import datetime, date
import asyncio
import os
from dotenv import load_dotenv
import logging

# logolás beállítás
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("/tmp/backend.log"),
        logging.StreamHandler()
    ]
)

# load .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# database setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# sqlalchemy model
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=True)

Base.metadata.create_all(bind=engine)

# pydantic models
class ItemCreate(BaseModel):
    name: str
    description: str
    due_date: datetime | None = None

class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    status: str | None = None
    due_date: datetime | None = None

class ItemRead(ItemCreate):
    id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True

# fastapi app
app = FastAPI(title="TODO alkalmazás")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# background task
async def check_overdue():
    while True:
        db: Session = SessionLocal()
        try:
            today = date.today()
            items = db.query(Item).filter(Item.status == "pending").all()
            for item in items:
                if item.due_date and item.due_date.date() < today:
                    item.status = "overdue"
                    db.add(item)
                    logging.info(f"TODO '{item.name}' státusza lejárt lett.")
            db.commit()
        except Exception as e:
            logging.error(f"Hiba a check_overdue futása közben: {e}")
        finally:
            db.close()
        await asyncio.sleep(60*60)  # óránként

@app.on_event("startup")
async def start_background_tasks():
    logging.info("Háttérfolyamat elindítva: check_overdue")
    asyncio.create_task(check_overdue())

# crud
@app.get("/items/", response_model=list[ItemRead])
def read_items(db: Session = Depends(get_db)):
    try:
        items = db.query(Item).all()
        logging.info(f"{len(items)} TODO lekérdezve")
        return items
    except Exception as e:
        logging.error(f"Hiba TODO lekérdezéskor: {e}")
        raise HTTPException(status_code=500, detail="Hiba történt a lekérdezés során")

@app.post("/items/", response_model=ItemRead)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    try:
        existing_item = db.query(Item).filter(Item.name == item.name).first()
        if existing_item:
            logging.warning(f"Duplikált TODO létrehozás kísérlet: {item.name}")
            raise HTTPException(status_code=400, detail="Már létezik ilyen nevű TODO")
        
        status = "overdue" if item.due_date and item.due_date < datetime.utcnow() else "pending"

        db_item = Item(
            name=item.name,
            description=item.description,
            due_date=item.due_date,
            status=status
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        logging.info(f"TODO létrehozva: {db_item.name} (status: {db_item.status})")
        return db_item
    except Exception as e:
        logging.error(f"Hiba TODO létrehozásakor: {e}")
        raise HTTPException(status_code=500, detail="Hiba történt a TODO létrehozásakor")

@app.put("/items/{item_id}", response_model=ItemRead)
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    try:
        db_item = db.query(Item).filter(Item.id == item_id).first()
        if not db_item:
            logging.warning(f"Nem található TODO frissítéshez: {item_id}")
            raise HTTPException(status_code=404, detail="TODO nem található")
        if item.name is not None:
            db_item.name = item.name
        if item.description is not None:
            db_item.description = item.description
        if item.status is not None:
            db_item.status = item.status
        db.commit()
        db.refresh(db_item)
        logging.info(f"TODO frissítve: {db_item.name}")
        return db_item
    except Exception as e:
        logging.error(f"Hiba TODO frissítésekor: {e}")
        raise HTTPException(status_code=500, detail="Hiba történt a TODO frissítésekor")

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    try:
        db_item = db.query(Item).filter(Item.id == item_id).first()
        if not db_item:
            logging.warning(f"Nem található TODO törléshez: {item_id}")
            raise HTTPException(status_code=404, detail="TODO nem található")
        db.delete(db_item)
        db.commit()
        logging.info(f"TODO törölve: {db_item.name}")
        return {"detail": "TODO törölve"}
    except Exception as e:
        logging.error(f"Hiba TODO törléskor: {e}")
        raise HTTPException(status_code=500, detail="Hiba történt a TODO törlésekor")