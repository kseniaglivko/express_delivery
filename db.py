from sqlalchemy import create_engine, Column, String, Table, MetaData
from sqlalchemy_utils.types.choice import ChoiceType
from typing import List
import databases
from fastapi import FastAPI
from pydantic import BaseModel

DATABASE_URL = "postgresql://dbuser:dbpassword@localhost/express_delivery"

database = databases.Database(DATABASE_URL)

metadata = MetaData()

deliveries = Table(
    "deliveries",
    metadata,
    Column("id", String(5), primary_key=True),
    Column(
        "status",
        ChoiceType(
            [("to_do", "to_do"), ("in_progress", "in_progress"), ("done", "done")],
            impl=String(),
        ),
        comment="Status",
    ),
)


engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)


class Delivery(BaseModel):
    id: str
    status: str


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/deliveries/", response_model=List[Delivery])
async def read_db():
    query = deliveries.select()
    return await database.fetch_all(query)


@app.post("/deliveries/", response_model=Delivery)
async def update_db(del_: Delivery):
    query = deliveries.insert().values(text=del_.id, status=del_.status)
    last_record_id = await database.execute(query)
    return {**del_.dict(), "id": last_record_id}
