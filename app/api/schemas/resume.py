from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ResumeResponse(BaseModel):
    id: int
    original_filename: str
    file_type: str
    file_size: int
    file_hash: str
    storage_path: str
    source_type: str
    source_reference: str | None
    extracted_text: str | None
    extraction_status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)