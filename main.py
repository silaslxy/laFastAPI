from fastapi import FastAPI

from demo.api import demo_router
from ping.api import ping_router


# 异常错误


def create_app():
    # 工程名
    app = FastAPI(title="project-name: laFastApi")

    # 注册模块
    app.include_router(ping_router, prefix="")
    app.include_router(demo_router, prefix="/demo")
    return app


app = create_app()


if __name__ == '__main__':
    import uvicorn

    # uvicorn main:app --reload --host 0.0.0.0 --port 8000
    # reload=False时workers有效
    # workers 启动多个进程
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=9001, workers=2)
