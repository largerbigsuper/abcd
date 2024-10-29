from fastapi import APIRouter, Query
from tortoise.expressions import Q

from app.controllers.filetags import file_tag_controller
from app.schemas import Success
from app.schemas.base import Fail, SuccessExtra
from app.schemas.filetags import FileTagCreate, FileTagUpdate

router = APIRouter()


@router.get("/list", summary="查看标签列表")
async def list_tags(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    name: str = Query("", description="名称，用于搜索"),
):
    q = Q()
    if name:
        q &= Q(name__contains=name)

    total, tag_objs = await file_tag_controller.list(page=page, page_size=page_size, search=q)
    data = [await obj.to_dict() for obj in tag_objs]
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/get", summary="查看标签")
async def get_tag(
    tag_id: int = Query(..., description="标签ID"),
):
    tag_obj = await file_tag_controller.get(id=tag_id)
    return Success(data=await tag_obj.to_dict())


@router.post("/create", summary="创建标签")
async def create_tag(
    tag_in: FileTagCreate,
):
    is_exist = await file_tag_controller.is_exist(tag_in.name)
    if is_exist:
        return Fail(code=400, msg="tag allready existed !")
    new_tag = await file_tag_controller.create(obj_in=tag_in)
    return Success(msg="Created Successfully")


@router.post("/update", summary="更新标签")
async def update_tag(
    tag_in: FileTagUpdate,
):
    tag = await file_tag_controller.update(id=tag_in.id, obj_in=tag_in)
    return Success(msg="Updated Successfully")


@router.delete("/delete", summary="删除标签")
async def delete_tag(
    tag_id: int = Query(..., description="标签ID"),
):
    await file_tag_controller.remove(id=tag_id)
    return Success(msg="Deleted Successfully")
