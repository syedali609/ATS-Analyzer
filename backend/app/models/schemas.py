from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class AnalyzeRequest(BaseModel):
    job_description: str = Field(..., description="The job description text to match against")
    resume_text: Optional[str] = Field(None, description="Direct plain text resume input if no file is uploaded")

class CheckResult(BaseModel):
    name: str = Field(..., description="Name of the formatting check")
    passed: bool = Field(..., description="Whether the check passed")
    score: int = Field(..., description="Points earned")
    max_score: int = Field(..., description="Maximum possible points for this check")
    details: str = Field(..., description="Detailed findings or improvement tip")

class KeywordMatchDetail(BaseModel):
    keyword: str
    in_resume: bool
    importance_score: float = Field(default=0.0, description="TF-IDF weight/relevance of keyword")

class KeywordAnalysis(BaseModel):
    total_jd_keywords: int
    matched_count: int
    missing_count: int
    coverage_score: float = Field(..., description="0 to 100 percentage keyword coverage")
    tfidf_similarity: float = Field(..., description="0 to 100 cosine similarity percentage")
    keyword_score: float = Field(..., description="Final combined keyword match score (0-100)")
    matched_keywords: List[str]
    missing_keywords: List[str]
    keyword_details: List[KeywordMatchDetail]

class FormattingAnalysis(BaseModel):
    formatting_score: float = Field(..., description="Total formatting score out of 100")
    checks: List[CheckResult]
    detected_headers: List[str]
    has_contact_info: bool
    email_found: Optional[str] = None
    phone_found: Optional[str] = None
    word_count: int
    has_tables: bool
    is_single_column: bool
    has_consistent_dates: bool

class AnalysisResponse(BaseModel):
    overall_score: float = Field(..., description="Final composite ATS score (0-100)")
    keyword_score: float = Field(..., description="Keyword match score component")
    formatting_score: float = Field(..., description="Formatting check score component")
    resume_word_count: int
    file_type: str
    keyword_analysis: KeywordAnalysis
    formatting_analysis: FormattingAnalysis
    recommendations: List[str] = Field(default_factory=list)

class HealthCheck(BaseModel):
    status: str = "ok"
    version: str = "1.0.0"
