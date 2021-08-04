# import
from re import I
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import Form

# import
from databases.db import get_db
from securities import token as token_helper

from settings import config
from helpers.nas import NasWebDavConnect
from helpers import time as time_helper


router = APIRouter()


@router.post("/pnl")
def upload( 
    user = Depends(token_helper.get_current_user),
    file: UploadFile = Form(...),
    sheet_name: str = Form(...),
    password: str = Form(...),
    month: int = Form(...),
    year: int = Form(...)

):
    role_name = user.role_name
    check = False
    for item in role_name:
        if item == 'superuser' or item == 'pnl':
            check = True
            break
    if check == False:
        raise HTTPException(status_code=400, detail="permission denied!")
    if file.content_type not in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
        raise HTTPException(status_code=400, detail="type support is .xls .xlsx")
    byte_excel = file.file.read()
    if len(byte_excel) > 20**22: 
        raise HTTPException(status_code=400, detail="wrong size > 20MB")
    nas = NasWebDavConnect(
        webdav_hostname = config.NAS_HOST,
        webdav_login = config.NAS_USER,
        webdav_password = config.NAS_PASSWORD,
        lazy = False
    )
    try:
        str_dir = time_helper.str_yyyy_mm_from_int(year, month, "-")
        str_file_name = time_helper.str_yyyy_mm_dd()
        if nas.is_existed(config.NAS_ROOT_PATH + "/{str_dir}".format(str_dir = str_dir)) == False:
            nas.create_path(config.NAS_ROOT_PATH + "/{str_dir}".format(str_dir = str_dir))
        nas.upload_file(byte_excel, config.NAS_ROOT_PATH + "/{str_dir}/{str_file_name}.xlsx".format(
                str_dir = str_dir, 
                str_file_name = str_file_name
            )
        )
        data = {
            "sheet_name": sheet_name,
            "password": password,
        }
        nas.upload_file(data, config.NAS_ROOT_PATH + "/{str_dir}/{str_file_name}.json".format(
                str_dir = str_dir, 
                str_file_name = str_file_name
            )
        )
        import requests
        str_dir_a = str_dir.split('-')
        DAG_ID = "dwh_pnl_daily"
        parameters = {"year_start": str_dir_a[0], 'month_start': str_dir_a[1], 'file_name': str_file_name} 
        result = requests.post(f"{config.AIRFLOW_API_ENDPOINT}/dags/{DAG_ID}/dag_runs", json={"conf": parameters})  
        return result.status_code
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="nas problem!")


@router.post("/qa-qc")
def upload_qa_qc( user = Depends(token_helper.get_current_user),):
    role_name = user.role_name
    check = False
    for item in role_name:
        if item == 'superuser' or item == 'qa-qc':
            check = True
            break
    if check == False:
        raise HTTPException(status_code=400, detail="permission denied!")
    return user