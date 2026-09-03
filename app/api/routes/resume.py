from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.api.schemas.resume import ResumeResponse
from app.core.file_validation import FileValidationError
from app.services.exceptions import (
    DOCXExtractionError,
    DuplicateResumeError,
    PDFExtractionError,
)
from app.services.resume_service import ResumeService


router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"],
)


@router.post(
    "/upload",
    response_model=ResumeResponse,
)
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    service = ResumeService(db)

    try:
        file_content = file.file.read()

        resume = service.upload_resume(
            filename=file.filename or "unknown",
            content_type=file.content_type,
            file_content=file_content,
        )

        return resume

    except DuplicateResumeError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc

    except FileValidationError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except PDFExtractionError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except DOCXExtractionError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc