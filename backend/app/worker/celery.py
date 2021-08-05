import os
from celery import Celery


app  = Celery('celery_app')
app .conf.broker_url = os.environ.get("CELERY_BROKER_URL")
app .conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")

if __name__ == '__main__':
    app.start()