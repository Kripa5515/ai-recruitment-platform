from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.api.schemas.resume import (
    ResumeResponse,
    ResumeUploadItem,
    ResumeUploadResponse,
)
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
    response_model=ResumeUploadResponse,
)
async def upload_resumes(
    files: Annotated[
        list[UploadFile],
        File(...),
    ],
    db: Session = Depends(get_db),
):
    service = ResumeService(db)

    items: list[ResumeUploadItem] = []

    successful = 0
    duplicates = 0
    failed = 0

    for file in files:
        filename = file.filename or "unknown"

        try:
            file_content = await file.read()

            candidate, resume, created = (
                service.process_resume_with_candidate(
                    filename=filename,
                    file_content=file_content,
                    content_type=file.content_type,
                )
            )

            if created:
                successful += 1

                items.append(
                    ResumeUploadItem(
                        filename=filename,
                        status="success",
                        message="Resume processed successfully.",
                        resume=resume,
                        candidate_id=(
                            candidate.id
                            if candidate is not None
                            else None
                        ),
                        candidate_name=(
                            candidate.name
                            if candidate is not None
                            else None
                        ),
                    )
                )

            else:
                duplicates += 1

                items.append(
                    ResumeUploadItem(
                        filename=filename,
                        status="duplicate",
                        message="Duplicate resume already exists.",
                        resume=resume,
                        candidate_id=(
                            candidate.id
                            if candidate is not None
                            else resume.candidate_id
                        ),
                        candidate_name=(
                            candidate.name
                            if candidate is not None
                            else None
                        ),
                    )
                )

        except FileValidationError as exc:
            failed += 1

            items.append(
                ResumeUploadItem(
                    filename=filename,
                    status="failed",
                    message=str(exc),
                )
            )

        except PDFExtractionError as exc:
            failed += 1

            items.append(
                ResumeUploadItem(
                    filename=filename,
                    status="failed",
                    message=str(exc),
                )
            )

        except DOCXExtractionError as exc:
            failed += 1

            items.append(
                ResumeUploadItem(
                    filename=filename,
                    status="failed",
                    message=str(exc),
                )
            )

        except Exception as exc:
            failed += 1

            items.append(
                ResumeUploadItem(
                    filename=filename,
                    status="failed",
                    message=f"Unexpected error: {exc}",
                )
            )

    return ResumeUploadResponse(
        total_files=len(files),
        successful=successful,
        duplicates=duplicates,
        failed=failed,
        items=items,
    )