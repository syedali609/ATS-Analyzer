from typing import List
from app.core.config import settings
from app.models.schemas import (
    KeywordAnalysis,
    FormattingAnalysis,
    AnalysisResponse
)

def generate_recommendations(
    keyword_analysis: KeywordAnalysis,
    formatting_analysis: FormattingAnalysis
) -> List[str]:
    """
    Generate prioritized, actionable feedback to increase the ATS score.
    """
    recs: List[str] = []
    
    # Keyword recommendations
    if keyword_analysis.missing_keywords:
        top_missing = keyword_analysis.missing_keywords[:6]
        recs.append(
            f"Add high-relevance missing keywords: {', '.join(top_missing)}."
        )
    if keyword_analysis.coverage_score < 50.0:
        recs.append(
            "Low keyword coverage (<50%). Align bullet point phrasing closely with terms in the job description."
        )
        
    # Formatting recommendations from failed checks
    for check in formatting_analysis.checks:
        if not check.passed:
            recs.append(f"[{check.name}] {check.details}")
            
    if not recs:
        recs.append("Excellent resume structure and keyword match! Ready for submission.")
        
    return recs

def calculate_overall_score(
    keyword_analysis: KeywordAnalysis,
    formatting_analysis: FormattingAnalysis,
    file_type: str
) -> AnalysisResponse:
    """
    Combines keyword match score and formatting score using weights:
    overall_score = KEYWORD_WEIGHT * keyword_score + FORMATTING_WEIGHT * formatting_score
    """
    kw_weight = settings.KEYWORD_SCORE_WEIGHT
    fmt_weight = settings.FORMATTING_SCORE_WEIGHT
    
    overall = (kw_weight * keyword_analysis.keyword_score) + (fmt_weight * formatting_analysis.formatting_score)
    overall_score = round(min(max(overall, 0.0), 100.0), 1)
    
    recommendations = generate_recommendations(keyword_analysis, formatting_analysis)
    
    return AnalysisResponse(
        overall_score=overall_score,
        keyword_score=keyword_analysis.keyword_score,
        formatting_score=formatting_analysis.formatting_score,
        resume_word_count=formatting_analysis.word_count,
        file_type=file_type,
        keyword_analysis=keyword_analysis,
        formatting_analysis=formatting_analysis,
        recommendations=recommendations
    )
