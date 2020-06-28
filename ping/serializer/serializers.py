from datetime import datetime
from pydantic import BaseModel, Field


class PingSerializer(BaseModel):
    """
    接口返回的序列化
    """

    # default:设置默认值
    # description: 字段描述
    # max_length: 字符长度限制
    # example: 调试时在swagger中的默认值
    pong: str = Field(default="pong", description="ping-pong", max_length=15, example="pong")
