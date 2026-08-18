import re
from typing import List, Dict, Set

# Standard ATS Section Headers to detect
STANDARD_SECTION_HEADERS: List[str] = [
    "experience",
    "work experience",
    "professional experience",
    "employment history",
    "education",
    "academic background",
    "skills",
    "technical skills",
    "core competencies",
    "summary",
    "professional summary",
    "profile",
    "executive summary",
    "projects",
    "key projects",
    "personal projects",
    "certifications",
    "licenses",
    "certifications & licenses"
]

# Contact Information Regex Patterns
EMAIL_REGEX: re.Pattern = re.compile(
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", re.IGNORECASE
)

PHONE_REGEX: re.Pattern = re.compile(
    r"(\+?\d{1,3}[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}", re.VERBOSE
)

LINKEDIN_REGEX: re.Pattern = re.compile(
    r"(linkedin\.com/in/[a-zA-Z0-9_-]+)", re.IGNORECASE
)

GITHUB_REGEX: re.Pattern = re.compile(
    r"(github\.com/[a-zA-Z0-9_-]+)", re.IGNORECASE
)

# Date formats: e.g. "Jan 2020 - Present", "2018 - 2022", "05/2021 - 12/2023", "2020 – 2024"
DATE_PATTERNS: List[re.Pattern] = [
    re.compile(r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}\s*[-–—]\s*(Present|\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4})\b", re.IGNORECASE),
    re.compile(r"\b(0[1-9]|1[0-2])/\d{4}\s*[-–—]\s*(Present|(0[1-9]|1[0-2])/\d{4})\b", re.IGNORECASE),
    re.compile(r"\b(19|20)\d{2}\s*[-–—]\s*(Present|(19|20)\d{2})\b", re.IGNORECASE)
]

# Clean English stop words (alphanumeric only to avoid sklearn warnings)
STOPWORDS: Set[str] = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren", "arent", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can", "cant", "cannot", "could",
    "couldn", "couldnt", "did", "didn", "didnt", "do", "does", "doesn", "doesnt", "doing",
    "don", "dont", "down", "during", "each", "few", "for", "from", "further", "had",
    "hadn", "hadnt", "has", "hasn", "hasnt", "have", "haven", "havent", "having", "he",
    "hed", "hell", "hes", "her", "here", "heres", "hers", "herself", "him", "himself",
    "his", "how", "hows", "i", "id", "ill", "im", "ive", "if", "in", "into", "is",
    "isn", "isnt", "it", "its", "itself", "lets", "me", "more", "most", "mustn", "mustnt",
    "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or",
    "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan",
    "shant", "she", "shed", "shell", "shes", "should", "shouldn", "shouldnt", "so",
    "some", "such", "than", "that", "thats", "the", "their", "theirs", "them",
    "themselves", "then", "there", "theres", "these", "they", "theyd", "theyll",
    "theyre", "theyve", "this", "those", "through", "to", "too", "under", "until",
    "up", "very", "was", "wasn", "wasnt", "we", "wed", "well", "were", "weren",
    "werent", "weve", "what", "whats", "when", "whens", "where", "wheres", "which",
    "while", "who", "whos", "whom", "why", "whys", "with", "won", "wont", "would",
    "wouldn", "wouldnt", "you", "youd", "youll", "youre", "youve", "your", "yours",
    "yourself", "yourselves", "role", "candidate", "responsibilities", "requirements",
    "seeking", "looking", "ability", "experience", "work", "job", "position", "team",
    "years", "strong", "preferred", "plus", "must", "have"
}

# Strong Action Verbs for Resume Impact
STRONG_ACTION_VERBS: Set[str] = {
    "accelerated", "achieved", "architected", "automated", "built", "championed",
    "created", "decreased", "delivered", "designed", "developed", "directed",
    "drove", "engineered", "established", "expanded", "generated", "implemented",
    "improved", "increased", "initiated", "innovated", "instituted", "launched",
    "led", "managed", "maximized", "minimized", "modernized", "negotiated",
    "optimized", "orchestrated", "overhauled", "pioneered", "reduced", "refactored",
    "restructured", "scaled", "spearheaded", "streamlined", "transformed", "upgraded"
}
