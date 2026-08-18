import re
from typing import List, Tuple
from app.core.constants import (
    STANDARD_SECTION_HEADERS,
    EMAIL_REGEX,
    PHONE_REGEX,
    LINKEDIN_REGEX,
    GITHUB_REGEX,
    DATE_PATTERNS
)
from app.utils.text_cleaning import clean_text, extract_lines, get_word_count
from app.models.schemas import FormattingAnalysis, CheckResult

def check_standard_headers(text: str) -> Tuple[bool, int, int, List[str], str]:
    """Check 1: Standard Section Headers (25 pts)"""
    max_pts = 25
    text_lower = text.lower()
    found_headers = []
    
    for header in STANDARD_SECTION_HEADERS:
        # Match header line or bullet header
        pattern = r'(?:^|\n)\s*(?:[#*•\-]\s*)?' + re.escape(header) + r'\s*(?::|\n|$)'
        if re.search(pattern, text_lower, re.IGNORECASE):
            if header not in found_headers:
                found_headers.append(header)
                
    header_count = len(found_headers)
    if header_count >= 4:
        score = max_pts
        passed = True
        details = f"Great! Found {header_count} standard ATS section headers ({', '.join(found_headers[:4])})."
    elif header_count >= 2:
        score = 15
        passed = False
        details = f"Found {header_count} headers. Consider adding missing standard sections (e.g. Summary, Experience, Education, Skills)."
    else:
        score = 5
        passed = False
        details = "Few standard section headers detected. Use clear headers like 'Work Experience', 'Education', and 'Skills'."
        
    return passed, score, max_pts, found_headers, details

def check_contact_info(text: str) -> Tuple[bool, int, int, str, str, str]:
    """Check 2: Parseable Contact Info (20 pts)"""
    max_pts = 20
    email_match = EMAIL_REGEX.search(text)
    phone_match = PHONE_REGEX.search(text)
    linkedin_match = LINKEDIN_REGEX.search(text) or GITHUB_REGEX.search(text)
    
    email_str = email_match.group(0) if email_match else None
    phone_str = phone_match.group(0) if phone_match else None
    
    has_email = email_match is not None
    has_phone = phone_match is not None
    has_profile = linkedin_match is not None
    
    if has_email and has_phone and has_profile:
        score = max_pts
        passed = True
        details = f"Excellent! Valid email ({email_str}), phone number ({phone_str}), and online profile detected."
    elif has_email and (has_phone or has_profile):
        score = 15
        passed = True
        details = f"Good contact details detected. Found email ({email_str}). Adding both phone and LinkedIn profile is recommended."
    elif has_email:
        score = 10
        passed = False
        details = f"Found email ({email_str}), but missing phone number or LinkedIn link."
    else:
        score = 0
        passed = False
        details = "No valid email address detected. Ensure your contact info is at the top of your resume in plain text."
        
    has_contact = has_email
    return passed, score, max_pts, email_str, phone_str, details

def check_no_tables(has_tables: bool) -> Tuple[bool, int, int, str]:
    """Check 3: No Tables (20 pts)"""
    max_pts = 20
    if not has_tables:
        return True, max_pts, max_pts, "No table structures detected. Standard text layout reads cleanly in ATS."
    else:
        return False, 5, max_pts, "Table structures detected. Many ATS parsers skip or scramble text inside tables. Convert tables to bullet lists."

def check_single_column(is_single_column: bool) -> Tuple[bool, int, int, str]:
    """Check 4: Single-Column Layout (15 pts)"""
    max_pts = 15
    if is_single_column:
        return True, max_pts, max_pts, "Clean single-column layout detected. Standard top-to-bottom reading order."
    else:
        return False, 5, max_pts, "Multi-column layout detected. Multi-column text can cause ATS parsers to misread line order."

def check_word_count(word_count: int) -> Tuple[bool, int, int, str]:
    """Check 5: Optimal Resume Length (10 pts)"""
    max_pts = 10
    if 300 <= word_count <= 800:
        return True, max_pts, max_pts, f"Ideal word count ({word_count} words). Fits standard 1-2 page length."
    elif 150 <= word_count < 300:
        return False, 6, max_pts, f"Resume word count ({word_count} words) is slightly brief. Expand bullet points with measurable achievements."
    elif 800 < word_count <= 1200:
        return False, 6, max_pts, f"Resume length ({word_count} words) is on the longer side. Try streamlining concise bullet points."
    else:
        return False, 2, max_pts, f"Resume length ({word_count} words) is outside recommended 150-900 word boundary."

def check_date_consistency(text: str) -> Tuple[bool, int, int, str]:
    """Check 6: Consistent Date Formatting (10 pts)"""
    max_pts = 10
    matches_found = 0
    for pattern in DATE_PATTERNS:
        matches = pattern.findall(text)
        if matches:
            matches_found += len(matches)
            
    if matches_found >= 2:
        return True, max_pts, max_pts, f"Consistent date ranges detected ({matches_found} work history dates found)."
    elif matches_found == 1:
        return False, 5, max_pts, "Found 1 standard date pattern. Ensure all job experiences include start and end dates (e.g. 'Jan 2021 - Present')."
    else:
        return False, 2, max_pts, "No standard date ranges (e.g. 'MM/YYYY - MM/YYYY' or 'Month YYYY - Present') detected."

def evaluate_formatting(
    text: str,
    has_tables: bool = False,
    is_single_column: bool = True
) -> FormattingAnalysis:
    """
    Evaluate all 6 formatting checks and compute the overall formatting score (0-100).
    """
    clean_txt = clean_text(text)
    word_cnt = get_word_count(clean_txt)
    
    # 1. Headers
    h_passed, h_score, h_max, detected_headers, h_details = check_standard_headers(clean_txt)
    # 2. Contact
    c_passed, c_score, c_max, email_found, phone_found, c_details = check_contact_info(clean_txt)
    # 3. Tables
    t_passed, t_score, t_max, t_details = check_no_tables(has_tables)
    # 4. Columns
    col_passed, col_score, col_max, col_details = check_single_column(is_single_column)
    # 5. Word count
    w_passed, w_score, w_max, w_details = check_word_count(word_cnt)
    # 6. Dates
    d_passed, d_score, d_max, d_details = check_date_consistency(clean_txt)
    
    checks = [
        CheckResult(name="Standard Section Headers", passed=h_passed, score=h_score, max_score=h_max, details=h_details),
        CheckResult(name="Parseable Contact Info", passed=c_passed, score=c_score, max_score=c_max, details=c_details),
        CheckResult(name="No Tables Detected", passed=t_passed, score=t_score, max_score=t_max, details=t_details),
        CheckResult(name="Single-Column Layout", passed=col_passed, score=col_score, max_score=col_max, details=col_details),
        CheckResult(name="Optimal Resume Length", passed=w_passed, score=w_score, max_score=w_max, details=w_details),
        CheckResult(name="Consistent Date Formatting", passed=d_passed, score=d_score, max_score=d_max, details=d_details)
    ]
    
    total_score = h_score + c_score + t_score + col_score + w_score + d_score
    
    return FormattingAnalysis(
        formatting_score=float(total_score),
        checks=checks,
        detected_headers=detected_headers,
        has_contact_info=c_passed,
        email_found=email_found,
        phone_found=phone_found,
        word_count=word_cnt,
        has_tables=has_tables,
        is_single_column=is_single_column,
        has_consistent_dates=d_passed
    )
