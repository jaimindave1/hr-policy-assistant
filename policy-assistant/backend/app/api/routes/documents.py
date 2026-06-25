from fastapi import APIRouter,UploadFile, File, HTTPException,status
from app.models.schemas import HealthResponse
from app.core.config import get_settings
from app.utils.file_validation import validate_pdf_files
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["documents"])
document_service = DocumentService()

@router.get("")
def list_documents() -> dict[str, list[str]]:
    return {"documents": []}

@router.post("/upload")
async def upload_documents(file: UploadFile = File(...)) -> dict:
    """
    Upload a policy PDF document.
    """

    try:
        validate_pdf_files(file)

        result = await document_service.save_upload(file)

        return {
            "message": "File uploaded successfully",
            "document": result,
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error while uploading file {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload document.",
        )
