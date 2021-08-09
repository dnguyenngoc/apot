import logging
from celery import Celery
from celery import Celery, states
import celery
from celery.exceptions import Ignore
import traceback

from worker.redis import is_backend_running, get_backend_url
from worker.broker import is_broker_running, get_broker_url
from worker.ocr.model import OcrModel
from helpers.image import read_from_path, read_from_url
from settings import ocr_config

if not is_backend_running():
    exit()

if not is_broker_running():
    exit()


app  = Celery(
    ocr_config.CELERY_NAME,  
    broker=get_broker_url(),
    backend=get_backend_url(),
)


app.config_from_object('worker.{}.celery_config'.format(ocr_config.CELERY_NAME))


@app.task(bind=True, name="{}.predict".format(ocr_config.CELERY_NAME))
def predict(self, file_path: str, action_type: str):  
    try:
        ocr = OcrModel(path_to_checkpoint=ocr_config.MODEL_PATH)
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