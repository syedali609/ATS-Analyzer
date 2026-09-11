# 📄 ATS Analyzer — Resume ATS Compatibility Checker

A full-stack **Applicant Tracking System (ATS) resume analyzer**. Upload a resume and a job description, and it scores how well the resume matches on keywords and ATS-friendly formatting — powered by a **FastAPI** backend with TF-IDF keyword matching, and a dark, single-file HTML/CSS/JS frontend that falls back to client-side scoring if the API is unreachable.

**Live app:** [ats-analyzer-teal.vercel.app](https://ats-analyzer-teal.vercel.app)
**API:** [ats-analyzer-1-hz75.onrender.com](https://ats-analyzer-1-hz75.onrender.com/docs)

---

## 🌟 Key Features

- **TF-IDF Keyword Matcher** — extracts the top unigrams & bigrams from the job description, calculates keyword coverage %, and computes whole-document TF-IDF cosine similarity with stem-matching.
- **6-Point ATS Formatting Audit**:
  1. Standard section headers (25 pts)
  2. Parseable contact information (20 pts)
  3. Table structure warning (20 pts)
  4. Single-column layout heuristic (15 pts)
  5. Optimal word count, 150–900 words (10 pts)
  6. Consistent work history dates (10 pts)
- **Multi-format support** — reads `.pdf` (via `pdfplumber`), `.docx` (via `python-docx`), and plain text.
- **Hybrid frontend engine** — if the backend API is unreachable, the frontend falls back to an in-browser scoring engine so the tool still works offline.
- **Unit test suite** — covers keyword extraction, cosine similarity, and formatting audit checks.

---

## 🏗️ Architecture

```
Browser (frontend/index.html)
        │  fetch() → /api/health, /api/analyze
        ▼
FastAPI backend (backend/app)
        │
        ├── parsers/      → extract text from PDF / DOCX / plain text
        ├── analysis/     → TF-IDF keyword matching + formatting audit
        └── models/       → Pydantic request/response schemas
```

The frontend and backend are deployed and hosted **separately**:

| Component | Host | Config |
|---|---|---|
| Frontend | Vercel | static `frontend/index.html` |
| Backend  | Render | `render.yaml` + `backend/Dockerfile` |

Because they're on different domains, the backend's CORS allow-list (`backend/app/core/config.py` → `CORS_ORIGINS`) must include whatever origin the frontend is served from. If you fork or redeploy the frontend to a new domain, add that domain to `CORS_ORIGINS` or the browser will block API requests.

`vercel.json` and `Procfile` are also included as alternate deploy paths (e.g. running both frontend and backend on Vercel, or on any Procfile-based platform like Heroku) — pick whichever matches your hosting setup.

---

## 📁 Repository Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI application entrypoint
│   │   ├── api/
│   │   │   └── routes.py              # Endpoints: GET /api/health, POST /api/analyze
│   │   ├── core/
│   │   │   ├── config.py              # Settings, score weights, CORS allow-list
│   │   │   └── constants.py           # Section headers, regexes, stopwords
│   │   ├── parsers/
│   │   │   ├── pdf_parser.py          # PDF text, table & column extraction
│   │   │   ├── docx_parser.py         # DOCX paragraph & table parser
│   │   │   └── base_parser.py         # Upload dispatcher (routes by file type)
│   │   ├── analysis/
│   │   │   ├── keyword_matcher.py     # TF-IDF keyword extraction & cosine similarity
│   │   │   ├── formatting_checks.py   # 6 weighted ATS structure checks
│   │   │   └── scorer.py              # Composite score & recommendations
│   │   ├── models/
│   │   │   └── schemas.py             # Pydantic v2 request/response models
│   │   └── utils/
│   │       └── text_cleaning.py       # Text sanitization & tokenizers
│   ├── tests/
│   │   ├── test_keyword_matcher.py
│   │   └── test_formatting_checks.py
│   ├── Dockerfile                     # Container build for Render
│   ├── Procfile                       # Process command for Heroku-style platforms
│   ├── requirements.txt
│   └── requirements-dev.txt
├── frontend/
│   └── index.html                     # Single-file HTML/CSS/JS web app
├── render.yaml                        # Render service definitions (backend + static frontend)
├── vercel.json                        # Vercel build/routing config
└── README.md
```

---

## 🚀 Running It Locally

### 1. Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --reload --port 8000
```

- Swagger UI: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/api/health`

### 2. Frontend

```bash
cd frontend
python3 -m http.server 5500
```

Open `http://localhost:5500` in your browser. The frontend auto-detects whether it's running locally or in production and points itself at the right API base URL — see the top of the `<script>` block in `frontend/index.html` if you need to adjust this.

### 3. Tests

```bash
cd backend
pip install -r requirements-dev.txt
pytest
```

---

## 📊 ATS Scoring Formula

```
Overall ATS Score = (0.6 × Keyword Match Score) + (0.4 × Formatting Audit Score)

Keyword Match Score = (0.7 × Keyword Coverage %) + (0.3 × TF-IDF Cosine Similarity %)
```

Weights are configurable via `KEYWORD_SCORE_WEIGHT` and `FORMATTING_SCORE_WEIGHT` in `backend/app/core/config.py` (or as environment variables — see `render.yaml`).

---

## 🔌 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Returns service status and version. |
| `POST` | `/api/analyze` | Analyzes a resume against a job description. Accepts a `file` upload (PDF/DOCX/TXT) **or** raw `resume_text`, plus a required `job_description`. Returns keyword coverage, formatting audit results, and an overall score. |

Full interactive docs are available at `/docs` on the running backend.

---
