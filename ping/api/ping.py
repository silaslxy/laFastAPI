from fastapi import APIRouter

from ping.serializer import serializers

router = APIRouter()


@router.get("", summary="ping-pong", description="ping-pong:detail", response_model=serializers.PingSerializer)
async def ping():
    """
    ping-pong:detail
    :return:
    """
    res = serializers.PingSerializer()
    return res
