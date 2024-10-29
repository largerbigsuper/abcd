from fastapi import APIRouter

from .fileinfo import router

fileinfo_router = APIRouter()
fileinfo_router.include_router(router, tags=["文件"])

__all__ = ["fileinfo_router"]
