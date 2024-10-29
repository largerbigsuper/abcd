from typing import Optional

from app.core.crud import CRUDBase
from app.models.files import FileTag
from app.schemas.filetags import FileTagCreate, FileTagUpdate


class FileTagController(CRUDBase[FileTag, FileTagCreate, FileTagUpdate]):
    
    def __init__(self):
        super().__init__(model=FileTag)

    async def is_exist(self, name: str) -> bool:
        return await self.model.filter(name=name).exists()

file_tag_controller = FileTagController()
