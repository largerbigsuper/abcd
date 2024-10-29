from pydantic import BaseModel, Field

class FileTagBase(BaseModel):
    name: str = Field(..., max_length=50, description="标签名称")

class FileTagCreate(FileTagBase):
    pass

class FileTagUpdate(FileTagBase):
    id: int

class FileTagOut(FileTagBase):
    id: int
    
    class Config:
        from_attributes = True
