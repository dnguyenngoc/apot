# apot
Serving ML Models in Production with FastAPI and Celery

## Overview
There is an abundance of material online related to building and training all kinds of machine learning models. However once a high performance model has been trained there is significantly less material for how to put it into production.

This post walks through a working example for serving a ML model using Celery and FastAPI. All code can be found in the repository here.
<link> git


## Potential Options
Below is a summary of potential approaches for deploying your trained models to production:
Load model directly in application: this option involves having the pretrained model directly in the main application code. For small models this might be feasible however large models may introduce memory issues. This option also introduces a direct dependency on the model within the main application (coupled).
Offline batch prediction: Use cases that do not require near real-time predictions can make use of this option. The model can be used the make predictions for a batch of data in a process that runs at defined intervals (e.g. overnight). The predictions can then be utilized by the application once the batch job is complete. Resource for prediction is only required when the batch process runs which can be beneficial.
API: The third option is to deploy the model as its own microservice and communicate with it via an API. This decouples the application from the model and allows it to be utilized from multiple other services. The ML service can serve requests in one of the two ways described below.
Synchronous: the client requests a prediction and must wait for the model service to return a prediction. This is suitable for small models that require a small number of computations, or where the client cannot continue other processing steps without a prediction.
Asynchronous: instead of directly returning a prediction the model service will return a unique identifier for a task. Whilst the prediction task is being completed by the model service the client is free to continue other processing. The result can then be fetched via a results endpoint using the unique task id.

## Process Flow

The steps below describe the actions taken to handle a prediction request:

1 Client sends a POST request to the FastAPI prediction endpoint, with the relevant feature information contained in the request body (JSON).
2 The request body is validated by FastAPI against a defined model (i.e. checks if the expected features have been provided). If the validation is successful then a Celery prediction task is created and passed to the configured broker (e.g. RabbitMQ).
3 The unique id is returned to the client if a task is created successfully.
4 The prediction task is delivered to an available worker by the broker. Once delivered the worker generates a prediction using the pretrained ML model.
5 Once a prediction has been generated the result is stored using the Celery backend (e.g. Redis).
6 At any point after step 3 the client can begin to poll the FastAPI results endpoint using the unique task id. Once the prediction is ready it will be returned to the client.




## Project Structure
The project structure is as follows:
serving_ml
│   app.py
│   models.py
│   README.md
│   requirements.txt
│   test_client.py
│
├───celery_task_app
│   │   tasks.py
│   │   worker.py
│   │   __init__.py
│   │
│   ├───ml
│   │   │   model.py
│   │   │   __init__.py
app.py: FastAPI application including route definitions.
models.py: Pydantic model definitions that are used for the API validation and response structure.
test_client.py: Script used for testing the set-up. We’ll cover this in more detail later.
celery_task_app\tasks.py: Contains Celery task definition, specifically the prediction task in our case.
celery_task_app\worker.py: Defines the celery app instance and associated config.
celery_task_app\ml\model.py: Machine learning model wrapper class used to load pretrained model and serve predictions.


ML Model
First let’s look at how we are going to load the pretrained model and calculate predictions. The code below defines a wrapper class for a pretrained model that loads from file on creation and calculates class probability or membership in its predict method.

## code sample


## Celery
Celery is a simple task queue implementation that can used to distribute tasks across threads and/or machines. The implementation requires a broker and optionally a backend:
Broker: This is used to deliver messages between clients and workers. To initiate a task the client adds a message to the queue, the broker then delivers that message to a worker. RabbitMQ is often used as the broker and is the default used by Celery.
Backend: This is optional and its only function is to store task results to be retrieved at a later date. Redis is commonly used as the backend.
First let’s look at how we define our Celery app instance: