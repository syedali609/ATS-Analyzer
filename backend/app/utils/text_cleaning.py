import re
from typing import List

def clean_text(text: str) -> str:
    """
    Clean and normalize raw input text: strip whitespace, fix special spaces,
    and remove non-printable characters while preserving paragraph breaks.
    """
    if not text:
        return ""
    
    # Replace non-breaking spaces and special unicode spaces
    text = text.replace('\xa0', ' ').replace('\u200b', '')
    
    # Standardize newline characters
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # Remove multiple spaces per line
    lines = [re.sub(r'[ \t]+', ' ', line).strip() for line in text.split('\n')]
    
    # Join back keeping single blank lines between paragraphs
    cleaned = '\n'.join(lines)
    return cleaned.strip()

def tokenize(text: str) -> List[str]:
    """
    Extract lowercase word tokens (alphanumeric strings, including words with hyphens).
    """
    if not text:
        return []
    return re.findall(r'\b[a-zA-Z0-9+#\.\-]+[a-zA-Z0-9+#]\b|\b[a-zA-Z0-9]\b', text.lower())

def get_word_count(text: str) -> int:
    """
    Calculate the total word count of a given string.
    """
    cleaned = clean_text(text)
    if not cleaned:
        return 0
    return len(cleaned.split())

def extract_lines(text: str) -> List[str]:
    """
    Extract non-empty lines from text.
    """
    cleaned = clean_text(text)
    if not cleaned:
        return []
    return [line.strip() for line in cleaned.split('\n') if line.strip()]
