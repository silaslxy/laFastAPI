from datetime import datetime

from fastapi import FastAPI

from ping.model import serializers

# test = APIRouter()

app = FastAPI(title="laFastApi")


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
    uvicorn.run("main:app", reload=False, host="0.0.0.0", port=9001, workers=2)
