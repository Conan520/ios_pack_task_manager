from enum import Enum
from typing import Optional

from pydantic import BaseModel, constr


class IOSPackTask(BaseModel):
    id: Optional[int] = None
    task_type: constr(max_length=64)
    task_name: constr(max_length=255)
    task_content: str
    task_state: constr(max_length=32)
    task_result: str
    log_url: str
    owner_id: constr(max_length=96)
    owner_name: constr(max_length=32)
    packager_ip: constr(max_length=255)
    create_time: constr(max_length=32)
    start_time: constr(max_length=32)
    complete_time: constr(max_length=32)
    executor: constr(max_length=64)

    class Config:
        orm_mode = True


class TaskState(str, Enum):
    PENDING = "Pending"
    RUNNING = "Running"
    CANCELED = "Canceled"
    FAILED = "Failed"
    PASS = "Pass"

    def __str__(self):
        return self._value_

    __repr__ = __str__


class TaskType(str, Enum):
    Pack = "PackIOS"    # 打包ios
    Switch = "Switch Branch"    # 切换分支

    def __str__(self):
        return self._value_

    __repr__ = __str__

