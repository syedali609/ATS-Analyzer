import io
from typing import Dict, Any, Tuple
import pdfplumber
from fastapi import HTTPException

def parse_pdf(file_bytes: bytes) -> Tuple[str, bool, bool]:
    """
    Parses PDF file bytes using pdfplumber.
    Returns:
        (extracted_text, has_tables, is_single_column)
    """
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded PDF file is empty.")
    
    extracted_text_pages = []
    has_tables = False
    is_single_column = True
    
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            if not pdf.pages:
                raise HTTPException(status_code=400, detail="PDF contains no pages.")
            
            for page in pdf.pages:
                # Extract text
                page_text = page.extract_text() or ""
                extracted_text_pages.append(page_text)
                
                # Check for tables
                tables = page.extract_tables()
                if tables and len(tables) > 0:
                    has_tables = True
                
                # Simple column heuristic: check bounding boxes of words on page
                try:
                    words = page.extract_words()
                    if words:
                        width = page.width
                        midpoint = width / 2.0
                        
                        # Count words starting strictly on left vs right half in middle y-ranges
                        left_words = sum(1 for w in words if w['x1'] < midpoint - 15)
                        right_words = sum(1 for w in words if w['x0'] > midpoint + 15)
                        
                        # If significant words exist separately in both left and right columns
                        if left_words > 25 and right_words > 25:
                            is_single_column = False
                except Exception:
                    pass
                    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Could not parse PDF file. Ensure it is a valid document. Error: {str(e)}"
        )
    
    full_text = "\n\n".join(extracted_text_pages).strip()
    if not full_text:
        raise HTTPException(
            status_code=400,
            detail="No readable text could be extracted from the PDF. It may be scanned or image-based."
        )
    
    return full_text, has_tables, is_single_column
