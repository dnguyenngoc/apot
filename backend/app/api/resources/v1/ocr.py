# import
import logging
from typing import Any, Optional
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.param_functions import Form
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.sql.expression import desc

# import
from securities import ldap
from fastapi import File, UploadFile
from celery.result import AsyncResult
from fastapi.responses import JSONResponse

from celery import Celery, states
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED
)
from fastapi import BackgroundTasks
from pydantic import BaseModel

router = APIRouter()
from settings import config


ml = Celery(broker=config.BROKER, backend=config.REDIS_BACKEND)

    
TASKS = {
    'ocr': 'ml.predict_ocr',
}


def send_result(task_id):
    while True:
        result = ml.AsyncResult(task_id)
        if result.state in states.READY_STATES:
            break
    output = TaskResult(
        id=task_id,
        status=result.state,
        error=str(result.info) if result.failed() else None,
        result=result.get() if result.state == states.SUCCESS else None
    )
    print(output)


class UrlItem(BaseModel):
    file_url: str
    callback: bool = False


class TaskResult(BaseModel):
    id: str
    status: str
    error: Optional[str] = None
    result: Optional[Any] = None



@router.post("/image/predict", status_code=HTTP_201_CREATED)
def get_lenght_image(data: UrlItem, queue: BackgroundTasks):
    task = ml.send_task(
        name=TASKS['ocr'],
        kwargs={'file_path': data.file_url},
        queue='ml'
    )
    if data.callback:
        queue.add_task(send_result, task.id)
    return JSONResponse({"id": task.id, 'status': "Processing"})



@router.get("/task/{task_id}")
def get_task_result(task_id: str):

    result = ml.AsyncResult(task_id)

    output = TaskResult(
        id=task_id,
        status=result.state,
        error=str(result.info) if result.failed() else None,
        result=result.get() if result.state == states.SUCCESS else None
    )

    return JSONResponse(
        status_code=HTTP_200_OK,
        content=output.dict()
    )