from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class FileType(str, Enum):
    TEXT = "text"
    IMAGE = "image" 
    GIF = "gif"
    VIDEO = "video"

# 文件相关Schema
class FileInfoBase(BaseModel):
    name: str = Field(..., max_length=255, description="文件名")
    file_type: FileType = Field(..., description="文件类型")
    size: int = Field(..., description="文件大小(bytes)")
    mime_type: str = Field(..., max_length=100, description="MIME类型")

class FileInfoCreate(FileInfoBase):
    duration: Optional[int] = Field(None, description="视频/音频时长(秒)")
    width: Optional[int] = Field(None, description="图片/视频宽度")
    height: Optional[int] = Field(None, description="图片/视频高度")
    path: str = Field(..., max_length=500, description="存储路径")
    user_id: int = Field(..., description="上传用户ID")

class FileInfoUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    file_type: Optional[FileType] = None

class FileInfoOut(FileInfoBase):
    id: int
    duration: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    tags: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# 查询参数Schema
class FileInfoQuery(BaseModel):
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(10, ge=1, le=100, description="每页数量")
    file_type: Optional[FileType] = Field(None, description="文件类型")
    tags: Optional[List[str]] = Field(None, description="标签列表")
    keyword: Optional[str] = Field(None, description="关键词")

# 文件标签操作Schema
class FileTagCreate(BaseModel):
    tags: List[str] = Field(..., description="标签名称列表")

class FileTagDelete(BaseModel):
    tag_id: int = Field(..., description="标签ID")

# 批量操作Schema
class BatchFileIds(BaseModel):
    file_ids: List[int] = Field(..., description="文件ID列表")

# 响应Schema
class FileListOut(BaseModel):
    total: int
    items: List[FileInfoOut]
