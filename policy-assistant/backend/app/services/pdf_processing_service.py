from uuid import uuid4

from langchain_community.document_loaders import PyPDFLoader
from app.core.config import get_settings
from app.core.app_logging import get_logger
from langchain_text_splitters import RecursiveCharacterTextSplitter
logger = get_logger(__name__)

class PDFProcessingService:
    """
    Handles pdf parcing and chuking
    """

    def __init__(self) -> None:
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=500,
        )

    def parse_and_chunk(self, file_path: str, document_name: str):
        """
        Parses pdf from uploaded path and creates chunks
        """
        logger.info("Parsing PDF", file_path=file_path)

        loader = PyPDFLoader(file_path)

        documents = loader.load()

        logger.info("PDF loaded", total_pages=len(documents))

        chunks = []

        for page_index, page in enumerate(documents):
            page_text = page.page_content

            if not page_text.strip():
                continue

            page_number = page_index + 1

            split_texts = self.text_splitter.split_text(page_text)

            logger.info("split_texts", totalsplit_texts=len(split_texts))

            for chunk_text in split_texts:
                chunk_id = str(uuid4())

                chunks.append(
                    {
                        "chunk_id": chunk_id,
                        "document_name": document_name,
                        "page_number": page_number,
                        "chunk_text": chunk_text.strip(),
                    }
                )

            logger.info("Chunking complete", total_chunks=len(chunks))

        return chunks
