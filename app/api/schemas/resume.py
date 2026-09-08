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
    candidate_id: int | None
    version: int | None
    is_current: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ResumeUploadItem(BaseModel):
    filename: str
    status: str
    message: str
    resume: ResumeResponse | None = None
    candidate_id: int | None = None
    candidate_name: str | None = None


class ResumeUploadResponse(BaseModel):
    total_files: int
    successful: int
    duplicates: int
    failed: int
    items: list[ResumeUploadItem]