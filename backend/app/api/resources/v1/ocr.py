# import
from fastapi import APIRouter

# import
from fastapi.responses import JSONResponse

from celery import Celery, states
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED
)
from fastapi import BackgroundTasks
from settings import config
from api.entities.ocr import TaskResult, UrlItem
from settings import ocr_config

router = APIRouter()


ocr = Celery(broker=config.BROKER, backend=config.REDIS_BACKEND)

    
TASKS = {'ocr_predict': '{}.predict'.format(ocr_config.CELERY_NAME),}


def send_result(task_id):
    while True:
        result = ocr.AsyncResult(task_id)
        if result.state in states.READY_STATES:
            break
    output = TaskResult(
        id=task_id,
        status=result.state,
        error=str(result.info) if result.failed() else None,
        result=result.get() if result.state == states.SUCCESS else None
    )
    print(output)


@router.post("/image/predict", status_code=HTTP_201_CREATED)
def get_lenght_image(
    data: UrlItem,
    queue: BackgroundTasks
):
    task = ocr.send_task(
        name=TASKS['ocr_predict'],
        kwargs={'file_path': data.file_path, 'action_type': data.action_type},
        queue=ocr_config.CELERY_NAME
    )
    if data.callback:
        queue.add_task(send_result, task.id)
    return JSONResponse({"id": task.id, 'status': "Processing"})


@router.get("/task/{task_id}")
def get_task_result(task_id: str):
    result = ocr.AsyncResult(task_id)
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