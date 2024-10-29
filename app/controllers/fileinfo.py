import os
import time
from fastapi import File, HTTPException, UploadFile
from app.core.crud import CRUDBase
from app.settings import settings
from app.models.files import FileInfo, FileTag
from app.schemas.fileinfo import FileInfoCreate, FileInfoUpdate
from app.utils.file import get_file_info

if not os.path.exists(settings.UPLOAD_DIR):
    os.makedirs(settings.UPLOAD_DIR)

class FileInfoController(CRUDBase[FileInfo, FileInfoCreate, FileInfoUpdate]):

    def __init__(self):
        super().__init__(model=FileInfo)


    async def upload_file(self, file: UploadFile, tags: str, user_id: int):
        """
        上传单个文件
        """
        try:
            # 读取文件内容
            content = await file.read()
            
            # 获取文件信息
            file_info = get_file_info(content, file.filename)
            
            # 确保上传目录存在
            os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
            
            # 生成文件存储路径
            file_path = os.path.join(
                settings.UPLOAD_DIR, 
                f"{int(time.time())}_{file.filename}"
            )
            
            # 保存文件
            with open(file_path, 'wb') as f:
                f.write(content)
            
            # 创建文件记录
            file_obj = await FileInfo.create(
                name=file.filename,
                file_type=file_info["file_type"],
                size=file_info["size"],
                duration=file_info.get("duration"),
                width=file_info.get("width"),
                height=file_info.get("height"),
                path=file_path,
                mime_type=file_info["mime_type"],
                user_id=user_id
            )
            
            # 处理标签
            if tags:
                for tag_name in tags:
                    tag, _ = await FileTag.get_or_create(name=tag_name)
                    await file_obj.tags.add(tag)
            
            # 预加载tags关系
            await file_obj.fetch_related("tags")
            return file_obj
            
        except Exception as e:
            # 清理已上传的文件
            if 'file_path' in locals() and os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(status_code=400, detail=f"文件上传失败: {str(e)}")


fileinfo_controller = FileInfoController()
