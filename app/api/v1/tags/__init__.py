from fastapi import APIRouter

from .filetags import router

tags_router = APIRouter()
tags_router.include_router(router, tags=["文件标签"])

__all__ = ["tags_router"]
