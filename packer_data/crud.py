from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from packer_data.orm_model import IOSPluginsInfoTable
from packer_data.schemas import IOSPluginsInfo
from utils import log


async def store_data(data: IOSPluginsInfo, db_session: AsyncSession):
    async with db_session.begin():
        result = await db_session.execute(select(IOSPluginsInfoTable).where(IOSPluginsInfoTable.ip == data.ip))
        result: IOSPluginsInfoTable = result.scalars().first()
        if result is not None:
            result.cicd_tag = data.cicd_tag
            result.engine_info = data.engine_info
            result.projects_info = data.projects_info
            await db_session.flush()
        else:
            db_session.add(IOSPluginsInfoTable(**data.dict()))  # 这里不用加await, 因为add()不是异步方法，返回的不是Coroutine


async def find_all_plugins_info(db_session: AsyncSession):
    result = await db_session.execute(select(IOSPluginsInfoTable))
    result = result.scalars().all()
    # result = sess.query(IOSPluginsInfoTable).all()    # 异步Session没有这个方法
    return result


async def find(ip: Optional[str], db_session: AsyncSession):
    async with db_session.begin():
        result = await db_session.execute(select(IOSPluginsInfoTable).filter_by(ip=ip))
        result = result.scalars().all()
        db_session.expunge_all()
    return result


async def register_packager(packager: IOSPluginsInfo, db_session: AsyncSession):
    async with db_session.begin():
        db_session.add(IOSPluginsInfoTable(**packager.dict()))
    # log.info(db_session.get_transaction())
    # db_session.begin()
    # try:
    #     db_session.add(IOSPluginsInfoTable(**packager.dict()))
    # except Exception:
    #     await db_session.rollback()
    #     raise
    # else:
    #     await db_session.commit()

