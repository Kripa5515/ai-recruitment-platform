from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.models.resume import Resume

class ResumeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
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
        resume = Resume(
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

        self.db.add(resume)
        self.db.commit()
        self.db.refresh(resume)

        return resume

    def get_by_id(self, resume_id: int) -> Resume | None:
        statement = select(Resume).where(Resume.id == resume_id)
        result = self.db.execute(statement)
        return result.scalar_one_or_none()

    def get_by_hash(self, file_hash: str) -> Resume | None:
        statement = select(Resume).where(
            Resume.file_hash == file_hash
        )
        result = self.db.execute(statement)
        return result.scalar_one_or_none()

    def get_all(self) -> list[Resume]:
        statement = select(Resume).order_by(Resume.id)
        result = self.db.execute(statement)
        return list(result.scalars().all())