# 🚀 AI Resume Screening System Pro

An advanced AI-powered resume screening and analysis system with NLP capabilities, ATS scoring, and comprehensive career guidance.

## ✨ Key Features

### 👤 User Mode Features
- **Advanced Resume Parsing**: Extract name, email, phone, experience, education, certifications
- **ATS Score Analysis**: 100-point ATS compatibility score with detailed feedback
- **Skill Gap Analysis**: Compare your skills with job requirements
- **100+ Skills Database**: Comprehensive technical skills across multiple domains
- **25+ Job Roles**: Wide range of positions from entry to senior level
- **Visual Analytics**: Interactive charts and graphs for better insights
- **Career Recommendations**: Personalized learning paths and resources
- **Resume Strength Score**: Overall resume quality assessment with breakdown
- **Keyword Extraction**: Identify important keywords from your resume
- **Multiple File Formats**: Support for PDF, DOCX, and TXT files

### 👔 HR Mode Features
- **Bulk Resume Processing**: Upload and analyze multiple resumes at once
- **Intelligent Ranking**: Rank candidates based on job description match
- **Score Distribution**: Visual representation of candidate pool quality
- **Top Candidate Analysis**: Detailed breakdown of top 3 candidates
- **Keyword Matching**: Show matched and missing keywords for each candidate
- **Export Functionality**: Download results as Excel or CSV
- **Progress Tracking**: Real-time analysis progress indicator

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **NLP**: NLTK, scikit-learn
- **Data Processing**: Pandas, NumPy
- **Visualizations**: Plotly
- **Document Parsing**: pdfplumber, python-docx
- **Machine Learning**: TF-IDF, Cosine Similarity

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Clone or Download the Project**
```bash
cd resume_screening_upgraded
```

2. **Create Virtual Environment (Recommended)**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Download NLTK Data**
```python
# Run this in Python shell or create a setup script
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

## 🚀 Running the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 📖 Usage Guide

### For Job Seekers (User Mode)

1. **Select User Mode** from the sidebar
2. **Upload Your Resume** (PDF, DOCX, or TXT)
3. **Select Target Job Role** from the dropdown
4. **View Results**:
   - ATS Score and feedback
   - Skills distribution
   - Job role fit analysis
   - Skill gap for target role
   - Learning recommendations
   - Resume strength analysis
   - Career advice

### For Recruiters (HR Mode)

1. **Select HR Mode** from the sidebar
2. **Choose Job Role** you're hiring for
3. **Upload Multiple Resumes** (bulk upload supported)
4. **View Results**:
   - Candidate rankings
   - Score distribution
   - Top candidate details
   - Matched/missing keywords
5. **Export Results** as Excel or CSV

## 📊 Scoring System

### ATS Score (100 points)
- Name: 10 points
- Email: 15 points
- Phone: 10 points
- Experience: 20 points
- Education: 15 points
- Projects: 10 points
- Skills: 20 points

### Match Score
- TF-IDF Cosine Similarity: 70%
- Keyword Overlap: 30%
- Skills Bonus: Up to 10 points

### Resume Strength (100 points)
- Completeness: 25 points
- Relevance to JD: 40 points
- Experience: 20 points
- Keywords: 15 points

## 🎯 Supported Job Roles

### Data & Analytics
- Data Scientist
- Data Analyst
- Data Engineer
- Business Intelligence Analyst

### Software Development
- Full Stack Developer
- Frontend Developer
- Backend Developer
- Mobile Developer

### ML & AI
- Machine Learning Engineer
- AI Research Scientist
- NLP Engineer
- Computer Vision Engineer

### Cloud & Infrastructure
- Cloud Engineer
- Cloud Architect
- DevOps Engineer
- Site Reliability Engineer

### Other Roles
- Cybersecurity Analyst
- Security Engineer
- Product Manager
- Technical Project Manager
- QA Engineer
- SDET
- Blockchain Developer
- Database Administrator
- UI/UX Designer

## 💡 Tips for Best Results

### For Job Seekers
1. **Use Keywords**: Include relevant technical terms naturally
2. **Quantify Achievements**: Use numbers and percentages
3. **Clear Structure**: Use clear headings and sections
4. **Update Regularly**: Keep skills and experience current
5. **Tailor Resume**: Customize for each job application

### For Recruiters
1. **Clear Job Description**: Provide detailed role requirements
2. **Consistent Format**: Request standardized resume formats
3. **Multiple Criteria**: Don't rely solely on match score
4. **Manual Review**: Use tool as initial screening, then manual review
5. **Feedback Loop**: Refine job descriptions based on results

## 🔧 Customization

### Adding New Job Roles
Edit `roles.py`:
```python
ROLES = {
    "Your New Role": {
        "description": "Detailed job description with required skills...",
        "level": "Entry/Mid/Senior"
    }
}
```

### Adding New Skills
Edit `skills.py`:
```python
SKILLS_DB = {
    "your_category": [
        "skill1", "skill2", "skill3"
    ]
}
```

## 🐛 Troubleshooting

### Common Issues

1. **NLTK Data Not Found**
```python
import nltk
nltk.download('stopwords')
nltk.download('punkt')
```

2. **PDF Parsing Errors**
- Ensure PDF is not password-protected
- Try converting to DOCX or TXT

3. **Port Already in Use**
```bash
streamlit run app.py --server.port 8502
```

4. **Module Not Found**
```bash
pip install -r requirements.txt --upgrade
```

## 📝 File Structure

```
resume_screening_upgraded/
│
├── app.py                 # Main Streamlit application
├── resume_parser.py       # Resume parsing and information extraction
├── nlp_engine.py         # NLP matching and scoring algorithms
├── skills.py             # Skills database and extraction
├── roles.py              # Job roles database
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🔮 Future Enhancements

- [ ] Multi-language support
- [ ] AI-powered resume writing suggestions
- [ ] Interview question recommendations
- [ ] Salary estimation based on skills
- [ ] LinkedIn profile integration
- [ ] Email notifications for HR
- [ ] Advanced filtering options
- [ ] Candidate comparison tool
- [ ] Resume builder integration
- [ ] API endpoints for integration

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is open-source and available for educational and commercial use.

## 👨‍💻 Author

Built with ❤️ using AI and modern NLP technologies

## 🙏 Acknowledgments

- Streamlit for the amazing framework
- scikit-learn for ML algorithms
- NLTK for NLP capabilities
- Plotly for beautiful visualizations

---

**Need Help?** Feel free to reach out or open an issue!

**Star ⭐ this project if you found it helpful!**