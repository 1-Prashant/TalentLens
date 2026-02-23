import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from resume_parser import parse_resume, calculate_ats_score
from nlp_engine import (get_match_score, rank_resumes, extract_keywords, 
                        generate_suggestions, calculate_resume_strength,
                        get_detailed_match_score)
from roles import ROLES, get_role_category
from skills import (skill_gap, extract_skills, categorize_skills, 
                    get_skill_recommendations, ALL_SKILLS)
st.markdown("""
<style>

/* Default = white text (for dark UI) */
body, .stApp {
    color: white;
}

/* White / light cards → make text black */
div[data-testid="stMetric"] {
    background-color: white !important;
    color: black !important;
}

/* Metric text inside light cards */
div[data-testid="stMetric"] * {
    color: black !important;
}

/* Any custom light card */
.light-card {
    background: white !important;
    color: black !important;
}

/* Dark cards keep white */
.dark-card {
    background: #1e1e1e !important;
    color: white !important;
}

/* Auto detect light backgrounds */
div[style*="background-color: white"],
div[style*="background: white"],
div[style*="#fff"],
div[style*="#f"] {
    color: black !important;
}

</style>
""", unsafe_allow_html=True)
# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🚀 AI Resume Screening System Pro (NLP Powered)</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/resume.png", width=150)
    st.title("⚙️ Settings")
    mode = st.selectbox("Select Mode", ["👤 User Mode", "👔 HR Mode"], index=0)
    
    st.markdown("---")
    st.markdown("### 📊 Features")
    st.markdown("""
    - ✅ 100+ Skills Database
    - ✅ 25+ Job Roles
    - ✅ ATS Score Analysis
    - ✅ Skill Gap Analysis
    - ✅ Advanced NLP Matching
    - ✅ Experience & Education Extraction
    - ✅ Career Recommendations
    """)
    
    st.markdown("---")
    st.info("💡 Upload resume in PDF, DOCX, or TXT format")


# ---------------- USER MODE ----------------
if mode == "👤 User Mode":
    st.header("👤 Resume Analyzer & Career Advisor")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "📄 Upload Your Resume", 
            type=["pdf", "docx", "txt"],
            help="Supported formats: PDF, DOCX, TXT"
        )
    
    with col2:
        role = st.selectbox(
            "🎯 Target Job Role", 
            list(ROLES.keys()),
            help="Select the role you're applying for"
        )
    
    if uploaded_file:
        with st.spinner("🔍 Analyzing your resume..."):
            # Parse resume
            resume = parse_resume(uploaded_file)
            
            if resume is None:
                st.error("❌ Could not parse resume. Please upload a valid PDF, DOCX, or TXT file.")
            else:
                # Extract skills
                resume_skills = extract_skills(resume["text"])
                resume["skills"] = resume_skills
                
                # Calculate ATS Score
                ats_result = calculate_ats_score(resume)
                
                # Basic Information Section
                st.markdown("## 📋 Extracted Information")
                
                info_col1, info_col2, info_col3, info_col4 = st.columns(4)
                
                with info_col1:
                    st.metric("Name", resume["name"])
                
                with info_col2:
                    st.metric("Email", resume["email"][:20] + "..." if len(resume["email"]) > 20 else resume["email"])
                
                with info_col3:
                    st.metric("Experience", f"{resume['experience_years']} years" if resume['experience_years'] != "Not Specified" else "Not Found")
                
                with info_col4:
                    st.metric("Education", resume["education"])
                
                st.markdown("---")
                
                # ATS Score Section
                st.markdown("## 🎯 ATS (Applicant Tracking System) Score")
                
                ats_col1, ats_col2 = st.columns([1, 2])
                
                with ats_col1:
                    # Gauge Chart for ATS Score
                    fig_ats = go.Figure(go.Indicator(
                        mode = "gauge+number+delta",
                        value = ats_result["score"],
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "ATS Score", 'font': {'size': 24}},
                        delta = {'reference': 70, 'increasing': {'color': "green"}},
                        gauge = {
                            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                            'bar': {'color': "darkblue"},
                            'bgcolor': "white",
                            'borderwidth': 2,
                            'bordercolor': "gray",
                            'steps': [
                                {'range': [0, 50], 'color': '#ffcccc'},
                                {'range': [50, 75], 'color': '#ffffcc'},
                                {'range': [75, 100], 'color': '#ccffcc'}],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 85}}))
                    
                    fig_ats.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
                    st.plotly_chart(fig_ats, width="stretch")
                
                with ats_col2:
                    st.markdown("### 📝 ATS Feedback")
                    
                    if ats_result["score"] >= 80:
                        st.success("✅ Excellent! Your resume is ATS-friendly")
                    elif ats_result["score"] >= 60:
                        st.warning("⚠️ Good, but needs improvement")
                    else:
                        st.error("❌ Needs significant improvement")
                    
                    if ats_result["feedback"]:
                        st.markdown("**Improvements Needed:**")
                        for feedback in ats_result["feedback"]:
                            st.write(feedback)
                    else:
                        st.success("🎉 All ATS criteria met!")
                
                st.markdown("---")
                
                # Skills Analysis
                st.markdown("## 🛠️ Skills Analysis")
                
                # Categorize skills
                categorized = categorize_skills(resume_skills)
                
                if categorized:
                    # Create skills distribution chart
                    skill_counts = {cat: len(skills) for cat, skills in categorized.items()}
                    
                    fig_skills = px.bar(
                        x=list(skill_counts.keys()),
                        y=list(skill_counts.values()),
                        labels={'x': 'Skill Category', 'y': 'Number of Skills'},
                        title='Skills Distribution by Category',
                        color=list(skill_counts.values()),
                        color_continuous_scale='Blues'
                    )
                    fig_skills.update_layout(showlegend=False, height=400)
                    st.plotly_chart(fig_skills, width="stretch")
                    
                    # Show skills by category
                    st.markdown("### 📊 Your Skills by Category")
                    
                    cols = st.columns(2)
                    for idx, (category, skills) in enumerate(categorized.items()):
                        with cols[idx % 2]:
                            with st.expander(f"**{category.replace('_', ' ').title()}** ({len(skills)} skills)"):
                                st.write(", ".join(skills))
                else:
                    st.warning("⚠️ No technical skills detected. Make sure to include your skills in the resume!")
                
                st.markdown("---")
                
                # Job Fit Analysis
                st.markdown("## 🎯 Job Role Fit Analysis")
                
                # Calculate match scores for all roles
                scores = []
                for r in ROLES:
                    jd = ROLES[r]["description"]
                    score = get_match_score(resume["text"], jd)
                    category = get_role_category(r)
                    scores.append({
                        "Job Role": r,
                        "Match %": score,
                        "Category": category
                    })
                
                df_roles = pd.DataFrame(scores).sort_values("Match %", ascending=False)
                
                # Top 5 roles
                top5 = df_roles.head(5)
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown("### 🏆 Top 5 Matching Roles")
                    
                    # Create horizontal bar chart
                    fig_top5 = px.bar(
                        top5,
                        x="Match %",
                        y="Job Role",
                        orientation='h',
                        color="Match %",
                        color_continuous_scale='RdYlGn',
                        text="Match %"
                    )
                    fig_top5.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                    fig_top5.update_layout(height=300, showlegend=False)
                    st.plotly_chart(fig_top5, width="stretch")
                
                with col2:
                    st.markdown("### 📈 All Roles Comparison")
                    st.dataframe(
                        df_roles.style.background_gradient(subset=['Match %'], cmap='RdYlGn'),
                        height=300
                    )
                
                # Best fit role
                best = df_roles.iloc[0]
                st.success(f"🎯 **Best Fit Role:** {best['Job Role']} with {best['Match %']:.1f}% match!")
                
                st.markdown("---")
                
                # Skill Gap for Target Role
                st.markdown(f"## 🔍 Skill Gap Analysis for {role}")
                
                target_jd = ROLES[role]["description"]
                gap_analysis = skill_gap(resume["text"], target_jd)
                
                gap_col1, gap_col2, gap_col3 = st.columns(3)
                
                with gap_col1:
                    st.metric(
                        "Matched Skills",
                        len(gap_analysis["matched_skills"]),
                        delta=None,
                        delta_color="normal"
                    )
                
                with gap_col2:
                    st.metric(
                        "Missing Skills",
                        len(gap_analysis["missing_skills"]),
                        delta=None,
                        delta_color="inverse"
                    )
                
                with gap_col3:
                    st.metric(
                        "Match Percentage",
                        f"{gap_analysis['match_percentage']:.1f}%",
                        delta=None
                    )
                
                # Visualize skill gap
                if gap_analysis["matched_skills"] or gap_analysis["missing_skills"]:
                    gap_data = pd.DataFrame({
                        'Status': ['Matched', 'Missing'],
                        'Count': [len(gap_analysis["matched_skills"]), len(gap_analysis["missing_skills"])]
                    })
                    
                    fig_gap = px.pie(
                        gap_data,
                        values='Count',
                        names='Status',
                        title='Skill Match Overview',
                        color='Status',
                        color_discrete_map={'Matched': 'lightgreen', 'Missing': 'lightcoral'}
                    )
                    st.plotly_chart(fig_gap, width="stretch")
                
                # Show matched and missing skills
                skill_col1, skill_col2 = st.columns(2)
                
                with skill_col1:
                    st.markdown("### ✅ Matched Skills")
                    if gap_analysis["matched_skills"]:
                        for skill in gap_analysis["matched_skills"]:
                            st.success(f"✓ {skill}")
                    else:
                        st.info("No matched skills found")
                
                with skill_col2:
                    st.markdown("### ❌ Skills to Learn")
                    if gap_analysis["missing_skills"]:
                        for skill in gap_analysis["missing_skills"]:
                            st.error(f"✗ {skill}")
                    else:
                        st.success("🎉 You have all required skills!")
                
                st.markdown("---")
                
                # Learning Recommendations
                if gap_analysis["missing_skills"]:
                    st.markdown("## 📚 Learning Recommendations")
                    
                    recommendations = get_skill_recommendations(gap_analysis["missing_skills"])
                    
                    for rec in recommendations:
                        st.info(rec)
                
                st.markdown("---")
                
                # Resume Strength Analysis
                st.markdown("## 💪 Resume Strength Analysis")
                
                strength = calculate_resume_strength(resume, target_jd)
                
                strength_col1, strength_col2 = st.columns([1, 2])
                
                with strength_col1:
                    # Overall score
                    st.metric(
                        "Overall Resume Score",
                        f"{strength['total_score']}/100",
                        delta=f"Grade: {strength['grade']}"
                    )
                    
                    # Grade indicator
                    if strength['total_score'] >= 80:
                        st.success("🌟 Excellent Resume!")
                    elif strength['total_score'] >= 70:
                        st.info("👍 Good Resume")
                    elif strength['total_score'] >= 60:
                        st.warning("⚠️ Average Resume")
                    else:
                        st.error("❌ Needs Improvement")
                
                with strength_col2:
                    # Breakdown chart
                    breakdown_df = pd.DataFrame({
                        'Category': list(strength['breakdown'].keys()),
                        'Score': list(strength['breakdown'].values())
                    })
                    
                    fig_strength = px.bar(
                        breakdown_df,
                        x='Category',
                        y='Score',
                        title='Resume Strength Breakdown',
                        color='Score',
                        color_continuous_scale='Viridis'
                    )
                    fig_strength.update_layout(height=300)
                    st.plotly_chart(fig_strength, width="stretch")
                
                st.markdown("---")
                
                # Career Advice
                st.markdown("## 💼 Personalized Career Advice")
                
                advice_expander = st.expander("📖 Click to view detailed career guidance", expanded=True)
                
                with advice_expander:
                    if gap_analysis["match_percentage"] >= 70:
                        st.success(f"""
                        🎉 **Great Match!** You're well-suited for the {role} position.
                        
                        **Next Steps:**
                        - Apply to {role} positions confidently
                        - Highlight your {', '.join(gap_analysis['matched_skills'][:3])} skills in interviews
                        - Consider certifications to stand out
                        """)
                    else:
                        st.info(f"""
                        📈 **Development Needed** for {role}
                        
                        **Recommended Actions:**
                        1. **Build Projects**: Create 2-3 projects using {', '.join(gap_analysis['missing_skills'][:3])}
                        2. **Take Courses**: Enroll in online courses for missing skills
                        3. **Update Resume**: Add new skills and projects once completed
                        4. **Timeline**: Plan 3-6 months for skill development
                        
                        **Focus Areas:**
                        - {', '.join(gap_analysis['missing_skills'][:5])}
                        """)
                
                # Improvement Suggestions
                suggestions = generate_suggestions(
                    resume["text"],
                    target_jd,
                    gap_analysis["missing_skills"]
                )
                
                if suggestions:
                    st.markdown("### 🎯 Actionable Improvement Tips")
                    
                    for idx, suggestion in enumerate(suggestions, 1):
                        priority_color = {
                            "High": "🔴",
                            "Medium": "🟡",
                            "Low": "🟢"
                        }
                        
                        with st.container():
                            st.markdown(f"""
                            **{idx}. {suggestion['category']}** {priority_color.get(suggestion['priority'], '⚪')}
                            
                            - **Issue**: {suggestion['suggestion']}
                            - **Action**: {suggestion['action']}
                            """)
                            st.markdown("---")


# ---------------- HR MODE ----------------
else:
    st.header("👔 HR Resume Screening & Ranking System")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        role = st.selectbox(
            "🎯 Select Job Role",
            list(ROLES.keys()),
            help="Choose the position you're hiring for"
        )
    
    with col2:
        st.info(f"**Category:** {get_role_category(role)}")
    
    # Job Description
    with st.expander("📄 View Job Description", expanded=False):
        st.write(ROLES[role]["description"])
    
    st.markdown("---")
    
    # File Upload
    uploaded_files = st.file_uploader(
        "📤 Upload Multiple Resumes",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        help="You can upload multiple resumes at once"
    )
    
    if uploaded_files:
        st.info(f"📊 **{len(uploaded_files)} resumes** uploaded")
        
        with st.spinner("🔍 Analyzing all resumes..."):
            job_desc = ROLES[role]["description"]
            
            resumes = []
            progress_bar = st.progress(0)
            
            for idx, file in enumerate(uploaded_files):
                data = parse_resume(file)
                if data:
                    # Extract skills
                    data["skills"] = extract_skills(data["text"])
                    resumes.append(data)
                
                progress_bar.progress((idx + 1) / len(uploaded_files))
            
            progress_bar.empty()
            
            if not resumes:
                st.error("❌ Could not parse any resumes. Please check file formats.")
            else:
                # Rank resumes
                ranked = rank_resumes(resumes, job_desc)
                
                st.success(f"✅ Successfully analyzed {len(ranked)} resumes")
                
                # Summary Statistics
                st.markdown("## 📊 Screening Summary")
                
                stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
                
                with stat_col1:
                    st.metric("Total Candidates", len(ranked))
                
                with stat_col2:
                    strong_candidates = sum(1 for r in ranked if r["score"] >= 70)
                    st.metric("Strong Matches (≥70%)", strong_candidates)
                
                with stat_col3:
                    avg_score = sum(r["score"] for r in ranked) / len(ranked)
                    st.metric("Average Score", f"{avg_score:.1f}%")
                
                with stat_col4:
                    top_score = ranked[0]["score"]
                    st.metric("Top Score", f"{top_score:.1f}%")
                
                st.markdown("---")
                
                # Ranking Table
                st.markdown("## 🏆 Candidate Ranking")
                
                # Prepare data for table
                table_data = []
                for rank, r in enumerate(ranked, 1):
                    table_data.append({
                        "Rank": rank,
                        "Name": r["name"],
                        "Email": r["email"],
                        "Phone": r.get("phone", "N/A"),
                        "Experience": r.get("experience_years", "N/A"),
                        "Education": r.get("education", "N/A"),
                        "Match Score": f"{r['score']:.1f}%"
                    })
                
                df = pd.DataFrame(table_data)
                
                # Display with color coding
                st.dataframe(
                    df.style.apply(
                        lambda x: ['background-color: #d4edda' if i < 3 else '' for i in range(len(x))],
                        axis=0
                    ),
                    height=400
                )
                
                st.markdown("---")
                
                # Score Distribution
                st.markdown("## 📈 Score Distribution")
                
                scores = [r["score"] for r in ranked]
                
                fig_dist = px.histogram(
                    scores,
                    nbins=10,
                    labels={'value': 'Match Score (%)', 'count': 'Number of Candidates'},
                    title='Candidate Score Distribution',
                    color_discrete_sequence=['#1f77b4']
                )
                fig_dist.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig_dist, width="stretch")
                
                # Top Candidates Detail
                st.markdown("## 🌟 Top 3 Candidates Analysis")
                
                for idx, candidate in enumerate(ranked[:3], 1):
                    with st.expander(f"**Rank #{idx}: {candidate['name']}** - {candidate['score']:.1f}% Match"):
                        cand_col1, cand_col2 = st.columns([1, 1])
                        
                        with cand_col1:
                            st.markdown("**Contact Information:**")
                            st.write(f"📧 {candidate['email']}")
                            st.write(f"📞 {candidate.get('phone', 'N/A')}")
                            st.write(f"🎓 {candidate.get('education', 'N/A')}")
                            st.write(f"💼 {candidate.get('experience_years', 'N/A')} years experience")
                        
                        with cand_col2:
                            st.markdown("**Key Matched Keywords:**")
                            if candidate.get("matched_keywords"):
                                for kw in candidate["matched_keywords"][:5]:
                                    st.success(f"✓ {kw}")
                            
                            if candidate.get("missing_keywords"):
                                st.markdown("**Missing Keywords:**")
                                for kw in candidate["missing_keywords"][:3]:
                                    st.warning(f"⚠ {kw}")
                
                st.markdown("---")
                
                # Download Options
                st.markdown("## 💾 Export Results")
                
                download_col1, download_col2 = st.columns(2)
                
                with download_col1:
                    # Excel Download
                    import io
                    
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        df.to_excel(writer, sheet_name='Rankings', index=False)
                    
                    buffer.seek(0)
                    
                    st.download_button(
                        label="📥 Download Excel Report",
                        data=buffer,
                        file_name=f"{role.replace(' ', '_')}_ranking.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                
                with download_col2:
                    # CSV Download
                    csv = df.to_csv(index=False).encode('utf-8')
                    
                    st.download_button(
                        label="📥 Download CSV Report",
                        data=csv,
                        file_name=f"{role.replace(' ', '_')}_ranking.csv",
                        mime="text/csv"
                    )

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>🚀 <b>AI Resume Screening System Pro</b> | Powered by Advanced NLP & Machine Learning</p>
        <p>Built with Streamlit, scikit-learn, NLTK, and Plotly</p>
    </div>
    """, unsafe_allow_html=True)