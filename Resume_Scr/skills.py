# Comprehensive Skills Database - 100+ Skills

SKILLS_DB = {
    # Programming Languages
    "programming": [
        "python", "java", "javascript", "typescript", "c++", "c#", "php", 
        "ruby", "go", "golang", "rust", "kotlin", "swift", "r", "matlab",
        "scala", "perl", "shell scripting", "bash", "powershell"
    ],
    
    # Web Development
    "web_development": [
        "html", "css", "react", "angular", "vue", "node.js", "express",
        "django", "flask", "fastapi", "spring boot", "asp.net", "laravel",
        "next.js", "nuxt.js", "jquery", "bootstrap", "tailwind css",
        "sass", "webpack", "rest api", "graphql", "web services"
    ],
    
    # Mobile Development
    "mobile": [
        "android", "ios", "react native", "flutter", "xamarin", 
        "ionic", "kotlin", "swift", "mobile development"
    ],
    
    # Data Science & ML
    "data_science": [
        "machine learning", "deep learning", "data science", "artificial intelligence",
        "neural networks", "computer vision", "nlp", "natural language processing",
        "statistics", "data analysis", "data mining", "predictive modeling",
        "time series", "a/b testing", "statistical modeling"
    ],
    
    # ML Frameworks & Libraries
    "ml_frameworks": [
        "tensorflow", "pytorch", "keras", "scikit-learn", "xgboost",
        "lightgbm", "catboost", "pandas", "numpy", "scipy", "opencv",
        "hugging face", "transformers", "bert", "gpt", "llm"
    ],
    
    # Big Data
    "big_data": [
        "hadoop", "spark", "pyspark", "hive", "kafka", "flink",
        "storm", "cassandra", "mongodb", "elasticsearch", "big data"
    ],
    
    # Databases
    "databases": [
        "sql", "mysql", "postgresql", "oracle", "sql server", "mongodb",
        "redis", "dynamodb", "cassandra", "neo4j", "sqlite", "mariadb",
        "database design", "nosql", "database optimization"
    ],
    
    # Cloud & DevOps
    "cloud": [
        "aws", "azure", "google cloud", "gcp", "docker", "kubernetes",
        "jenkins", "ci/cd", "terraform", "ansible", "devops", "cloudformation",
        "lambda", "ec2", "s3", "azure functions", "microservices"
    ],
    
    # Data Visualization & BI
    "visualization": [
        "tableau", "power bi", "excel", "looker", "qlikview", "d3.js",
        "matplotlib", "seaborn", "plotly", "data visualization", "dashboards"
    ],
    
    # Version Control & Collaboration
    "tools": [
        "git", "github", "gitlab", "bitbucket", "jira", "confluence",
        "agile", "scrum", "kanban", "version control"
    ],
    
    # Testing
    "testing": [
        "unit testing", "selenium", "pytest", "junit", "test automation",
        "integration testing", "api testing", "performance testing"
    ],
    
    # Cybersecurity
    "security": [
        "cybersecurity", "penetration testing", "ethical hacking",
        "network security", "encryption", "firewall", "vulnerability assessment"
    ],
    
    # Other Technical
    "other_technical": [
        "linux", "unix", "windows server", "networking", "tcp/ip",
        "dns", "load balancing", "monitoring", "etl", "data warehousing",
        "business intelligence", "data engineering", "system design"
    ],
    
    # Soft Skills
    "soft_skills": [
        "leadership", "communication", "problem solving", "teamwork",
        "project management", "analytical thinking", "critical thinking",
        "presentation", "stakeholder management", "mentoring"
    ]
}

# Flatten all skills into a single list
ALL_SKILLS = []
for category in SKILLS_DB.values():
    ALL_SKILLS.extend(category)

# Remove duplicates
ALL_SKILLS = list(set(ALL_SKILLS))


def extract_skills(text):
    """Extract skills from text using comprehensive skills database"""
    text = text.lower()
    found = []
    
    for skill in ALL_SKILLS:
        # Use word boundary matching for better accuracy
        import re
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            found.append(skill)
    
    return list(set(found))


def categorize_skills(skills_list):
    """Categorize extracted skills by domain"""
    categorized = {}
    
    for category, skills in SKILLS_DB.items():
        category_skills = [s for s in skills_list if s in skills]
        if category_skills:
            categorized[category] = category_skills
    
    return categorized


def skill_gap(resume_text, job_text):
    """Analyze skill gap between resume and job description"""
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)
    
    missing = list(set(job_skills) - set(resume_skills))
    matched = list(set(job_skills) & set(resume_skills))
    
    # Calculate match percentage
    if len(job_skills) > 0:
        match_percentage = (len(matched) / len(job_skills)) * 100
    else:
        match_percentage = 0
    
    return {
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "match_percentage": round(match_percentage, 2)
    }


def get_skill_recommendations(missing_skills):
    """Provide learning resources recommendations for missing skills"""
    recommendations = {
        "python": "Coursera, Udemy Python courses, Real Python tutorials",
        "machine learning": "Andrew Ng's ML course, Fast.ai, Kaggle",
        "react": "React documentation, FreeCodeCamp, Scrimba",
        "aws": "AWS Training, A Cloud Guru, AWS Solutions Architect cert",
        "sql": "Mode Analytics SQL Tutorial, SQLZoo, W3Schools",
        "docker": "Docker documentation, Docker Mastery course",
        "data science": "DataCamp, Kaggle courses, Coursera Data Science",
    }
    
    tips = []
    for skill in missing_skills[:5]:  # Top 5 missing skills
        if skill in recommendations:
            tips.append(f"**{skill.title()}**: {recommendations[skill]}")
        else:
            tips.append(f"**{skill.title()}**: Search for online courses, YouTube tutorials, or official documentation")
    
    return tips