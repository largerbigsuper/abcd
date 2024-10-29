from fastapi import APIRouter, Depends, File, Query, UploadFile
from typing import List, Optional

from app.controllers.fileinfo import fileinfo_controller
from app.schemas import Success
from app.schemas.depts import *


router = APIRouter()


@router.get("/list", summary="查看文件列表")
async def list_files(
    name: str = Query(None, description="文件名称"),
):
    dept_tree = await fileinfo_controller.get_dept_tree(name)
    return Success(data=dept_tree)


@router.get("/get", summary="查看文件")
async def get_file(
    file_id: int = Query(..., description="文件ID"),
):
    file_obj = await fileinfo_controller.get(id=file_id)
    data = await file_obj.to_dict()
    return Success(data=data)


@router.post("/create", summary="创建文件")
async def create_file(
    dept_in: DeptCreate,
):
    await fileinfo_controller.create_dept(obj_in=dept_in)
    return Success(msg="Created Successfully")


@router.post("/update", summary="更新文件")
async def update_file(
    file: UploadFile = File(...),
    tags: Optional[str] = Query(None),
    current_user = Depends(get_current_user)
):
    file_obj = await fileinfo_controller.upload_file(file, tags, current_user.id)
    return Success(msg="Update Successfully")


@router.delete("/delete", summary="删除文件")
async def delete_file(
    file_id: int = Query(..., description="文件ID"),
):
    await fileinfo_controller.remove(id=file_id)
    return Success(msg="Deleted Success")
