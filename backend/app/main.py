from fastapi import FastAPI
from settings import config
import logging
from logging.handlers import TimedRotatingFileHandler
from fastapi.middleware.cors import CORSMiddleware
from databases.db import Session
from starlette.requests import Request
from api.routers import v1


# ++++++++++++++++++++++++++++++++++++++++++++ DEFINE APP +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
app = FastAPI(title=config.PROJECT_NAME, openapi_url="/api/openapi.json", docs_url="/api/docs", redoc_url="/api/redoc")


# ++++++++++++++++++++++++++++++++++++++++++++ HANDLE LOG FILE +++++++++++++++++++++++++++++++++++++++++++++++++++++++
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler = TimedRotatingFileHandler('logs/fastapi/{}-{}-{}_{}h-00p-00.log'.format(
    config.u.year, config.u.month, config.u.day , config.u.hour), when="midnight", interval=1, encoding='utf8')
handler.suffix = "%Y-%m-%d"
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)


# ++++++++++++++++++++++++++++++++++++++++++++ ROUTER CONFIG ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
app.include_router(v1.router, prefix="/api/v1")


# ++++++++++++++++++++++++++++++++++++++++++++ CORS MIDDLEWARE ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
origins = [
    "http://{host}".format(host=config.HOST_NAME),
    "http://{host}:{port}".format(host=config.HOST_NAME, port = config.BE_PORT),
    "http://{host}:{port}".format(host=config.HOST_NAME, port = config.FE_PORT)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ++++++++++++++++++++++++++++++++++++++++++++++ DB CONFIG ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response



# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# from fastapi import File, UploadFile
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")


# from worker.tasks import create_task
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


