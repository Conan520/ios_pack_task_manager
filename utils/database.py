from typing import Callable, AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    'mysql+aiomysql://root:root123@localhost:3306/meta_verse_plugins_v2',
    pool_pre_ping=True,
    encoding="utf-8",
)

async_session_factory: Callable[..., AsyncSession] = sessionmaker(
    engine,
    class_=AsyncSession,
    future=True,
    expire_on_commit=False,     # 防止数据开始会话后失效
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """session生成器 作为FastApi的Depends选项"""
    async with async_session_factory() as session:
        yield session
