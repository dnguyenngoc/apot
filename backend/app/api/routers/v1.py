from fastapi import APIRouter

from api.resources.v1 import account, ocr

router = APIRouter()


router.include_router(account.router, prefix="/account",  tags=["V1-Account"])
router.include_router(ocr.router, prefix="/ocr",  tags=["V1-OCR"])
