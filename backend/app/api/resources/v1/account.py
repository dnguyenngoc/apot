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

router = APIRouter()


@router.post("/login/access-token", response_model = account_entity.Token)
def login( 
    db_session: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)
):
    is_user_ldap = ldap.is_user_ldap(form_data.username, form_data.password)
    if is_user_ldap == False:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    now = time_helper.now_utc()
    role = user_logic.get_user_role_by_name(db_session, form_data.username)
    role_id = []
    role_name = []
    if role:       
        for item in role:
            role_id.append(item.role_id)
            role_name.append(item.role_name)

    token_create = account_entity.TokenCreate(
        user_name= form_data.username,
        password= form_data.password,
        role_id= role_id,
        role_name=role_name,
    )
    access_token = token_helper.create_access_token(token_create.__dict__)
    refresh_token = token_helper.create_fresh_token(token_create.__dict__)
    token = account_entity.Token(
        access_token = access_token, 
        refresh_token = refresh_token,
        expire_token= now + timedelta(days=3),
        expire_refresh_token= now + timedelta(days = 7),
        role_name =role_name
    )
    return token


@router.post("/login/refresh-token", response_model = account_entity.Token)
def refresh_token( 
    *, 
    db_session: Session = Depends(get_db),
    refresh_token: str = Form(...),
):
    token = token_helper.decrypt_renew(refresh_token)
    if token == False:
        raise HTTPException(status_code=403, detail="token wrong")
    is_user_ldap = ldap.is_user_ldap(token['user_name'], token['password'])
    if is_user_ldap == False:
        raise HTTPException(status_code=400, detail="token wrong")
    now = time_helper.now_utc()
    role = user_logic.get_user_role_by_name(db_session, token['user_name'])
    role_id = []
    role_name = []
    if role:       
        for item in role:
            role_id.append(item.role_id)
            role_name.append(item.role_name)

    token_create = account_entity.TokenCreate(
        user_name= token['user_name'],
        password= token['password'],
        role_id= role_id,
        role_name=role_name,
    )
    access_token = token_helper.create_access_token(token_create.__dict__)
    refresh_token = token_helper.create_fresh_token(token_create.__dict__)
    token = account_entity.Token(
        access_token = access_token, 
        refresh_token = refresh_token,
        expire_token= now + timedelta(days=3),
        expire_refresh_token= now + timedelta(days = 7),
        role_name =role_name
    )
    return token



@router.get("/role/role-name")
def verify_role_user( 
    *,
    user = Depends(token_helper.get_current_user),
):
    return user.role_name


# @router.post("/login/check-token")
# def check_token(
#     *, 
#     db_session: Session = Depends(get_db),
#     token: str = Form(...),
# ):
#     token = token_helper.decrypt(token)
#     if token == False:
#         raise HTTPException(status_code=400, detail="token expire")
#     user_db = token_helper.get_current_user(db_session, token)
#     return {"status": "good!"}
    

# @router.post("/login/refresh-token", response_model = account_entity.Token)
# def refresh_token( 
#     *, 
#     db_session: Session = Depends(get_db),
#     refresh_token: str = Form(...),
# ):
#     token = token_helper.decrypt(refresh_token)
#     if token == False:
#         raise HTTPException(status_code=403, detail="token wrong")
#     user_db = token_helper.get_current_user(db_session, token)
#     now = time_helper.now_utc()
#     token_create = account_entity.TokenCreate(**user_db.__dict__, role_name = user_db.role.name, user_id = user_db.id)
#     access_token = token_helper.create_access_token(token_create.__dict__)
#     refresh_token = token_helper.create_fresh_token(token_create.__dict__)
#     token = account_entity.Token(
#         access_token = access_token, 
#         refresh_token = refresh_token,
#         expire_token= now + timedelta(days=3),
#         expire_refresh_token= now + timedelta(days = 7)
#     )
#     return token

# @router.put('/change-password')
# def change_password(
#     user = Depends(token_helper.get_current_user),
# ):
#     pass



# @router.post("/login/access-token", response_model = account_entity.Token)
# def login( 
#     db_session: Session = Depends(get_db),
#     form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)
# ):
#     user_db = user_logic.get_user_by_email_and_password_join_role(db_session, form_data.username, form_data.password)
#     if not user_db:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     now = time_helper.now_utc()
#     token_create = account_entity.TokenCreate(**user_db.__dict__, role_name = user_db.role.name, user_id = user_db.id)
#     access_token = token_helper.create_access_token(token_create.__dict__)
#     refresh_token = token_helper.create_fresh_token(token_create.__dict__)
#     token = account_entity.Token(
#         access_token = access_token, 
#         refresh_token = refresh_token,
#         expire_token= now + timedelta(days=3),
#         expire_refresh_token= now + timedelta(days = 7
#         )
#     )
#     return token