from pydantic import BaseModel, Field

from demo.enum.enums import UserCategoryEnum


class UserSerializer(BaseModel):
    """
    用户数据序列化与校验
    """
    username: str = Field(default=..., description="用户名", max_length=32)
    full_name: str = Field(default=..., description="全名", max_length=32)
    category: UserCategoryEnum = Field(default=..., description="用户类型")


class CategoryDetailSerializer(BaseModel):
    """
    用户类型描述
    """
    category: UserCategoryEnum = Field(default=None, description="用户类型")
    description: str = Field(default=None, description="用户类型描述")
