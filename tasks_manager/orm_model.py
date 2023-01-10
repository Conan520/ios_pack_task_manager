from typing import Optional

from sqlalchemy import Column, String, Text, BigInteger, select
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession

from utils import engine

Base = declarative_base()


class IOSPackTaskTable(Base):
    __tablename__ = "ios_pack_tasks"
    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    task_type = Column(String(64), primary_key=True, nullable=False)
    task_name = Column(String(255))
    task_content = Column(Text(65536))  # mediumtext
    task_state = Column(String(32), index=True)
    task_result = Column(Text)
    log_url = Column(String(255))
    owner_id = Column(String(96))
    owner_name = Column(String(32), index=True)
    packager_ip = Column(String(255))
    create_time = Column(String(32))
    start_time = Column(String(32))
    complete_time = Column(String(32))
    executor = Column(String(64), index=True)

    def __init__(
            self, *,
            id: Optional[int],
            task_type: str,
            task_name: Optional[str],
            task_content: str,
            task_state: str,
            task_result: str,
            log_url: Optional[str],
            owner_id: str,
            owner_name: str,
            packager_ip: Optional[str],
            create_time: str,
            start_time: str,
            complete_time: str,
            executor: str
    ):
        self.id = id
        self.task_type = task_type
        self.task_name = task_name
        self.task_content = task_content
        self.task_state = task_state
        self.task_result = task_result
        self.log_url = log_url
        self.owner_id = owner_id
        self.owner_name = owner_name
        self.packager_ip = packager_ip
        self.create_time = create_time
        self.start_time = start_time
        self.complete_time = complete_time
        self.executor = executor
