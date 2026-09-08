from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.api.schemas.resume import ResumeResponse
from app.services.exceptions import DuplicateResumeError
from app.services.resume_service import ResumeService


router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"],
)


@router.post(
    "/",
    response_model=ResumeResponse,
)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    file_content = await file.read()

    service = ResumeService(db)

    try:
        resume = service.upload_resume(
            filename=file.filename or "resume",
            content_type=file.content_type,
            file_content=file_content,
        )

        return resume

    except DuplicateResumeError:
        raise