from enum import Enum


class UserCategoryEnum(str, Enum):
    """
    用户类型枚举
    """
    student = "STUDENT"
    teacher = "TEACHER"
