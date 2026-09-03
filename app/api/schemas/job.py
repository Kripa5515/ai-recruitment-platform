from datetime import datetime
from pydantic import BaseModel, ConfigDict

class JobCreate(BaseModel):
    title: str
    description: str
    company: str
    location: str
    experience_required: str
    employment_type: str


class JobUpdate(BaseModel):
    title: str
    description: str
    company: str
    location: str
    experience_required: str
    employment_type: str
    status: str


class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    company: str
    location: str
    experience_required: str
    employment_type: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)