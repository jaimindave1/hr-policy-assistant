from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile

from app.core.config import get_settings
from app.core.app_logging import get_logger
from app.services.pdf_processing_service import PDFProcessingService
from app.services.embedding_service import EmbeddingService
from app.repositories.document_repository import DocumentRepository


logger = get_logger(__name__)

class DocumentService:
    """
    Handles document upload and storage
    """    

    def __init__(self) -> None:
        self.settings = get_settings()
        self.pdf_processor = PDFProcessingService()
        self.embedding_service = EmbeddingService()
        self.repository = DocumentRepository()


    async def save_upload(self, file: UploadFile) -> dict:
        """
        Saves uploaded PDF to local storage.
        """

        upload_dir = self.settings.upload_dir

        file_id = str(uuid4())
        safe_name = file.filename.replace(" ", "_")

        file_name = f"{file_id}_{safe_name}"
        file_path = upload_dir / file_name

        logger.info("Saving uploaded file", file_name=file_name)

        contents = await file.read()

        with open(file_path, "wb") as f:
            f.write(contents)

        
        chunks = self.pdf_processor.parse_and_chunk(
            file_path=str(file_path),
            document_name=file.filename,
        )

        enriched_chunks = self.embedding_service.embed_chunks(chunks)

        self.repository.save_chunks(enriched_chunks)

        return {
            "file_id": file_id,
            "file_name": file.filename,
            "stored_name": file_name,
            "total_chunks": len(chunks),
        }


