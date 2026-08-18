from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body
from app.models.schemas import AnalysisResponse, HealthCheck
from app.parsers.base_parser import extract_resume_content
from app.analysis.keyword_matcher import match_keywords
from app.analysis.formatting_checks import evaluate_formatting
from app.analysis.scorer import calculate_overall_score

router = APIRouter()

@router.get("/health", response_model=HealthCheck, summary="Health Check Endpoint")
async def health_check():
    """Verify backend API service status."""
    return HealthCheck(status="ok", version="1.0.0")

@router.post("/analyze", response_model=AnalysisResponse, summary="Analyze Resume against Job Description")
async def analyze_resume(
    file: Optional[UploadFile] = File(None),
    job_description: Optional[str] = Form(None),
    resume_text: Optional[str] = Form(None)
):
    """
    Main endpoint for analyzing a resume against a job description.
    Supports either file upload (PDF/DOCX/TXT) or raw plain text.
    """
    jd_input = job_description
    res_input = resume_text
            
    if not jd_input or not jd_input.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description is required for ATS matching analysis."
        )
        
    # Extract text content from file or plain text string
    extracted_text, file_type, has_tables, is_single_column = await extract_resume_content(
        file=file,
        raw_text=res_input
    )
    
    # Run Keyword TF-IDF analysis & Cosine Similarity
    keyword_analysis = match_keywords(extracted_text, jd_input)
    
    # Run Formatting & Structure audit
    formatting_analysis = evaluate_formatting(
        extracted_text,
        has_tables=has_tables,
        is_single_column=is_single_column
    )
    
    # Calculate weighted final ATS score
    analysis_result = calculate_overall_score(
        keyword_analysis,
        formatting_analysis,
        file_type=file_type
    )
    
    return analysis_result
