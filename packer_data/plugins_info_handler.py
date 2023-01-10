import traceback
from typing import List, Optional

from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from utils import BaseResponse, log, get_db_session
from . import crud
from .orm_model import IOSPluginsInfoTable
from .schemas import IOSPluginsInfo

router = APIRouter()


@router.post("/info")
async def store_data(data: IOSPluginsInfo, db_session: AsyncSession = Depends(get_db_session)):
    try:
        log.info(data)
        await crud.store_data(data, db_session)
    except Exception:
        log.error(traceback.format_exc(chain=False))
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=traceback.format_exc(chain=False))
    else:
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(BaseResponse(message="success")))


@router.get("/info/all")
async def find_all(db_session: AsyncSession = Depends(get_db_session)) -> JSONResponse:
    data: List[IOSPluginsInfoTable] = await crud.find_all_plugins_info(db_session)
    result: List[IOSPluginsInfo] = [IOSPluginsInfo.from_orm(d) for d in data]
    # log.info(result)
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(BaseResponse(message="success", data=result)))


@router.get("/info")
async def find(ip: str, db_session: AsyncSession = Depends(get_db_session)) -> JSONResponse:
    data: List[IOSPluginsInfoTable] = await crud.find(ip, db_session)
    result: List[IOSPluginsInfo] = [IOSPluginsInfo.from_orm(d) for d in data]
    # log.info(result)
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(BaseResponse(message="success", data=result)))


@router.post("/register")
async def register(packager_info: IOSPluginsInfo, db_session: AsyncSession = Depends(get_db_session)):
    result = await crud.find(packager_info.ip, db_session)
    log.info(packager_info)
    if len(result) != 0:
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=jsonable_encoder(
                                BaseResponse(message="the packager has already registered")))
    await crud.register_packager(packager_info, db_session)

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(
                            BaseResponse(message="the packager registers successfully")))

