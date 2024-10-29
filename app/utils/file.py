import io
import os
import magic
import cv2
from PIL import Image
from app.models.files import FileType

def get_file_info(content: bytes, filename: str) -> dict:
    """获取文件信息"""
    # 获取MIME类型
    mime_type = magic.from_buffer(content, mime=True)
    
    info = {
        "size": len(content),
        "mime_type": mime_type
    }
    
    # 根据MIME类型判断文件类型
    if mime_type.startswith('text/'):
        info["file_type"] = FileType.TEXT
    elif mime_type.startswith('image/'):
        if mime_type == 'image/gif':
            info["file_type"] = FileType.GIF
        else:
            info["file_type"] = FileType.IMAGE
            # 获取图片尺寸
            img = Image.open(io.BytesIO(content))
            info["width"], info["height"] = img.size
    elif mime_type.startswith('video/'):
        info["file_type"] = FileType.VIDEO
        # 获取视频信息
        temp_path = f"/tmp/{filename}"
        with open(temp_path, "wb") as f:
            f.write(content)
        cap = cv2.VideoCapture(temp_path)
        info["width"] = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        info["height"] = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        info["duration"] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS))
        cap.release()
        os.remove(temp_path)
    
    return info
