"""Модуль для работы с базой данных."""
from typing import Set
from pydantic import BaseModel, constr
from sqlalchemy import create_engine, Column, String, Table, MetaData
from sqlalchemy_utils.types.choice import ChoiceType
import databases

DATABASE_URL = "postgresql://dbuser:dbpassword@localhost/express_delivery"

database = databases.Database(DATABASE_URL)

metadata = MetaData()

# Таблица с информацией о заказах на доставку.
deliveries = Table(
    "deliveries",
    metadata,
    Column("id", String(5), primary_key=True, index=True),
    Column(
        "status",
        ChoiceType(
            [("to_do", "to_do"), ("in_progress", "in_progress"), ("done", "done")],
            impl=String(),
        ),
        comment="Status",
    ),
)

engine = create_engine(DATABASE_URL)

metadata.create_all(engine)

delivery_id_type = constr(regex="^[a-z0-9]{2,5}$")


class Delivery(BaseModel):
    """Класс для валидации тела запроса."""
    id: str
    status: Set[delivery_id_type]
