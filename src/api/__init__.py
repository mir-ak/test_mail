from fastapi import APIRouter

from . import mail


router: APIRouter = APIRouter()
router.include_router(mail.router)