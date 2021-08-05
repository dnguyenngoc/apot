from celery.app import task
from celery.result import AsyncResult
from fastapi import Body, FastAPI, Form, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import File, UploadFile


# from worker.tasks import create_task


from worker.tasks import predict_ocr_single


# move to entity api
from pydantic import BaseModel
class OcrResponse(BaseModel):
    """ Celery task representation """
    task_id: str
    status: str

class PredictionResponse(BaseModel):
    task_id: str
    status: str
    probability: str


app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")



# @app.get("/")
# def home(request: Request):
#     return templates.TemplateResponse("home.html", context={"request": request})


# @app.post("/tasks", status_code=201)
# def run_task(payload = Body(...)):
#     task_type = payload["type"]
#     task = create_task.delay(int(task_type))
#     return JSONResponse({"task_id": task.id})


# @app.get("/tasks/{task_id}")
# def get_status(task_id):
#     task_result = AsyncResult(task_id)
#     result = {
#         "task_id": task_id,
#         "task_status": task_result.status,
#         "task_result": task_result.result
#     }
#     return JSONResponse(result)


@app.post('/ocr/predict', response_model=OcrResponse, status_code=202)
async def ocr(file: UploadFile = File(...)):
    """Create celery prediction task. Return task_id to client in order to retrieve result"""

    image = file # fix load file to image and bla bla here
    task_id = predict_ocr_single.delay(image)
    return {'task_id': str(task_id), 'status': 'Processing'}


@app.get('/ocr/result/{task_id}', response_model=PredictionResponse, status_code=200,
         responses={202: {'model': OcrResponse, 'description': 'Accepted: Not Ready'}})
async def ocr_result(task_id):
    """Fetch result for given task_id"""
    task = AsyncResult(task_id)
    if not task.ready():
        print(app.url_path_for('ocr'))
        return JSONResponse(status_code=202, content={'task_id': str(task_id), 'status': 'Processing'})
    result = task.get()
    return {'task_id': task_id, 'status': 'Success', 'probability': str(result)}