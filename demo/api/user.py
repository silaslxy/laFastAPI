from fastapi import APIRouter, Path

from demo.enum.enums import UserCategoryEnum
from demo.serializer.user_serializers import UserSerializer, CategoryDetailSerializer

user_router = APIRouter()


# status_code定义返回的状态码 若要自定义status_code 可以参考fastapi.status
# summary: 关于url的简单介绍
# description: 关于url的详细描述， 有限使用description， 其次文档字符串
# response_model: 限制返回的数据格式
@user_router.post("", summary="创建用户", description="创建用户详细介绍", response_model=UserSerializer)
async def create_user(user_serializer: UserSerializer):
    """
    创建用户详细介绍
    :param user_serializer:
    :return:
    """
    return user_serializer


@user_router.get("/{category}", summary="根据类型获取介绍",
                 description="根据类型获取介绍",
                 response_model=CategoryDetailSerializer)
async def get_category_detail(category: UserCategoryEnum = Path(..., description="用户枚举类型")):
    """
    根据类型获取介绍
    :param category:
    :return:
    """
    res = CategoryDetailSerializer()
    res.category = category
    if category == UserCategoryEnum.student:
        res.description = "学生"
    else:
        res.description = "老师"
    return res
