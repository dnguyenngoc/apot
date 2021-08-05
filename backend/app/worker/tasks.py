from worker.celery import app
import time
from celery import Task
import logging
import importlib


# task sample will remove
# @app.task(name="create_task")
# def create_task(task_type):
#     time.sleep(int(task_type) * 10)
#     return True


class OcrPredictTask(Task):
    """
    Abstraction of Celery's Task class to support loading ML model.
    """
    abstract = True

    def __init__(self):
        super().__init__()
        self.model = None

    def __call__(self, *args, **kwargs):
        """
        Load model on first call (i.e. first task processed)
        Avoids the need to load model on each task request
        """
        if not self.model:
            logging.info('Loading Model...')
            module_import = importlib.import_module(self.path[0])
            model_obj = getattr(module_import, self.path[1])
            self.model = model_obj()
            logging.info('Model loaded')
        return self.run(*args, **kwargs)


@app.task(ignore_result=False,
          bind=True,
          base=OcrPredictTask,
          path=('worker.ml.model', 'OcrModel'),
          name='{}.{}'.format(__name__, 'Ocr'))

def predict_ocr_single(self, image):
    """
    Essentially the run method of PredictTask
    """
    pred_array = self.model.predict(image)
    positive_prob = pred_array[0][-1]
    return positive_prob