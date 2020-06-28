from datetime import datetime
from typing import List, Set
from uuid import UUID

from pydantic import BaseModel, Field, validator

from demo.serializer.user_serializers import UserSerializer


class ItemSerializer(BaseModel):
    """
    项目数据序列化与校验
    """

    # example 可以列举一个值 做参考
    # default = ... 表示该字段必填
    # default = None 表示字段选填
    name: str = Field(default=..., description="姓名", max_length=15, example="silas")
    description: str = Field(default=None, description="描述", max_length=15)
    tags: List[str] = Field(None, description="标签列表可选")
    require_tags: List[str] = Field(..., description="标签列表必填")
    unique_tags: Set[str] = Field(None, description="标签列表必填去重")
    user: UserSerializer = Field(None, description="用户信息")
    # max_items/min_items 设置列表的长度
    users: List[UserSerializer] = Field(..., description="用户信息列表", max_items=3, min_items=1)
    trace_id: UUID = Field(None, description="链路追踪id")
    create_time: datetime = Field(datetime.now(), description="创建时间")

    @validator("name")
    def validator_name(cls, value):
        """
        其他字段校验
        :param value:
        :return:
        """
        if value == "test":
            raise ValueError("不能为test")
        return value

    # # 生成样本数据
    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "name": "xiaosiwen"
    #         }
    #     }
