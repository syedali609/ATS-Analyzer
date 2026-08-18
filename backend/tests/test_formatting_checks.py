import pytest
from app.analysis.formatting_checks import (
    check_standard_headers,
    check_contact_info,
    evaluate_formatting
)

def test_check_standard_headers():
    text = """
    JOHN DOE
    john.doe@email.com | (555) 019-2831 | linkedin.com/in/johndoe
    
    PROFESSIONAL SUMMARY
    Innovative software engineer with 5 years experience.
    
    WORK EXPERIENCE
    Software Engineer - Tech Corp (Jan 2021 - Present)
    - Developed scalable microservices in Python.
    
    EDUCATION
    BS in Computer Science - University of Science (2016 - 2020)
    
    SKILLS
    Python, React, TypeScript, Docker, PostgreSQL
    """
    passed, score, max_pts, headers, details = check_standard_headers(text)
    assert passed is True
    assert score == 25
    assert len(headers) >= 4

def test_check_contact_info():
    text = "Jane Smith\njane.smith@example.com\n+1 (555) 123-4567\nlinkedin.com/in/janesmith"
    passed, score, max_pts, email, phone, details = check_contact_info(text)
    assert passed is True
    assert email == "jane.smith@example.com"
    assert phone is not None
    assert score == 25 or score == 20

def test_check_contact_info_missing_email():
    text = "Jane Smith\nNo contact details provided."
    passed, score, max_pts, email, phone, details = check_contact_info(text)
    assert passed is False
    assert email is None
    assert score == 0

def test_evaluate_formatting_good_resume():
    text = """
    ALEX JOHNSON
    alex.johnson@devmail.com | (555) 234-5678 | linkedin.com/in/alexjohnson
    
    SUMMARY
    Senior Full Stack Engineer with 6+ years of experience building scalable web applications.
    
    WORK EXPERIENCE
    Lead Engineer - Acme Cloud Solutions (Jan 2022 - Present)
    - Architected microservices architecture handling 10M daily requests.
    
    Senior Developer - DataFlow Inc (Mar 2019 - Dec 2021)
    - Reduced database query latency by 45% through query optimization.
    
    EDUCATION
    Bachelor of Science in Software Engineering, Tech State University (2015 - 2019)
    
    SKILLS
    Python, FastAPI, TypeScript, React, Docker, Kubernetes, AWS, PostgreSQL
    """
    result = evaluate_formatting(text, has_tables=False, is_single_column=True)
    assert result.formatting_score >= 80.0
    assert len(result.checks) == 6
    assert result.has_contact_info is True
    assert result.email_found == "alex.johnson@devmail.com"

def test_evaluate_formatting_poor_resume():
    text = "Just a short raw note without sections or email."
    result = evaluate_formatting(text, has_tables=True, is_single_column=False)
    assert result.formatting_score < 50.0
