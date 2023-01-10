from typing import Optional, Any

from pydantic import BaseModel


class BaseResponse(BaseModel):
    message: Optional[str]
    data: Optional[Any]
