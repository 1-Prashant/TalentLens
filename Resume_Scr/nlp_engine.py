import nltk
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter

# Download required NLTK data
try:
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
except:
    pass

from nltk.corpus import stopwords

try:
    stop_words = set(stopwords.words('english'))
except:
    stop_words = set()


# -------- Clean Text --------
def clean_text(text):
    """Clean and preprocess text"""
    text = text.lower()
    # Keep important technical terms
    text = re.sub(r'[^\w\s\+\#\.]', ' ', text)  # Keep +, #, . for terms like C++, C#, etc.
    text = ' '.join(text.split())  # Remove extra spaces
    return text


def remove_stopwords(text):
    """Remove stopwords but keep technical terms"""
    words = text.split()
    # Keep words that are not stopwords or are technical terms
    technical_terms = {'python', 'java', 'c++', 'c#', 'r', 'go', 'sql'}
    words = [w for w in words if w not in stop_words or w in technical_terms]
    return " ".join(words)


# -------- Extract Keywords --------
def extract_keywords(text, top_n=20):
    """Extract top keywords from text using TF-IDF"""
    # Clean text
    clean = clean_text(text)
    
    # Use TF-IDF
    try:
        vectorizer = TfidfVectorizer(max_features=top_n, stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([clean])
        feature_names = vectorizer.get_feature_names_out()
        
        # Get scores
        scores = tfidf_matrix.toarray()[0]
        keywords = [(feature_names[i], scores[i]) for i in range(len(feature_names))]
        keywords = sorted(keywords, key=lambda x: x[1], reverse=True)
        
        return [kw[0] for kw in keywords]
    except:
        # Fallback to simple word frequency
        words = clean.split()
        word_freq = Counter(words)
        return [word for word, freq in word_freq.most_common(top_n)]


# -------- Advanced Matching Score --------
def get_match_score(resume_text, job_description):
    """Calculate matching score between resume and job description"""
    
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(job_description)
    
    # Method 1: TF-IDF Cosine Similarity (70% weight)
    try:
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([resume_clean, jd_clean])
        cosine_score = cosine_similarity(vectors[0], vectors[1])[0][0]
    except:
        cosine_score = 0
    
    # Method 2: Keyword Overlap (30% weight)
    resume_keywords = set(extract_keywords(resume_text, 30))
    jd_keywords = set(extract_keywords(job_description, 30))
    
    if len(jd_keywords) > 0:
        keyword_overlap = len(resume_keywords & jd_keywords) / len(jd_keywords)
    else:
        keyword_overlap = 0
    
    # Combined score
    final_score = (cosine_score * 0.7) + (keyword_overlap * 0.3)
    
    return round(final_score * 100, 2)


# -------- Enhanced Match Score with Details --------
def get_detailed_match_score(resume_text, job_description, resume_skills=None):
    """Get detailed matching score with breakdown"""
    
    # Basic match score
    base_score = get_match_score(resume_text, job_description)
    
    # Keyword matching
    resume_keywords = set(extract_keywords(resume_text, 25))
    jd_keywords = set(extract_keywords(job_description, 25))
    matched_keywords = resume_keywords & jd_keywords
    missing_keywords = jd_keywords - resume_keywords
    
    # Skills bonus (if skills provided)
    skills_bonus = 0
    if resume_skills:
        skills_bonus = min(len(resume_skills) * 0.5, 10)  # Up to 10 bonus points
    
    final_score = min(base_score + skills_bonus, 100)
    
    return {
        "score": round(final_score, 2),
        "base_score": base_score,
        "skills_bonus": skills_bonus,
        "matched_keywords": list(matched_keywords)[:10],
        "missing_keywords": list(missing_keywords)[:10],
        "resume_keywords": list(resume_keywords)[:15],
        "jd_keywords": list(jd_keywords)[:15]
    }


# -------- Rank Multiple Resumes --------
def rank_resumes(resume_list, job_description):
    """Rank multiple resumes against job description"""
    results = []
    
    for resume in resume_list:
        # Calculate detailed score
        score_details = get_detailed_match_score(
            resume["text"], 
            job_description,
            resume.get("skills", [])
        )
        
        results.append({
            "name": resume.get("name", "Unknown"),
            "email": resume.get("email", "N/A"),
            "phone": resume.get("phone", "N/A"),
            "experience_years": resume.get("experience_years", "N/A"),
            "education": resume.get("education", "N/A"),
            "score": score_details["score"],
            "matched_keywords": score_details["matched_keywords"],
            "missing_keywords": score_details["missing_keywords"]
        })
    
    # Sort by score (descending)
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    
    return results


# -------- Generate Improvement Suggestions --------
def generate_suggestions(resume_text, job_description, missing_skills):
    """Generate personalized improvement suggestions"""
    suggestions = []
    
    # Skill-based suggestions
    if missing_skills:
        top_missing = missing_skills[:5]
        suggestions.append({
            "category": "🎯 Skills Gap",
            "priority": "High",
            "suggestion": f"Add these in-demand skills: {', '.join(top_missing)}",
            "action": "Take online courses or work on projects to gain these skills"
        })
    
    # Keyword suggestions
    jd_keywords = extract_keywords(job_description, 15)
    resume_keywords = extract_keywords(resume_text, 15)
    missing_kw = set(jd_keywords) - set(resume_keywords)
    
    if missing_kw:
        suggestions.append({
            "category": "📝 Keywords",
            "priority": "Medium",
            "suggestion": f"Include keywords: {', '.join(list(missing_kw)[:5])}",
            "action": "Naturally incorporate these terms in your experience and projects"
        })
    
    # Length check
    word_count = len(resume_text.split())
    if word_count < 300:
        suggestions.append({
            "category": "📄 Resume Length",
            "priority": "Medium",
            "suggestion": "Resume seems too short",
            "action": "Add more details about projects, achievements, and responsibilities"
        })
    elif word_count > 1500:
        suggestions.append({
            "category": "📄 Resume Length",
            "priority": "Low",
            "suggestion": "Resume is quite lengthy",
            "action": "Focus on relevant experience and achievements"
        })
    
    # Quantifiable achievements
    numbers = re.findall(r'\d+%|\d+x|\d+\+', resume_text)
    if len(numbers) < 3:
        suggestions.append({
            "category": "📊 Quantifiable Results",
            "priority": "High",
            "suggestion": "Add measurable achievements",
            "action": "Include metrics: 'Improved performance by 30%', 'Led team of 5', etc."
        })
    
    return suggestions


# -------- Calculate Resume Strength --------
def calculate_resume_strength(resume_data, job_description):
    """Calculate overall resume strength score"""
    scores = {
        "completeness": 0,
        "relevance": 0,
        "experience": 0,
        "keywords": 0
    }
    
    # Completeness (out of 25)
    required_fields = ['name', 'email', 'phone', 'education', 'experience_years']
    filled = sum(1 for field in required_fields if resume_data.get(field) and resume_data[field] not in ["Not Found", "Not Specified", "Name Not Found"])
    scores["completeness"] = (filled / len(required_fields)) * 25
    
    # Relevance to JD (out of 40)
    match_score = get_match_score(resume_data["text"], job_description)
    scores["relevance"] = (match_score / 100) * 40
    
    # Experience (out of 20)
    exp = resume_data.get("experience_years", 0)
    if exp != "Not Specified" and isinstance(exp, (int, float)):
        scores["experience"] = min((exp / 5) * 20, 20)  # Max at 5 years
    
    # Keywords (out of 15)
    jd_keywords = set(extract_keywords(job_description, 20))
    resume_keywords = set(extract_keywords(resume_data["text"], 20))
    if jd_keywords:
        keyword_match = len(jd_keywords & resume_keywords) / len(jd_keywords)
        scores["keywords"] = keyword_match * 15
    
    total = sum(scores.values())
    
    return {
        "total_score": round(total, 1),
        "breakdown": {k: round(v, 1) for k, v in scores.items()},
        "grade": get_grade(total)
    }


def get_grade(score):
    """Get letter grade based on score"""
    if score >= 90:
        return "A+"
    elif score >= 85:
        return "A"
    elif score >= 80:
        return "A-"
    elif score >= 75:
        return "B+"
    elif score >= 70:
        return "B"
    elif score >= 65:
        return "B-"
    elif score >= 60:
        return "C+"
    elif score >= 55:
        return "C"
    else:
        return "D"