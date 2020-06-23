from datetime import datetime
from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Query

from ping.model import serializers

# test = APIRouter()

app = FastAPI(title="laFastApi")


class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None


# field 字段的定义 可以考虑是否可以使用
# class StrField:
#     value: str
#     description: str
#
#     def __init__(self, description=""):
#         self.description = description
#
#     def __str__(self):
#         return self.value


class ItemFiled(BaseModel):
    name: str


class ModelNameEnum(str, Enum):
    student = "STUDENT"
    teacher = "TEACHER"


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/items/")
async def create_item(item: Item):
    return item


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = Query(None, max_length=50, alias="alias", description="des", title="title"), limit: int = None):
    return {"item_id": item_id, "q": q, "limit": limit}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.get("/model/{model_name}")
async def get_model(model_name: ModelNameEnum):
    if model_name == ModelNameEnum.student:
        return {"model_name": model_name, "message": "silas"}
    else:
        return {"model_name": model_name, "message": "sarira"}


@app.get("/ping/{ping_id}", name="健康检测ping", response_model=serializers.Ping)
async def ping(ping_id: int):
    res = serializers.Ping
    res.pong = "ok"
    res.time = datetime.today()
    res.ping_id = ping_id
    return res.__dict__


if __name__ == '__main__':
    import uvicorn

    # uvicorn main:app --reload --host 0.0.0.0 --port 8000
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=9001, workers=2)
