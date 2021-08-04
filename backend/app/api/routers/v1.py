from fastapi import APIRouter

from api.resources.v1 import account, operation

router = APIRouter()


router.include_router(account.router, prefix="/account",  tags=["V1-Account"])
router.include_router(operation.router, prefix="/operation",  tags=["V1-Operation"])