import pytest
from app.analysis.keyword_matcher import (
    extract_top_keywords,
    compute_cosine_similarity,
    match_keywords
)

def test_extract_top_keywords():
    jd = """
    We are seeking a Senior Full Stack Engineer proficient in Python, FastAPI, React, TypeScript,
    Docker, and PostgreSQL. Responsibilities include building scalable REST APIs, microservices,
    optimizing SQL queries, and leading agile sprint teams.
    """
    keywords = extract_top_keywords(jd, max_features=15)
    assert len(keywords) > 0
    kw_names = [kw.lower() for kw, score in keywords]
    assert any(k in kw_names for k in ["python", "fastapi", "react", "typescript", "docker", "postgresql", "rest apis", "microservices"])

def test_compute_cosine_similarity():
    text1 = "Experienced Python developer building FastAPI backends and PostgreSQL databases."
    text2 = "Looking for a Python software engineer with FastAPI experience and database skills."
    similarity = compute_cosine_similarity(text1, text2)
    assert 0.0 <= similarity <= 100.0
    assert similarity >= 15.0  # Similarity for overlapping technical terms (python, fastapi, database)

def test_compute_cosine_similarity_empty():
    assert compute_cosine_similarity("", "job description") == 0.0

def test_match_keywords():
    jd = "Seeking Python, Docker, React, AWS, Kubernetes, GraphQL."
    resume = "Senior developer with Python, Docker, React, and AWS experience."
    
    result = match_keywords(resume, jd)
    assert result.total_jd_keywords > 0
    assert result.matched_count >= 3
    assert result.coverage_score > 0.0
    assert 0.0 <= result.keyword_score <= 100.0
    assert "python" in [k.lower() for k in result.matched_keywords]
