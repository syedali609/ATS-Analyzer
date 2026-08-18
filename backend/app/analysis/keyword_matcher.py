import re
import math
from typing import List, Dict, Tuple, Set
from app.core.constants import STOPWORDS
from app.utils.text_cleaning import clean_text, tokenize
from app.models.schemas import KeywordAnalysis, KeywordMatchDetail

SKLEARN_AVAILABLE = False
try:
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

def stem_word(w: str) -> str:
    """Simple lightweight suffix stemmer to unify plurals and verb forms."""
    w = w.lower()
    protected_words = {'string', 'spring', 'bring', 'speed', 'breed', 'freed', 'greed', 'during', 'being', 'nothing', 'something', 'everything', 'king', 'ring', 'thing', 'sing'}
    if w in protected_words:
        return w
    if len(w) > 4:
        if w.endswith("ies"): return w[:-3] + "y"
        if w.endswith("ses") or w.endswith("xes") or w.endswith("ches") or w.endswith("shes"): return w[:-2]
        if w.endswith("s") and not w.endswith("ss"): return w[:-1]
        if w.endswith("ing"): return w[:-3]
        if w.endswith("ed"): return w[:-2]
    return w

def extract_top_keywords(
    job_description: str,
    max_features: int = 25
) -> List[Tuple[str, float]]:
    """
    Extract top TF-IDF / term-frequency ranked unigrams and bigrams from the job description.
    Ensures single technical terms (unigrams) and key multi-word phrases (bigrams) are both included.
    """
    jd_clean = clean_text(job_description)
    if not jd_clean:
        return []
    
    custom_stopwords = list(STOPWORDS)
    
    if SKLEARN_AVAILABLE:
        try:
            # Unigram extraction
            uni_vectorizer = TfidfVectorizer(
                ngram_range=(1, 1),
                stop_words=custom_stopwords,
                min_df=1,
                token_pattern=r'(?u)\b[a-zA-Z0-9+#\.\-]{2,}\b'
            )
            uni_tfidf = uni_vectorizer.fit_transform([jd_clean])
            uni_names = uni_vectorizer.get_feature_names_out()
            uni_scores = uni_tfidf.toarray()[0]
            
            uni_list = [(uni_names[i], float(uni_scores[i])) for i in range(len(uni_names))]
            uni_filtered = [
                (kw, score) for kw, score in uni_list
                if not kw.isdigit() and len(kw) > 2 and kw.lower() not in STOPWORDS
            ]
            uni_filtered.sort(key=lambda x: x[1], reverse=True)
            
            # Bigram extraction
            try:
                bi_vectorizer = TfidfVectorizer(
                    ngram_range=(2, 2),
                    stop_words=custom_stopwords,
                    min_df=1,
                    token_pattern=r'(?u)\b[a-zA-Z0-9+#\.\-]{2,}\b'
                )
                bi_tfidf = bi_vectorizer.fit_transform([jd_clean])
                bi_names = bi_vectorizer.get_feature_names_out()
                bi_scores = bi_tfidf.toarray()[0]
                
                bi_list = [(bi_names[i], float(bi_scores[i])) for i in range(len(bi_names))]
                bi_filtered = [
                    (kw, score) for kw, score in bi_list
                    if not kw.isdigit() and len(kw) > 4
                ]
                bi_filtered.sort(key=lambda x: x[1], reverse=True)
            except Exception:
                bi_filtered = []
            
            # Blend top unigrams (70%) and top bigrams (30%)
            top_unis = uni_filtered[:int(max_features * 0.7)]
            top_bis = bi_filtered[:int(max_features * 0.3)]
            
            combined = top_unis + top_bis
            seen = set()
            dedup = []
            for kw, score in combined:
                if kw not in seen:
                    seen.add(kw)
                    dedup.append((kw, round(score, 3)))
                    
            return dedup[:max_features]
        except Exception:
            pass
            
    # Pure Python n-gram frequency fallback
    words = tokenize(jd_clean)
    freq: Dict[str, int] = {}
    
    for w in words:
        if len(w) > 2 and w not in STOPWORDS and not w.isdigit():
            freq[w] = freq.get(w, 0) + 1
            
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i+1]
        if len(w1) > 2 and len(w2) > 2 and w1 not in STOPWORDS and w2 not in STOPWORDS:
            bigram = f"{w1} {w2}"
            freq[bigram] = freq.get(bigram, 0) + 1
            
    if not freq:
        return []
        
    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:max_features]
    max_freq = sorted_words[0][1] if sorted_words else 1
    return [(w, round(count / max_freq, 3)) for w, count in sorted_words]

def compute_cosine_similarity(text1: str, text2: str) -> float:
    """
    Compute cosine similarity between resume text and job description using stemmed tokens.
    """
    c1 = clean_text(text1)
    c2 = clean_text(text2)
    if not c1 or not c2:
        return 0.0
        
    # Stem tokens for better cross-matching of plurals and verb forms
    t1_stemmed = " ".join([stem_word(w) for w in tokenize(c1)])
    t2_stemmed = " ".join([stem_word(w) for w in tokenize(c2)])
    
    if SKLEARN_AVAILABLE:
        try:
            vectorizer = TfidfVectorizer(
                ngram_range=(1, 1),
                stop_words=list(STOPWORDS),
                sublinear_tf=True,
                token_pattern=r'(?u)\b[a-zA-Z0-9+#\.\-]{2,}\b'
            )
            tfidf = vectorizer.fit_transform([t1_stemmed, t2_stemmed])
            sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
            return round(float(sim) * 100.0, 1)
        except Exception:
            pass
            
    # Pure Python Vector Cosine Similarity Fallback
    t1_tokens = [stem_word(t) for t in tokenize(c1) if t not in STOPWORDS]
    t2_tokens = [stem_word(t) for t in tokenize(c2) if t not in STOPWORDS]
    
    vec1: Dict[str, int] = {}
    vec2: Dict[str, int] = {}
    for t in t1_tokens: vec1[t] = vec1.get(t, 0) + 1
    for t in t2_tokens: vec2[t] = vec2.get(t, 0) + 1
    
    all_vocab = set(vec1.keys()).union(set(vec2.keys()))
    if not all_vocab:
        return 0.0
        
    dot_product = sum(vec1.get(w, 0) * vec2.get(w, 0) for w in all_vocab)
    mag1 = math.sqrt(sum(v**2 for v in vec1.values()))
    mag2 = math.sqrt(sum(v**2 for v in vec2.values()))
    
    if mag1 == 0 or mag2 == 0:
        return 0.0
        
    sim = dot_product / (mag1 * mag2)
    return round(float(sim) * 100.0, 1)

def match_keywords(
    resume_text: str,
    job_description: str
) -> KeywordAnalysis:
    """
    Main keyword analysis function blending keyword coverage (70%) and cosine similarity (30%).
    """
    res_clean = clean_text(resume_text).lower()
    res_stemmed = " ".join([stem_word(w) for w in tokenize(res_clean)])
    
    top_keywords = extract_top_keywords(job_description, max_features=25)
    
    if not top_keywords:
        return KeywordAnalysis(
            total_jd_keywords=0,
            matched_count=0,
            missing_count=0,
            coverage_score=0.0,
            tfidf_similarity=0.0,
            keyword_score=0.0,
            matched_keywords=[],
            missing_keywords=[],
            keyword_details=[]
        )
    
    matched_keywords: List[str] = []
    missing_keywords: List[str] = []
    keyword_details: List[KeywordMatchDetail] = []
    
    res_tokens = set(tokenize(res_clean))
    res_stemmed_tokens = set([stem_word(t) for t in res_tokens])
    
    for kw, importance in top_keywords:
        kw_lower = kw.lower()
        kw_stemmed = " ".join([stem_word(w) for w in kw_lower.split()])
        
        in_resume = False
        if kw_lower in res_clean or kw_stemmed in res_stemmed:
            in_resume = True
        else:
            kw_words = kw_lower.split()
            if all(stem_word(w) in res_stemmed_tokens or w in res_tokens for w in kw_words):
                in_resume = True
        
        detail = KeywordMatchDetail(
            keyword=kw,
            in_resume=in_resume,
            importance_score=round(importance, 3)
        )
        keyword_details.append(detail)
        
        if in_resume:
            matched_keywords.append(kw)
        else:
            missing_keywords.append(kw)
            
    total_count = len(top_keywords)
    matched_count = len(matched_keywords)
    missing_count = len(missing_keywords)
    
    coverage_score = round((matched_count / total_count) * 100.0, 1) if total_count > 0 else 0.0
    cosine_sim = compute_cosine_similarity(resume_text, job_description)
    
    blended_score = round((0.7 * coverage_score) + (0.3 * cosine_sim), 1)
    
    return KeywordAnalysis(
        total_jd_keywords=total_count,
        matched_count=matched_count,
        missing_count=missing_count,
        coverage_score=coverage_score,
        tfidf_similarity=cosine_sim,
        keyword_score=min(blended_score, 100.0),
        matched_keywords=matched_keywords,
        missing_keywords=missing_keywords,
        keyword_details=keyword_details
    )
