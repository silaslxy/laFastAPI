from datetime import datetime
from enum import Enum
from typing import List, Set
from uuid import UUID

from fastapi import FastAPI, Body
from fastapi import Path
from fastapi import Query, Cookie, Header
from pydantic import BaseModel, Field
# from fastapi import status
# from starlette import status as s_status


from ping.model import serializers

# 异常错误
from fastapi import HTTPException

# test = APIRouter()

app = FastAPI(title="laFastApi")


class ModelNameEnum(str, Enum):
    student = "STUDENT"
    teacher = "TEACHER"


class User(BaseModel):
    username: str
    full_name: str = None


class Item(BaseModel):
    # example 可以列举一个值 做参考
    name: str = Field(default=..., description="姓名", max_length=15, example="xiaosiwen")
    description: str = Field(default="测试", description="描述", max_length=15)
    relation: ModelNameEnum = Field(default=..., description="关系枚举")
    # # name: str
    #     # # description: str = None
    #     # price: float
    #     # tax: float = None
    tags: List[str] = Field(..., description="标签列表必填")
    tags1: List[str] = Field(None, description="标签列表可选")
    tags2: Set[str] = Field(None, description="集合不允许重复")
    user: User = Field(None, description="用户信息")
    users: List[User] = Field(None, description="用户信息列表")
    trace_id: UUID = Field(None, description="链路追踪id")

    # # 生成样本数据
    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "name": "xiaosiwen"
    #         }
    #     }


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


@app.get("/")
def read_root():
    return {"Hello": "World"}


# status_code定义返回的状态码 若要自定义status_code 可以参考fastapi.status
@app.post("/items", status_code=201)
async def create_item(item: Item):
    return item


@app.post("/ex", name="异常请求", description="详细说明", tags=["异常类接口"])
async def throw_ex():
    raise HTTPException(status_code=400, detail="这是一个测试异常")


# 查询参数设置和请求body设置
# 必传查询使用...
@app.get("/items/{item_id}", name="获取item", description="详细说明", tags=["查询类接口"])
def read_item(item_id: int = Path(default=..., description="路径id", title="路径title", gt=0, le=1000),
              trace: str = Cookie(None, description="获取trace"),
              user_agent: str = Header(None, description="用户访问agent 其中convert_underscores控制是否转换",
                                       convert_underscores=False),
              q: str = Query(default=..., max_length=50, description="比传参数使用...", title="23..."),
              list_1: List[str] = Query(..., description="列表参数"),
              limit: int = None):
    return {"item_id": item_id,
            "q": q,
            "limit": limit,
            "list_1": list_1,
            "trace": trace}


# 不带默认值时使用*作为函数的第一个参数
@app.get("/items_test/{item_id}")
async def read_items(
        *, item_id: int = Path(..., title="The ID of the item to get"),
        q: str):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@app.put("/items/{item_id}",
         name="修改item",
         description="根据itemid修改item",
         tags=["更新类接口"],
         # response_model定义返回模型 用于限制返回的数据
         response_model=Item,
         response_model_exclude_none=False,
         response_model_exclude_defaults=False,
         response_model_include={"name"})
def update_item(item_id: int = Path(..., description='项目id'),
                item: Item = Body(..., description="请求参数")):
    # 对象转dict 用于模型之间转换赋值等等
    # item_dict = item.dict()
    # item_other = ItemOther(**item.dict(), hashed_password=hashed_password)

    # 定义模型时最好采用继承的方式以减少定义
    return item


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
