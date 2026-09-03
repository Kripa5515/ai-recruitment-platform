from datetime import datetime
from pydantic import BaseModel, ConfigDict

class JobCreate(BaseModel):
    title:str
    description:str

class JobUpdate(BaseModel):
    title: str
    description: str
    
class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)