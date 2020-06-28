from typing import List

from fastapi import APIRouter, Path, Cookie, Header, Query, Body

from demo.serializer.item_serializers import ItemSerializer

from fastapi.encoders import jsonable_encoder

item_router = APIRouter()


# status_code定义返回的状态码 若要自定义status_code 可以参考fastapi.status
# summary: 关于url的简单介绍
# description: 关于url的详细描述， 有限使用description， 其次文档字符串
# response_model: 限制返回的数据格式，
# response_model_include: 更详细的控制
@item_router.post("", summary="创建项目",
                  description="创建项目详细介绍",
                  response_model=ItemSerializer)
async def create_item(item_serializer: ItemSerializer):
    """
    创建项目详细介绍doc
    :param item_serializer:
    :return:
    """
    return item_serializer


#
# @app.post("/ex", name="异常请求", description="详细说明", tags=["异常类接口"])
# async def throw_ex():
#     raise HTTPException(status_code=400, detail="这是一个测试异常")

# 查询参数设置和请求body设置
# 必传查询使用...
# 使用fastapi.Path 做路径参数的格式校验
# 使用fastapi.Cookie 从cookie中获取所需的值
# 使用fastapi.Header 从header中获取所需的值 如user_agent
# 使用fastapi.Query 做查询参数的校验
@item_router.get("/{item_id}", summary="获取项目", description="根据项目ID获取项目详情")
async def get_item_by_id(item_id: int = Path(default=..., description="路径id", gt=0, le=1000),
                         trace_id: str = Cookie(None, description="获取traceId"),
                         user_agent: str = Header(..., description="用户访问agent", convert_underscores=True),
                         name: str = Query(default=..., max_length=50, description="名称"),
                         names: List[str] = Query(None, description="名称批量查询")):
    """
    根据项目ID获取项目详情
    :param item_id:
    :param trace_id:
    :param user_agent:
    :param name:
    :param names:
    :return:
    """
    return {
        "item_id": item_id,
        "trace_id": trace_id,
        "user_agent": user_agent,
        "name": name,
        "names": names
    }


# 使用fastapi.Body 作requestBody
@item_router.put("/{item_id}", summary="更新项目", description="根据项目ID更新项目",
                 response_model=ItemSerializer)
async def update_item(item_id: int = Path(..., description='项目id'),
                      item_serializer: ItemSerializer = Body(..., description="请求参数")):
    """
    根据项目ID更新项目
    :param item_id:
    :param item_serializer:
    :return:
    """
    if item_id is not None:
        # jsonable_encoder 将输入数据转化为可存储的json数据
        # 场景：数据库（假设仅接受json兼容的数据）不接收datetime 需要转成json
        # item_serializer.dict() 其中的create_time 还是datetime类型
        encoded = jsonable_encoder(item_serializer)
        # 部分更新，只能发送要更新的数据，其余数据保持不变，忽略默认值
        update = item_serializer.copy(update=item_serializer.dict(exclude_unset=True))

        return update

    return ItemSerializer()


# 使用* 之后的参数被当作关键字参数，与顺序无关，自动匹配 查询参数不实用Query 路径参数使用Path
# 不使用* name无默认值会抛异常
@item_router.get("/test/{item_id}", summary="测试:获取项目", description="测试:根据项目ID获取项目详情")
async def read_items(*,
                     item_id: int = Path(..., description="项目ID"),
                     name: str):
    results = {"item_id": item_id}
    if name:
        results.update({"name": name})
    return results
