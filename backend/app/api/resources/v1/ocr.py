# import
import logging
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.param_functions import Form
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.sql.expression import desc

# import
from databases.db import get_db
from databases.logic import user as user_logic
from api.entities import account as account_entity
from securities import token as token_helper
from helpers import time as time_helper
from datetime import timedelta
from securities import ldap
from fastapi import File, UploadFile
from worker.tasks import predict_ocr_single
from celery.result import AsyncResult
from fastapi.responses import JSONResponse
import numpy as np
import cv2


router = APIRouter()

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


@router.post('/ocr/predict', response_model=OcrResponse, status_code=202)
async def ocr(file: UploadFile = File(...)):
    """Create celery prediction task. Return task_id to client in order to retrieve result"""
    byte_file = file.file.read() # fix load file to image and bla bla here
    if len(byte_file) > 5**22: 
        raise HTTPException(status_code=400, detail="wrong size > 5MB")
    image = cv2.imdecode(np.frombuffer(byte_file, np.uint8), 1)
    task_id = predict_ocr_single.delay(image)
    return {'task_id': str(task_id), 'status': 'Processing'}


@router.get('/ocr/result/{task_id}', response_model=PredictionResponse, status_code=200,
         responses={202: {'model': OcrResponse, 'description': 'Accepted: Not Ready'}})
async def ocr_result(task_id):
    """Fetch result for given task_id"""
    task = AsyncResult(task_id)
    if not task.ready():
        print(router.url_path_for('ocr'))
        return JSONResponse(status_code=202, content={'task_id': str(task_id), 'status': 'Processing'})
    result = task.get()
    return {'task_id': task_id, 'status': 'Success', 'probability': str(result)}