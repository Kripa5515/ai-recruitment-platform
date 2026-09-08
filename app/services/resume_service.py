from sqlalchemy.orm import Session

from app.core.file_hash import calculate_sha256
from app.core.file_validation import validate_resume_file
from app.core.storage import save_resume_file
from app.core.storage_filename import generate_storage_filename
from app.data.models.resume import Resume
from app.data.repositories.resume_repository import ResumeRepository
from app.services.candidate_service import CandidateService
from app.services.exceptions import (
    DOCXExtractionError,
    PDFExtractionError,
)
from app.services.resume_parser import (
    extract_docx_text,
    extract_pdf_text,
)


class ResumeService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ResumeRepository(db)
        self.candidate_service = CandidateService(db)

    # ------------------------------------------------------------------
    # Basic Resume Operations
    # ------------------------------------------------------------------

    def get_resume(self, resume_id: int) -> Resume | None:
        return self.repository.get_by_id(resume_id)

    def get_all_resumes(self) -> list[Resume]:
        return self.repository.get_all()

    def get_resume_by_hash(self, file_hash: str) -> Resume | None:
        return self.repository.get_by_hash(file_hash)

    def get_resume_versions(
        self,
        candidate_id: int,
    ) -> list[Resume]:
        return self.repository.get_resume_versions_by_candidate_id(
            candidate_id
        )

    def get_current_resume(
        self,
        candidate_id: int,
    ) -> Resume | None:
        return self.repository.get_current_resume_by_candidate_id(
            candidate_id
        )

    # ------------------------------------------------------------------
    # File Processing
    # ------------------------------------------------------------------

    def extract_resume_text(
        self,
        file_type: str,
        file_content: bytes,
    ) -> str:
        """
        Extract text from PDF or DOCX.

        PDF:
            Uses PyMuPDF.

        DOCX:
            Uses python-docx.
        """

        try:
            if file_type == "pdf":
                extracted_text = extract_pdf_text(
                    file_content
                )

            elif file_type == "docx":
                extracted_text = extract_docx_text(
                    file_content
                )

            else:
                raise ValueError(
                    f"Unsupported resume file type: {file_type}"
                )

        except PDFExtractionError:
            raise

        except DOCXExtractionError:
            raise

        except Exception as exc:
            if file_type == "pdf":
                raise PDFExtractionError(
                    f"Failed to extract text from PDF: {exc}"
                ) from exc

            if file_type == "docx":
                raise DOCXExtractionError(
                    f"Failed to extract text from DOCX: {exc}"
                ) from exc

            raise

        if not extracted_text or not extracted_text.strip():
            if file_type == "pdf":
                raise PDFExtractionError(
                    "PDF does not contain extractable text."
                )

            if file_type == "docx":
                raise DOCXExtractionError(
                    "DOCX does not contain extractable text."
                )

        return extracted_text.strip()

    # ------------------------------------------------------------------
    # Candidate Extraction
    # ------------------------------------------------------------------

    def extract_candidate_profile(
        self,
        resume_text: str,
    ):
        """
        Convert raw resume text into structured candidate data
        using CandidateService / LLM extraction.
        """

        return self.candidate_service.extract_profile(
            resume_text
        )

    # ------------------------------------------------------------------
    # Resume Creation
    # ------------------------------------------------------------------

    def create_versioned_resume(
        self,
        *,
        original_filename: str,
        file_type: str,
        file_size: int,
        file_hash: str,
        storage_path: str,
        extracted_text: str | None = None,
        source_type: str = "upload",
        source_reference: str | None = None,
        candidate_id: int | None = None,
    ) -> tuple[Resume, bool]:
        """
        Create a resume record with versioning.

        Returns:
            (resume, created)

        created=True:
            New resume was created.

        created=False:
            Exact duplicate already existed.
        """

        # --------------------------------------------------------------
        # Exact duplicate check
        # --------------------------------------------------------------

        existing_resume = self.repository.get_by_hash(
            file_hash
        )

        if existing_resume is not None:
            return existing_resume, False

        try:
            version = None

            # ----------------------------------------------------------
            # Candidate-specific versioning
            # ----------------------------------------------------------

            if candidate_id is not None:

                current_resume = (
                    self.repository
                    .get_current_resume_by_candidate_id(
                        candidate_id
                    )
                )

                # Mark old resume as historical BEFORE creating
                # the new current version.
                if current_resume is not None:
                    current_resume.is_current = False

                # Calculate next version number.
                version = (
                    self.repository
                    .get_next_version_by_candidate_id(
                        candidate_id
                    )
                )

            # ----------------------------------------------------------
            # Create new resume
            # ----------------------------------------------------------

            resume = self.repository.create(
                original_filename=original_filename,
                file_type=file_type,
                file_size=file_size,
                file_hash=file_hash,
                storage_path=storage_path,
                source_type=source_type,
                source_reference=source_reference,
                extracted_text=extracted_text,
                extraction_status="completed",
                candidate_id=candidate_id,
                version=version,
                is_current=True,
            )

            # ----------------------------------------------------------
            # Transaction
            # ----------------------------------------------------------

            self.db.commit()
            self.db.refresh(resume)

            return resume, True

        except Exception:
            self.db.rollback()
            raise

    # ------------------------------------------------------------------
    # File-Based Resume Processing
    # ------------------------------------------------------------------

    def get_or_create_resume_from_file(
        self,
        filename: str,
        file_content: bytes,
        candidate_id: int | None = None,
        content_type: str | None = None,
        source_type: str = "upload",
        source_reference: str | None = None,
    ) -> tuple[Resume, bool]:
        """
        Validate, process, store and persist a resume.

        Exact duplicate resumes are reused without running extraction
        again.
        """

        # --------------------------------------------------------------
        # Validate file
        # --------------------------------------------------------------

        file_type = validate_resume_file(
            filename=filename,
            file_content=file_content,
            content_type=content_type,
        )

        # --------------------------------------------------------------
        # Calculate file hash
        # --------------------------------------------------------------

        file_hash = calculate_sha256(
            file_content
        )

        # --------------------------------------------------------------
        # Duplicate check BEFORE extraction
        #
        # This is important because duplicate files should not cause
        # another PDF/DOCX extraction or LLM call.
        # --------------------------------------------------------------

        existing_resume = self.repository.get_by_hash(
            file_hash
        )

        if existing_resume is not None:
            return existing_resume, False

        # --------------------------------------------------------------
        # Extract text
        # --------------------------------------------------------------

        extracted_text = self.extract_resume_text(
            file_type=file_type,
            file_content=file_content,
        )

        # --------------------------------------------------------------
        # Generate safe storage filename
        # --------------------------------------------------------------

        storage_filename = generate_storage_filename(
            file_type=file_type,
            file_hash=file_hash,
        )

        # --------------------------------------------------------------
        # Save physical file
        # --------------------------------------------------------------

        saved_file_path = save_resume_file(
            filename=storage_filename,
            file_content=file_content,
        )

        try:

            # ----------------------------------------------------------
            # Create resume record
            # ----------------------------------------------------------

            resume, created = self.create_versioned_resume(
                original_filename=filename,
                file_type=file_type,
                file_size=len(file_content),
                file_hash=file_hash,
                storage_path=str(saved_file_path),
                extracted_text=extracted_text,
                source_type=source_type,
                source_reference=source_reference,
                candidate_id=candidate_id,
            )

            return resume, created

        except Exception:

            # ----------------------------------------------------------
            # DB failed after physical file was saved.
            #
            # Remove orphan file from storage.
            # ----------------------------------------------------------

            saved_file_path.unlink(
                missing_ok=True
            )

            raise

    get_or_create_versioned_resume_from_file = get_or_create_resume_from_file

    def ingest_resume_folder(
        self,
        folder_path,
    ) -> list[Resume]:
        """
        Scan a folder and ingest all supported resume files.
        """
        from app.integrations.resume_folder_scanner import scan_resume_folder

        resume_files = scan_resume_folder(folder_path)
        resumes = []

        for file_path in resume_files:
            file_content = file_path.read_bytes()

            resume, _ = self.get_or_create_resume_from_file(
                filename=file_path.name,
                file_content=file_content,
                source_type="folder",
                source_reference=str(file_path),
            )
            resumes.append(resume)

        return resumes

    # ------------------------------------------------------------------
    # Resume + Candidate Processing
    # ------------------------------------------------------------------

    def process_resume_with_candidate(
        self,
        filename: str,
        file_content: bytes,
        content_type: str | None = None,
        source_type: str = "upload",
        source_reference: str | None = None,
    ) -> tuple:
        """
        Complete resume processing pipeline.

        Flow:

            File
              ↓
            Validation
              ↓
            SHA-256
              ↓
            Duplicate Check
              ↓
            PDF/DOCX Text Extraction
              ↓
            Candidate Profile Extraction
              ↓
            Candidate Create/Reuse
              ↓
            Resume Versioning
              ↓
            PostgreSQL
        """

        # --------------------------------------------------------------
        # Validate file
        # --------------------------------------------------------------

        file_type = validate_resume_file(
            filename=filename,
            file_content=file_content,
            content_type=content_type,
        )

        # --------------------------------------------------------------
        # Hash file
        # --------------------------------------------------------------

        file_hash = calculate_sha256(
            file_content
        )

        # --------------------------------------------------------------
        # Duplicate check BEFORE any expensive processing
        # --------------------------------------------------------------

        existing_resume = self.repository.get_by_hash(
            file_hash
        )

        if existing_resume is not None:

            candidate = None

            if existing_resume.candidate_id is not None:
                candidate = (
                    self.candidate_service
                    .get_candidate(
                        existing_resume.candidate_id
                    )
                )

            return (
                candidate,
                existing_resume,
                False,
            )

        # --------------------------------------------------------------
        # Extract PDF / DOCX text
        # --------------------------------------------------------------

        extracted_text = self.extract_resume_text(
            file_type=file_type,
            file_content=file_content,
        )

        # --------------------------------------------------------------
        # Extract structured candidate profile
        # --------------------------------------------------------------

        profile = self.extract_candidate_profile(
            extracted_text
        )

        # --------------------------------------------------------------
        # Generate storage filename
        # --------------------------------------------------------------

        storage_filename = generate_storage_filename(
            file_type=file_type,
            file_hash=file_hash,
        )

        # --------------------------------------------------------------
        # Save physical file
        # --------------------------------------------------------------

        saved_file_path = save_resume_file(
            filename=storage_filename,
            file_content=file_content,
        )

        try:

            # ----------------------------------------------------------
            # Get existing candidate or create new candidate.
            #
            # This operation does NOT commit.
            # The complete transaction is controlled below.
            # ----------------------------------------------------------

            (
                candidate,
                candidate_created,
            ) = (
                self.candidate_service
                .get_or_create_candidate_profile_without_commit(
                    profile
                )
            )

            # ----------------------------------------------------------
            # Find current resume
            # ----------------------------------------------------------

            current_resume = (
                self.repository
                .get_current_resume_by_candidate_id(
                    candidate.id
                )
            )

            # ----------------------------------------------------------
            # Mark old resume as historical
            # ----------------------------------------------------------

            if current_resume is not None:
                current_resume.is_current = False

            # ----------------------------------------------------------
            # Calculate next version
            # ----------------------------------------------------------

            version = (
                self.repository
                .get_next_version_by_candidate_id(
                    candidate.id
                )
            )

            # ----------------------------------------------------------
            # Create new resume
            # ----------------------------------------------------------

            resume = self.repository.create(
                original_filename=filename,
                file_type=file_type,
                file_size=len(file_content),
                file_hash=file_hash,
                storage_path=str(saved_file_path),
                source_type=source_type,
                source_reference=source_reference,
                extracted_text=extracted_text,
                extraction_status="completed",
                candidate_id=candidate.id,
                version=version,
                is_current=True,
            )

            # ----------------------------------------------------------
            # Commit complete transaction
            #
            # Candidate + profile details + resume are persisted
            # together.
            # ----------------------------------------------------------

            self.db.commit()

            # ----------------------------------------------------------
            # Refresh ORM objects
            # ----------------------------------------------------------

            self.db.refresh(candidate)
            self.db.refresh(resume)

            return (
                candidate,
                resume,
                True,
            )

        except Exception:

            # ----------------------------------------------------------
            # Rollback DB transaction
            # ----------------------------------------------------------

            self.db.rollback()

            # ----------------------------------------------------------
            # Remove physical file if DB processing failed
            # ----------------------------------------------------------

            saved_file_path.unlink(
                missing_ok=True
            )

            raise

    # ------------------------------------------------------------------
    # Candidate + Resume Helper
    # ------------------------------------------------------------------

    def create_candidate_and_resume(
        self,
        profile,
        original_filename: str,
        file_type: str,
        file_size: int,
        file_hash: str,
        storage_path: str,
        extracted_text: str,
        source_type: str = "upload",
        source_reference: str | None = None,
    ) -> tuple:
        """
        Create/reuse candidate and create a versioned resume
        in a single transaction.

        This helper is kept for service-level usage.
        """

        try:

            # ----------------------------------------------------------
            # Get existing candidate or create candidate profile
            # ----------------------------------------------------------

            (
                candidate,
                candidate_created,
            ) = (
                self.candidate_service
                .get_or_create_candidate_profile_without_commit(
                    profile
                )
            )

            # ----------------------------------------------------------
            # Mark previous current resume as historical BEFORE
            # creating the new version.
            # ----------------------------------------------------------

            current_resume = (
                self.repository
                .get_current_resume_by_candidate_id(
                    candidate.id
                )
            )

            if current_resume is not None:
                current_resume.is_current = False

            # ----------------------------------------------------------
            # Next version
            # ----------------------------------------------------------

            version = (
                self.repository
                .get_next_version_by_candidate_id(
                    candidate.id
                )
            )

            # ----------------------------------------------------------
            # Create resume
            # ----------------------------------------------------------

            resume = self.repository.create(
                original_filename=original_filename,
                file_type=file_type,
                file_size=file_size,
                file_hash=file_hash,
                storage_path=storage_path,
                source_type=source_type,
                source_reference=source_reference,
                extracted_text=extracted_text,
                extraction_status="completed",
                candidate_id=candidate.id,
                version=version,
                is_current=True,
            )

            # ----------------------------------------------------------
            # Commit
            # ----------------------------------------------------------

            self.db.commit()

            self.db.refresh(candidate)
            self.db.refresh(resume)

            return (
                candidate,
                resume,
            )

        except Exception:

            self.db.rollback()
            raise