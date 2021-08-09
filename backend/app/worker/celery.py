from logging import log
import logging
from celery import Celery
from celery import Celery, states
from celery.exceptions import Ignore
import traceback

from numpy.lib.type_check import imag
from worker.redis import is_backend_running, get_backend_url
from worker.broker import is_broker_running, get_broker_url
from worker.ml.model import OcrModel
from helpers.image import read_from_path, read_from_url


if not is_backend_running():
    exit()

if not is_broker_running():
    exit()

ml  = Celery(
    'ml',  
    broker=get_broker_url(),
    backend=get_backend_url(),
)

ml.config_from_object('worker.ml.config')

MODEL_PATH = './worker/ml/config/transformerocr.pth'


@ml.task(bind=True, name="ml.predict_ocr")
def predict_ocr(self, file_path: str, action_type: str):  
    try:
        ocr = OcrModel(path_to_checkpoint=MODEL_PATH)
    except Exception as e:
        logging.error('Can not load model: {}'.format(str(e)))
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(e).__name__,
                'exc_message': str(e),  # info
                'traceback': traceback.format_exc().split('\n'),
                'message': 'Unable to load model'
            }
        )
        raise Ignore()

    try:
        if action_type == 'path':
            image= read_from_path(file_path)
        else:
            image = read_from_url(file_path)
        data = ocr.predict_text(image=image, return_option='normal')
    except Exception as e:
        logging.error('Can not load predict: {}'.format(str(e)))
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(e).__name__,
                'exc_message': str(e),
                "message": "Unable to predict file"
            }
        )
        raise Ignore()
    
    return {
        'text': data
    }