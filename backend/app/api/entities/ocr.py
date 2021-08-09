from pydantic import BaseModel
from typing import Any, Optional, List


class UrlItem(BaseModel):
    file_path: str
    callback: bool = False


class TaskResult(BaseModel):
    id: str
    status: str
    error: Optional[str] = None
    result: Optional[Any] = None

