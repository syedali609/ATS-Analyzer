from typing import Tuple, Optional
from fastapi import HTTPException, UploadFile
from app.parsers.pdf_parser import parse_pdf
from app.parsers.docx_parser import parse_docx
from app.core.config import settings

async def extract_resume_content(
    file: Optional[UploadFile] = None,
    raw_text: Optional[str] = None
) -> Tuple[str, str, bool, bool]:
    """
    Dispatcher function to extract text from an uploaded file or raw text string.
    Returns:
        (text, file_type, has_tables, is_single_column)
    """
    if raw_text and raw_text.strip():
        text = raw_text.strip()
        if len(text.split()) < 10:
            raise HTTPException(
                status_code=400,
                detail="Provided resume text is too short (minimum 10 words required)."
            )
        return text, "txt", False, True
    
    if not file:
        raise HTTPException(
            status_code=400,
            detail="Please upload a resume file (.pdf, .docx, .txt) or provide resume text."
        )
    
    filename = file.filename or "resume.txt"
    ext = "." + filename.split(".")[-1].lower() if "." in filename else ".txt"
    
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format '{ext}'. Allowed formats: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    contents = await file.read()
    if len(contents) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum limit of {settings.MAX_FILE_SIZE_MB}MB."
        )
    
    if ext == ".pdf":
        text, has_tables, is_single_column = parse_pdf(contents)
    elif ext == ".docx":
        text, has_tables, is_single_column = parse_docx(contents)
    elif ext == ".txt":
        try:
            text = contents.decode("utf-8", errors="ignore").strip()
        except Exception:
            raise HTTPException(status_code=400, detail="Could not read text file.")
        if not text:
            raise HTTPException(status_code=400, detail="Uploaded text file is empty.")
        has_tables = False
        is_single_column = True
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported file extension '{ext}'")

    if len(text.split()) < 10:
        raise HTTPException(
            status_code=400,
            detail="Provided resume text is too short (minimum 10 words required)."
        )

    return text, ext[1:], has_tables, is_single_column
