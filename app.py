"""Модуль для работы с приложением."""
from typing import List, Any
from fastapi import FastAPI
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db import engine, database, deliveries, Delivery

app = FastAPI()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all(bind=engine)


def get_db() -> None:
    """Управление сессиями."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root() -> dict:
    """Приветственный скрипт."""
    return {"message": "Welcome to ExpressDelivery!"}


@app.post("/deliveries/", response_model=Delivery)
async def create_delivery(delivery: Delivery) -> Any:
    """Создание или изменение заказа."""
    query = deliveries.insert().values(id=delivery.id, status=delivery.status)
    last_record_id = await database.execute(query)
    return {**delivery.dict(), "id": last_record_id}


@app.get("/deliveries/", response_model=List[Delivery])
async def fetch_db() -> None:
    """Вывод информации о заказах."""
    query = deliveries.select()
    return await database.fetch_all(query)
