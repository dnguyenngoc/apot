from pydantic import BaseModel
from typing import Any, Optional, List



class OcrParam(BaseModel):
    image: Optional[Any]
    callback: bool = False


class OcrBatchParam(BaseModel):
    batch: List[Optional[Any]]
    callback: bool = False


class OcrResponse(BaseModel):
    id: str
    status: str
    error: Optional[str] = None
    result: Optional[Any] = None
