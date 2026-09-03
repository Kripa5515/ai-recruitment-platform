from sqlalchemy.orm import Session

from app.ai.extraction.pdf_extractor import extract_pdf_text
from app.ai.extraction.docx_extractor import extract_docx_text
from app.core.file_hash import calculate_sha256
from app.core.file_validation import validate_resume_file
from app.core.storage import save_resume_file
from app.core.storage_filename import generate_storage_filename
from app.data.models.resume import Resume
from app.data.repositories.resume_repository import ResumeRepository
from app.services.exceptions import DuplicateResumeError


class ResumeService:
    def __init__(self, db: Session):
        self.repository = ResumeRepository(db)

    def create_resume(
        self,
        original_filename: str,
        file_type: str,
        file_size: int,
        file_hash: str,
        storage_path: str,
        source_type: str = "upload",
        source_reference: str | None = None,
        extracted_text: str | None = None,
        extraction_status: str = "uploaded",
    ) -> Resume:
        existing_resume = self.repository.get_by_hash(file_hash)

        if existing_resume is not None:
            raise DuplicateResumeError(
                "A resume with the same file already exists."
            )

        return self.repository.create(
            original_filename=original_filename,
            file_type=file_type,
            file_size=file_size,
            file_hash=file_hash,
            storage_path=storage_path,
            source_type=source_type,
            source_reference=source_reference,
            extracted_text=extracted_text,
            extraction_status=extraction_status,
        )

    def get_resume(self, resume_id: int) -> Resume | None:
        return self.repository.get_by_id(resume_id)

    def get_resume_by_hash(self, file_hash: str) -> Resume | None:
        return self.repository.get_by_hash(file_hash)

    def get_all_resumes(self) -> list[Resume]:
        return self.repository.get_all()

    def upload_resume(
        self,
        filename: str,
        content_type: str | None,
        file_content: bytes,
    ) -> Resume:
        file_type = validate_resume_file(
            filename=filename,
            content_type=content_type,
            file_content=file_content,
        )

        file_hash = calculate_sha256(file_content)

        existing_resume = self.repository.get_by_hash(file_hash)

        if existing_resume is not None:
            raise DuplicateResumeError(
                "A resume with the same file already exists."
            )

        # Extract resume text based on file type
        if file_type == "pdf":
            extracted_text = extract_pdf_text(file_content)

        elif file_type == "docx":
            extracted_text = extract_docx_text(file_content)

        else:
            extracted_text = ""

        storage_filename = generate_storage_filename(
            file_type=file_type,
            file_hash=file_hash,
        )

        saved_file_path = save_resume_file(
            filename=storage_filename,
            file_content=file_content,
        )

        try:
            resume = self.repository.create(
                original_filename=filename,
                file_type=file_type,
                file_size=len(file_content),
                file_hash=file_hash,
                storage_path=str(saved_file_path),
                source_type="upload",
                extracted_text=extracted_text,
                extraction_status="completed",
            )

            return resume

        except Exception:
            saved_file_path.unlink(missing_ok=True)
            raise