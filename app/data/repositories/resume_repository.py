from sqlalchemy import select, func
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
    candidate_id: int | None = None,
    version: int | None = None,
    is_current: bool = True,
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
            candidate_id=candidate_id,
            version=version,
            is_current=is_current,
        )

        self.db.add(resume)
        self.db.flush()

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

    def get_by_storage_path(
        self,
        storage_path: str,
    ) -> Resume | None:
        statement = select(Resume).where(
            Resume.storage_path == storage_path
        )

        result = self.db.execute(statement)

        return result.scalar_one_or_none()

    def get_by_source_reference(
    self,
    source_type: str,
    source_reference: str,
    ) -> Resume | None:
        statement = select(Resume).where(
            Resume.source_type == source_type,
            Resume.source_reference == source_reference,
        )

        result = self.db.execute(statement)

        return result.scalar_one_or_none()

    def get_by_candidate_id(
    self,
    candidate_id: int,
    ) -> list[Resume]:
        statement = select(Resume).where(
            Resume.candidate_id == candidate_id
        ).order_by(Resume.id)

        result = self.db.execute(statement)

        return list(result.scalars().all())

    def get_current_resume_by_candidate_id(
    self,
    candidate_id: int,
    ):
        statement = (
            select(Resume)
            .where(
                Resume.candidate_id == candidate_id,
                Resume.is_current.is_(True),
            )
            .order_by(Resume.version.desc())
        )

        return self.db.scalar(statement)


    def get_latest_version_by_candidate_id(
        self,
        candidate_id: int,
    ) -> int:
        statement = select(
            func.max(Resume.version)
        ).where(
            Resume.candidate_id == candidate_id,
        )

        latest_version = self.db.scalar(statement)

        return latest_version or 0


    def get_next_version_by_candidate_id(
        self,
        candidate_id: int,
    ) -> int:
        latest_version = self.get_latest_version_by_candidate_id(
            candidate_id
        )

        return latest_version + 1


    def get_resume_versions_by_candidate_id(
        self,
        candidate_id: int,
    ):
        statement = (
            select(Resume)
            .where(
                Resume.candidate_id == candidate_id,
            )
            .order_by(Resume.version.desc())
        )

        return list(self.db.scalars(statement).all())