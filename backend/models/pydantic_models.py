from pydantic import BaseModel
from datetime import datetime

class ItemBase(BaseModel):
    name: str
    description: str

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    status: str | None = None

class ItemRead(ItemBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True