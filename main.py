import uvicorn
from fastapi import FastAPI

from packer_data import router
from tasks_manager import task_app

app = FastAPI(
    title="IOS打包任务管理服务器",
    version="1.0.0",
    description="IOS打包任务管理器服务"
)


@app.get("/")
async def hello():
    return {"message": "This is ios-pack-task-manager Service"}


app.include_router(router, prefix="/packager")
app.include_router(task_app, prefix="/tasks")


def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8088, reload=True)


if __name__ == '__main__':
    main()
