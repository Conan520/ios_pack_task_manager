import traceback
from typing import Optional

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from tasks_manager import crud
from tasks_manager.schemas import IOSPackTask, TaskState
from utils import log, get_db_session, BaseResponse

task_app = APIRouter()


@task_app.post("/create")
async def create(task: IOSPackTask, dbs: AsyncSession = Depends(get_db_session)) -> JSONResponse:
    log.info("start to create task")
    log.info(f"{task = }")
    try:
        await crud.create_task(task, dbs)
    except Exception:
        log.error(traceback.format_exc(chain=True))
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content=jsonable_encoder(BaseResponse(message="failed")))
    log.info("create task successfully")
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(BaseResponse(message="success")))


@task_app.get("/done")
async def find_task_done(
        owner_id: Optional[str] = None,
        packager_ip: Optional[str] = None,
        db_session: AsyncSession = Depends(get_db_session)):
    data = await crud.task_done(owner_id, packager_ip, db_session)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(BaseResponse(message="success", data=data))
    )


@task_app.get("/pending")
async def find_task_waiting(
        owner_id: Optional[str] = None,
        packager_ip: Optional[str] = None,
        db_session: AsyncSession = Depends(get_db_session)
):
    data = await crud.task_pending(owner_id, packager_ip, db_session)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(BaseResponse(message="success", data=data))
    )


@task_app.get("/failed", description="根据查询失败的任务")
async def find_task_failed(
        owner_id: Optional[str] = None,
        packager_ip: Optional[str] = None,
        db_session: AsyncSession = Depends(get_db_session)
) -> JSONResponse:
    data = await crud.task_failed(owner_id, packager_ip, db_session)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(BaseResponse(message="success", data=data))
    )


@task_app.get("/canceled", description="查询取消的任务")
async def find_task_canceled(
        owner_id: Optional[str] = None,
        packager_ip: Optional[str] = None,
        db_session: AsyncSession = Depends(get_db_session)
) -> JSONResponse:
    data = await crud.task_canceled(owner_id, packager_ip, db_session)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(BaseResponse(message="success", data=data))
    )


@task_app.put("/cancel", description="取消pending中的任务")
async def cancel_task(
        task_id: int,
        owner_id: str,
        owner_name: Optional[str] = None,
        db_session: AsyncSession = Depends(get_db_session)
) -> JSONResponse:
    task = await crud.query_task_by_id(task_id, db_session)
    if task.task_state != TaskState.PENDING:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(BaseResponse(
                message=f"only {TaskState.PENDING} state can be cancelled, current state is {task.task_state}"))
        )
    if owner_id != task.owner_id:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content=jsonable_encoder(
                                BaseResponse(message=f"unauthorized user {owner_name}, this is not your task")))
    await crud.cancel_task(task.id, db_session)
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(BaseResponse(message="success")))
