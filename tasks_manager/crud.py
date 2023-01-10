from typing import Optional

from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from tasks_manager.orm_model import IOSPackTaskTable
from tasks_manager.schemas import IOSPackTask, TaskState
from utils import BaseResponse


async def create_task(task: IOSPackTask, dbs: AsyncSession):
    async with dbs.begin():
        dbs.add(IOSPackTaskTable(**task.dict()))


async def cancel_task(task_id: int, db_session: AsyncSession):
    """取消任务
    :param task_id: 任务id
    :param db_session: 数据库会话
    :return:
    """
    await db_session.execute(update(IOSPackTaskTable)
                             .where(IOSPackTaskTable.id == task_id)
                             .values(task_state=TaskState.CANCELED))
    await db_session.commit()


async def query_task_by_id(task_id: int, db_session: AsyncSession) -> IOSPackTask:
    """通过任务id查找任务
    :param task_id:
    :param db_session:
    :return:
    """
    tasks = await db_session.execute(select(IOSPackTaskTable).filter_by(id=task_id))
    task = tasks.scalars().first()
    task = IOSPackTask.from_orm(task)
    return task


async def update_task(task: IOSPackTask, owner_id: str, executor_id: str, db_session: AsyncSession):
    """更新任务
    :param task:    变更后的状态
    :param owner_id:   发起人id
    :param executor_id:
    :param db_session:
    :return:
    """
    pass


async def search_task_state(state: str,
                            owner_id: Optional[str],
                            packager_ip: Optional[str],
                            db_session: AsyncSession):
    """查询对应状态的任务
    :param state: 任务状态
    :param owner_id: 用户id
    :param packager_ip: 打包机ip
    :param db_session: 数据库会话
    :return:
    """
    async with db_session.begin():
        if not owner_id and not packager_ip:
            result = await db_session.execute(select(IOSPackTaskTable).filter_by(task_state=state))
        elif owner_id and not packager_ip:
            result = await db_session.execute(select(IOSPackTaskTable).
                                              filter_by(task_state=state, owner_id=owner_id))
        elif not owner_id and packager_ip:
            result = await db_session.execute(select(IOSPackTaskTable).
                                              filter_by(task_state=state, packager_ip=packager_ip))
        else:
            result = await db_session.execute(select(IOSPackTaskTable).
                                              filter_by(task_state=state, packager_ip=packager_ip, owner_id=owner_id))
        # db_session.expunge_all()  # 使数据在会话之外能有效，如果设置了expire_on_commit=False可以不写这句
    data = result.scalars().all()
    return data

        
async def task_done(owner_id: Optional[str], packager_ip, db_session: AsyncSession):
    """查询成功的任务
    :param packager_ip: 打包机ip
    :param owner_id: 发起人的user_id
    :param db_session: 数据库回话
    :return: 工程的任务（可能过滤了owner_id）
    """
    return await search_task_state(TaskState.PASS, owner_id,packager_ip,  db_session)


async def task_pending(owner_id: Optional[str], packager_ip, db_session: AsyncSession):
    """查询正在排队的任务"""
    return await search_task_state(TaskState.PENDING, owner_id, packager_ip, db_session)


async def task_failed(owner_id: Optional[str], packager_ip, db_session: AsyncSession):
    """查询失败的任务
    :param packager_ip: 打包机ip
    :param owner_id: 发起人的user_id
    :param db_session: 数据库会话
    :return:
    """
    return await search_task_state(TaskState.FAILED, owner_id, packager_ip, db_session)


async def task_canceled(owner_id: Optional[str], packager_ip, db_session: AsyncSession):
    """查询取消的任务
    :param packager_ip: 打包机ip
    :param owner_id: 发起人的user_id
    :param db_session: 数据库会话
    :return:
    """
    return await search_task_state(TaskState.CANCELED, owner_id, packager_ip, db_session)



