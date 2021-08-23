from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db import SessionLocal, engine, Base, database
import asyncio

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Delivery(BaseModel):
    id: str
    status: str


@app.post("/deliveries/", response_model=Delivery)
async def create_delivery(delivery: Delivery, db: Session = Depends(get_db)):
    query = Delivery.insert().values(text=note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}


@app.get("/users/", response_model=List[Delivery])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
