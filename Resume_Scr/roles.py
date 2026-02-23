ROLES = {
    # Data & Analytics Roles
    "Data Scientist": {
        "description": """Looking for a Data Scientist with expertise in Python, machine learning, deep learning, 
        statistics, data science, pandas, numpy, scikit-learn, SQL, data visualization, A/B testing, 
        and statistical modeling. Experience with TensorFlow or PyTorch is a plus.""",
        "level": "Mid-Senior"
    },
    
    "Machine Learning Engineer": {
        "description": """Seeking ML Engineer with strong skills in Python, TensorFlow, PyTorch, scikit-learn, 
        deep learning, NLP, computer vision, model deployment, MLOps, Docker, Kubernetes, and cloud platforms (AWS/Azure/GCP). 
        Experience with production ML systems required.""",
        "level": "Mid-Senior"
    },
    
    "Data Analyst": {
        "description": """Hiring Data Analyst with proficiency in SQL, Excel, Power BI, Tableau, Python, 
        pandas, data visualization, statistics, dashboard creation, and business intelligence. 
        Strong analytical and communication skills required.""",
        "level": "Entry-Mid"
    },
    
    "Data Engineer": {
        "description": """Need Data Engineer experienced in Python, SQL, ETL, data warehousing, Spark, PySpark, 
        Hadoop, Kafka, Airflow, AWS/Azure, database design, data pipelines, and big data technologies.""",
        "level": "Mid-Senior"
    },
    
    "Business Intelligence Analyst": {
        "description": """Looking for BI Analyst with skills in SQL, Power BI, Tableau, Excel, data modeling, 
        data warehousing, business analytics, KPI tracking, and stakeholder management.""",
        "level": "Mid"
    },
    
    # Software Development Roles
    "Full Stack Developer": {
        "description": """Seeking Full Stack Developer proficient in JavaScript/TypeScript, React, Node.js, 
        Express, HTML, CSS, REST API, GraphQL, MongoDB, PostgreSQL, Git, and modern web development practices. 
        Experience with Next.js or cloud deployment is a plus.""",
        "level": "Mid-Senior"
    },
    
    "Frontend Developer": {
        "description": """Need Frontend Developer with expertise in HTML, CSS, JavaScript, React, Angular or Vue, 
        TypeScript, responsive design, REST API integration, Git, webpack, and modern frontend tooling.""",
        "level": "Entry-Mid"
    },
    
    "Backend Developer": {
        "description": """Hiring Backend Developer skilled in Python/Java/Node.js, REST API, GraphQL, 
        database design, SQL, MongoDB, microservices, Docker, authentication, and scalable system design.""",
        "level": "Mid-Senior"
    },
    
    "DevOps Engineer": {
        "description": """Looking for DevOps Engineer with experience in AWS/Azure/GCP, Docker, Kubernetes, 
        Jenkins, CI/CD, Terraform, Ansible, Linux, shell scripting, monitoring, and infrastructure automation.""",
        "level": "Mid-Senior"
    },
    
    "Mobile Developer": {
        "description": """Seeking Mobile Developer with skills in React Native, Flutter, or native iOS/Android development, 
        JavaScript/Kotlin/Swift, REST API integration, Git, and mobile UI/UX best practices.""",
        "level": "Mid"
    },
    
    # Cloud & Infrastructure
    "Cloud Engineer": {
        "description": """Need Cloud Engineer with expertise in AWS/Azure/GCP, Docker, Kubernetes, 
        cloud architecture, serverless, Lambda, EC2, S3, networking, security, and infrastructure as code.""",
        "level": "Mid-Senior"
    },
    
    "Cloud Architect": {
        "description": """Looking for Cloud Architect with deep knowledge of AWS/Azure/GCP, microservices, 
        system design, security, compliance, cost optimization, multi-cloud strategies, and enterprise architecture.""",
        "level": "Senior"
    },
    
    "Site Reliability Engineer": {
        "description": """Hiring SRE with skills in Linux, Python, monitoring, logging, Kubernetes, Docker, 
        CI/CD, incident management, performance tuning, and scalable infrastructure design.""",
        "level": "Mid-Senior"
    },
    
    # AI & ML Specialized
    "AI Research Scientist": {
        "description": """Seeking AI Research Scientist with PhD or equivalent experience in machine learning, 
        deep learning, neural networks, PyTorch/TensorFlow, research publications, Python, mathematics, 
        and experience in NLP, computer vision, or reinforcement learning.""",
        "level": "Senior"
    },
    
    "NLP Engineer": {
        "description": """Need NLP Engineer with expertise in natural language processing, transformers, 
        BERT, GPT, Hugging Face, Python, deep learning, text analytics, and production NLP systems.""",
        "level": "Mid-Senior"
    },
    
    "Computer Vision Engineer": {
        "description": """Looking for Computer Vision Engineer skilled in OpenCV, deep learning, 
        TensorFlow/PyTorch, image processing, object detection, CNN, Python, and real-time vision systems.""",
        "level": "Mid-Senior"
    },
    
    # Cybersecurity
    "Cybersecurity Analyst": {
        "description": """Hiring Cybersecurity Analyst with knowledge of network security, penetration testing, 
        vulnerability assessment, SIEM tools, firewall, encryption, incident response, and security frameworks.""",
        "level": "Mid"
    },
    
    "Security Engineer": {
        "description": """Need Security Engineer with expertise in application security, cloud security, 
        DevSecOps, threat modeling, security testing, Python/Java, and secure coding practices.""",
        "level": "Mid-Senior"
    },
    
    # Product & Project Management
    "Product Manager": {
        "description": """Seeking Product Manager with skills in product strategy, roadmap planning, 
        stakeholder management, agile/scrum, user research, analytics, SQL, and strong communication. 
        Technical background preferred.""",
        "level": "Mid-Senior"
    },
    
    "Technical Project Manager": {
        "description": """Looking for Technical PM with experience in project management, agile, scrum, 
        JIRA, technical understanding, stakeholder communication, risk management, and software development lifecycle.""",
        "level": "Mid-Senior"
    },
    
    # QA & Testing
    "QA Engineer": {
        "description": """Hiring QA Engineer with skills in test automation, Selenium, API testing, 
        Python/Java, unit testing, integration testing, performance testing, and CI/CD integration.""",
        "level": "Entry-Mid"
    },
    
    "SDET": {
        "description": """Need Software Development Engineer in Test with expertise in test automation frameworks, 
        Python/Java, Selenium, API testing, performance testing, CI/CD, and strong programming skills.""",
        "level": "Mid-Senior"
    },
    
    # Blockchain & Emerging Tech
    "Blockchain Developer": {
        "description": """Looking for Blockchain Developer with knowledge of Ethereum, Solidity, smart contracts, 
        Web3, cryptocurrency, distributed systems, and blockchain architecture.""",
        "level": "Mid-Senior"
    },
    
    # Database
    "Database Administrator": {
        "description": """Seeking DBA with expertise in SQL Server/Oracle/PostgreSQL, database optimization, 
        backup and recovery, performance tuning, security, and database administration.""",
        "level": "Mid-Senior"
    },
    
    # UI/UX
    "UI/UX Designer": {
        "description": """Need UI/UX Designer with skills in Figma, Adobe XD, user research, wireframing, 
        prototyping, user testing, design systems, and understanding of frontend technologies (HTML/CSS).""",
        "level": "Mid"
    }
}


def get_role_category(role_name):
    """Categorize roles by domain"""
    categories = {
        "Data & Analytics": ["Data Scientist", "Data Analyst", "Data Engineer", "Business Intelligence Analyst"],
        "Software Development": ["Full Stack Developer", "Frontend Developer", "Backend Developer", "Mobile Developer"],
        "ML & AI": ["Machine Learning Engineer", "AI Research Scientist", "NLP Engineer", "Computer Vision Engineer"],
        "Cloud & Infrastructure": ["Cloud Engineer", "Cloud Architect", "DevOps Engineer", "Site Reliability Engineer"],
        "Security": ["Cybersecurity Analyst", "Security Engineer"],
        "Management": ["Product Manager", "Technical Project Manager"],
        "QA & Testing": ["QA Engineer", "SDET"],
        "Other": ["Blockchain Developer", "Database Administrator", "UI/UX Designer"]
    }
    
    for category, roles in categories.items():
        if role_name in roles:
            return category
    return "Other"