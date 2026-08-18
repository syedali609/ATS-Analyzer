import io
from typing import Tuple
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
                
                # Simple column heuristic: check bounding boxes of lines on page
                try:
                    lines = page.extract_text_lines()
                    if lines:
                        width = page.width
                        midpoint = width / 2.0
                        
                        cross_midpoint = sum(1 for line in lines if line['x0'] < midpoint and line['x1'] > midpoint)
                        no_cross = sum(1 for line in lines if line['x1'] <= midpoint or line['x0'] >= midpoint)
                        
                        if no_cross > cross_midpoint:
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
