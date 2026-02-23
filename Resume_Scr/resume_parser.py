import pdfplumber
import docx
import re
from datetime import datetime
import io

# -------- Extract text from PDF --------
def extract_text_from_pdf(file):
    """Extract text from PDF file"""
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error extracting PDF: {e}")
    return text


# -------- Extract text from DOCX --------
def extract_text_from_docx(file):
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        print(f"Error extracting DOCX: {e}")
        return ""


# -------- Extract text from TXT --------
def extract_text_from_txt(file):
    """Extract text from TXT file"""
    try:
        content = file.read()
        if isinstance(content, bytes):
            text = content.decode('utf-8', errors='ignore')
        else:
            text = content
        return text
    except Exception as e:
        print(f"Error extracting TXT: {e}")
        return ""


# -------- Extract Email --------
def extract_email(text):
    """Extract email address from text"""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    matches = re.findall(pattern, text)
    return matches[0] if matches else "Not Found"


# -------- Extract Phone Number --------
def extract_phone(text):
    """Extract phone number from text"""
    # Pattern for various phone formats
    patterns = [
        r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # US/International
        r'\d{10}',  # 10 digits
        r'\+\d{12}',  # International with +
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            return matches[0]
    
    return "Not Found"


# -------- Extract Name (Improved) --------
def extract_name(text):
    """Extract name from resume using improved heuristics"""
    lines = text.split("\n")
    
    # Try first few non-empty lines
    for line in lines[:10]:
        line = line.strip()
        
        # Skip empty lines, emails, phones, URLs
        if not line or '@' in line or 'http' in line.lower():
            continue
            
        # Skip lines with too many numbers (likely phone/address)
        if sum(c.isdigit() for c in line) > 3:
            continue
            
        # Skip common headers
        skip_words = ['resume', 'cv', 'curriculum', 'vitae', 'profile', 'contact', 'objective']
        if any(word in line.lower() for word in skip_words):
            continue
        
        # Name is usually 2-4 words, mostly alphabetic
        words = line.split()
        if 2 <= len(words) <= 4:
            # Check if mostly alphabetic
            if sum(c.isalpha() or c.isspace() for c in line) / len(line) > 0.7:
                return line.title()
    
    return "Name Not Found"


# -------- Extract Experience (Years) --------
def extract_experience(text):
    """Extract years of experience from resume"""
    text_lower = text.lower()
    
    # Pattern: "X years of experience" or "X+ years"
    patterns = [
        r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|exp)',
        r'experience[:\s]+(\d+)\+?\s*(?:years?|yrs?)',
        r'(\d+)\+?\s*(?:years?|yrs?)\s*experience'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            return int(match.group(1))
    
    # Alternative: Calculate from work history dates
    years = extract_years_from_dates(text)
    if years:
        return years
    
    return "Not Specified"


def extract_years_from_dates(text):
    """Calculate experience from date ranges in resume"""
    # Pattern for date ranges: "2020 - 2023", "Jan 2020 - Present", etc.
    date_pattern = r'(\d{4})\s*[-–—]\s*(\d{4}|present|current)'
    matches = re.findall(date_pattern, text.lower())
    
    if not matches:
        return None
    
    total_years = 0
    current_year = datetime.now().year
    
    for start, end in matches:
        start_year = int(start)
        end_year = current_year if end in ['present', 'current'] else int(end)
        total_years += max(0, end_year - start_year)
    
    return total_years if total_years > 0 else None


# -------- Extract Education --------
def extract_education(text):
    """Extract education level from resume"""
    text_lower = text.lower()
    
    education_keywords = {
        "PhD": ["phd", "ph.d", "doctorate", "doctoral"],
        "Master's": ["master", "msc", "m.sc", "mba", "m.tech", "m.s"],
        "Bachelor's": ["bachelor", "bsc", "b.sc", "b.tech", "b.e", "b.s", "undergraduate"],
        "Diploma": ["diploma", "associate"],
    }
    
    found_education = []
    
    for degree, keywords in education_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                found_education.append(degree)
                break
    
    # Remove duplicates and return highest degree
    education_hierarchy = ["PhD", "Master's", "Bachelor's", "Diploma"]
    for edu in education_hierarchy:
        if edu in found_education:
            return edu
    
    return "Not Specified"


# -------- Extract Universities/Colleges --------
def extract_universities(text):
    """Extract university/college names from resume"""
    # Common university keywords
    uni_patterns = [
        r'university of [a-z\s]+',
        r'[a-z\s]+ university',
        r'[a-z\s]+ institute of technology',
        r'iit [a-z]+',
        r'nit [a-z]+',
    ]
    
    universities = []
    text_lower = text.lower()
    
    for pattern in uni_patterns:
        matches = re.findall(pattern, text_lower)
        universities.extend([m.title() for m in matches])
    
    # Remove duplicates
    return list(set(universities))[:3]  # Return top 3


# -------- Extract Certifications --------
def extract_certifications(text):
    """Extract certifications from resume"""
    cert_keywords = [
        "aws certified", "azure certified", "google cloud certified",
        "pmp", "cissp", "comptia", "certified", "certification",
        "coursera", "udacity", "nanodegree"
    ]
    
    text_lower = text.lower()
    found_certs = []
    
    lines = text.split('\n')
    for line in lines:
        line_lower = line.lower()
        for cert in cert_keywords:
            if cert in line_lower and len(line) < 150:
                found_certs.append(line.strip())
                break
    
    return found_certs[:5]  # Return top 5


# -------- Extract Projects --------
def extract_projects(text):
    """Extract project count from resume"""
    text_lower = text.lower()
    
    # Look for "projects" section
    project_keywords = ['projects', 'project work', 'key projects']
    
    for keyword in project_keywords:
        if keyword in text_lower:
            # Count bullet points or numbered items after "projects"
            idx = text_lower.find(keyword)
            section = text_lower[idx:idx+1000]  # Next 1000 chars
            
            # Count bullets/numbers
            bullets = section.count('•') + section.count('*') + section.count('-')
            numbers = len(re.findall(r'\n\d+\.', section))
            
            project_count = max(bullets, numbers)
            if project_count > 0:
                return project_count
    
    return 0


# -------- Main Parser Function --------
def parse_resume(file):
    """Main function to parse resume and extract all information"""
    filename = file.name.lower()
    
    # Extract text based on file type
    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(file)
    elif filename.endswith(".docx"):
        text = extract_text_from_docx(file)
    elif filename.endswith(".txt"):
        text = extract_text_from_txt(file)
    else:
        return None
    
    # Extract all information
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "experience_years": extract_experience(text),
        "education": extract_education(text),
        "universities": extract_universities(text),
        "certifications": extract_certifications(text),
        "project_count": extract_projects(text),
        "text": text
    }


# -------- Calculate ATS Score --------
def calculate_ats_score(resume_data):
    """Calculate ATS (Applicant Tracking System) score"""
    score = 0
    feedback = []
    
    # Name (10 points)
    if resume_data["name"] != "Name Not Found":
        score += 10
    else:
        feedback.append("❌ Name not clearly identified")
    
    # Email (15 points)
    if resume_data["email"] != "Not Found":
        score += 15
    else:
        feedback.append("❌ Email missing - Add professional email")
    
    # Phone (10 points)
    if resume_data["phone"] != "Not Found":
        score += 10
    else:
        feedback.append("❌ Phone number missing")
    
    # Experience (20 points)
    exp = resume_data["experience_years"]
    if exp != "Not Specified":
        if exp >= 5:
            score += 20
        elif exp >= 2:
            score += 15
        else:
            score += 10
    else:
        feedback.append("⚠️ Experience not clearly mentioned - Add years of experience")
    
    # Education (15 points)
    if resume_data["education"] != "Not Specified":
        if resume_data["education"] == "PhD":
            score += 15
        elif resume_data["education"] == "Master's":
            score += 13
        else:
            score += 10
    else:
        feedback.append("⚠️ Education not found - Add your degree")
    
    # Skills (20 points - will be added from skills matching)
    
    # Projects (10 points)
    if resume_data["project_count"] >= 3:
        score += 10
    elif resume_data["project_count"] > 0:
        score += 5
    else:
        feedback.append("⚠️ No projects mentioned - Add relevant projects")
    
    return {
        "score": score,
        "feedback": feedback
    }