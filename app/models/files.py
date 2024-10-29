from tortoise import fields
from enum import Enum
from .base import BaseModel, TimestampMixin

class FileType(str, Enum):
    TEXT = "text"
    IMAGE = "image" 
    GIF = "gif"
    VIDEO = "video"

class FileTag(BaseModel):
    """标签模型"""
    name = fields.CharField(max_length=50, unique=True, description="标签名称")
    
    class Meta:
        table = "file_tag"

class FileInfo(BaseModel, TimestampMixin):
    """文件信息模型"""
    name = fields.CharField(max_length=255, description="文件名")
    content = fields.TextField(description="内容")
    file_type = fields.CharEnumField(FileType, description="文件类型")
    size = fields.IntField(description="文件大小(bytes)")
    duration = fields.IntField(null=True, description="视频/音频时长(秒)")
    width = fields.IntField(null=True, description="图片/视频宽度") 
    height = fields.IntField(null=True, description="图片/视频高度")
    path = fields.CharField(max_length=500, description="存储路径")
    mime_type = fields.CharField(max_length=100, description="MIME类型")
    user_id = fields.IntField(description="上传用户ID")
    tags = fields.ManyToManyField("models.FileTag", related_name="files", description="文件标签")
    
    class Meta:
        table = "file_info"

