from fastapi import UploadFile, HTTPException, status

from app.core.config import get_settings

def validate_pdf_files(file: UploadFile)->None:
    """
    Validates uploaded file.
    """
    settings = get_settings()


    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must have a name.",
        )
    

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed.",
        )
    

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file content type.",
        )
    

    if file.size and file.size > settings.max_upload_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File must be less than {settings.max_upload_size_mb}MB.",
        )



