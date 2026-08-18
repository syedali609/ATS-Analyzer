# 📄 ATS Master — Resume ATS Compatibility Analyzer

An advanced, production-ready **Applicant Tracking System (ATS) Resume Analyzer** built with **FastAPI**, **scikit-learn (TF-IDF & Cosine Similarity)**, **pdfplumber**, **python-docx**, and a dark-themed visual frontend with CRT scan-line aesthetics.

---

## 🌟 Key Features

- **TF-IDF Keyword Matcher**: Extracts top 25 unigrams & bigrams from target Job Descriptions, calculates keyword coverage %, and computes whole-document TF-IDF cosine similarity with stem-matching.
- **6-Point Structural ATS Formatting Audit**:
  1. Standard Section Headers (25 pts)
  2. Parseable Contact Information (20 pts)
  3. Table Structure Warning (20 pts)
  4. Single-Column Layout Heuristic (15 pts)
  5. Optimal Word Count (150–900 words) (10 pts)
  6. Consistent Work History Dates (10 pts)
- **Multi-Format Support**: Reads `.pdf` via `pdfplumber`, `.docx` via `python-docx`, and raw plain text.
- **Hybrid Frontend Engine**: Built-in fallback engine allows offline client-side evaluation if the backend server is unreachable.
- **Unit Test Suite**: 100% test pass rate across keyword extraction, cosine similarity, header parsing, and formatting audit checks.

---

## 📁 Repository Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI application entrypoint
│   │   ├── api/
│   │   │   └── routes.py           # API endpoints (POST /api/analyze, GET /api/health)
│   │   ├── core/
│   │   │   ├── config.py           # Application settings & score weights
│   │   │   └── constants.py        # Section headers, regexes, clean stopwords
│   │   ├── parsers/
│   │   │   ├── pdf_parser.py       # PDF text, table & column extraction
│   │   │   ├── docx_parser.py      # DOCX paragraph & table parser
│   │   │   └── base_parser.py      # File uploader dispatcher
│   │   ├── analysis/
│   │   │   ├── keyword_matcher.py  # TF-IDF keyword extraction & cosine similarity
│   │   │   ├── formatting_checks.py# 6 weighted ATS structure checks
│   │   │   └── scorer.py          # Composite score calculator & recommendations
│   │   ├── models/
│   │   │   └── schemas.py          # Pydantic v2 request/response models
│   │   └── utils/
│   │       └── text_cleaning.py   # Text sanitization & tokenizers
│   ├── tests/
│   │   ├── test_keyword_matcher.py # Unit tests for TF-IDF keyword matching
│   │   └── test_formatting_checks.py # Unit tests for 6 ATS formatting checks
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   └── index.html                 # Single-file HTML/CSS/JS web application
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start Guide

### 1. Backend Setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Launch FastAPI development server
uvicorn app.main:app --reload --port 8000
```

- Interactive API Docs (Swagger UI): `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/api/health`

### 2. Run Test Suite

```bash
cd backend
pytest
```

### 3. Frontend Setup

```bash
cd frontend
python3 -m http.server 5500
```
Open `http://localhost:5500` in your web browser.

---

## 📊 ATS Scoring Formula

$$\text{Overall ATS Score} = (0.6 \times \text{Keyword Match Score}) + (0.4 \times \text{Formatting Audit Score})$$

Where:
$$\text{Keyword Match Score} = (0.7 \times \text{Keyword Coverage \%}) + (0.3 \times \text{TF-IDF Cosine Similarity \%})$$

---

## 📜 License

MIT License &copy; 2026.
