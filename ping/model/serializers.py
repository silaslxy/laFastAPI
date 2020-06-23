from datetime import datetime

from pydantic import BaseModel


class Ping(BaseModel):
    pong: str
    time: datetime
    ping_id: int


class ResTest(BaseModel):
    password: str
    username: str
