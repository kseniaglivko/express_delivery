"""Модуль для работы с базой данных."""
from enum import Enum
from pydantic import BaseModel, constr
from sqlalchemy import create_engine, Column, String, Table, MetaData
import databases

DATABASE_URL = "postgresql://dbuser:dbpassword@localhost/express_delivery"

DELIVERY_ID_TYPE = constr(regex="^[a-z0-9]{2,5}$")

database = databases.Database(DATABASE_URL)

metadata = MetaData()

# Таблица с информацией о заказах на доставку.
deliveries = Table(
    "deliveries",
    metadata,
    Column("id", String(5), primary_key=True, index=True),
    Column("status", String(11), comment="Status"),
)

engine = create_engine(DATABASE_URL)

metadata.create_all(engine)


class StatusEnum(str, Enum):
    """Класс для валидации возможных статусов заказа."""

    to_do = "to_do"
    in_progress = "in_progress"
    done = "done"


class Delivery(BaseModel):
    """Класс для валидации тела запроса."""

    id: DELIVERY_ID_TYPE  # type: ignore
    status: StatusEnum
