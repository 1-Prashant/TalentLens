"""
Setup Script for AI Resume Screening System Pro
This script helps you set up the application quickly
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False
    return True

def download_nltk_data():
    """Download required NLTK data"""
    print("\n📚 Downloading NLTK data...")
    try:
        import nltk
        nltk.download('stopwords', quiet=True)
        nltk.download('punkt', quiet=True)
        print("✅ NLTK data downloaded successfully!")
    except Exception as e:
        print(f"❌ Error downloading NLTK data: {e}")
        return False
    return True

def verify_installation():
    """Verify that all required packages are installed"""
    print("\n🔍 Verifying installation...")
    required_packages = [
        'streamlit',
        'pandas',
        'nltk',
        'sklearn',
        'plotly',
        'pdfplumber',
        'docx'
    ]
    
    missing = []
    for package in required_packages:
        try:
            if package == 'sklearn':
                __import__('sklearn')
            elif package == 'docx':
                __import__('docx')
            else:
                __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        return False
    else:
        print("✅ All packages verified!")
        return True

def main():
    """Main setup function"""
    print("=" * 60)
    print("🚀 AI Resume Screening System Pro - Setup")
    print("=" * 60)
    
    # Step 1: Install requirements
    if not install_requirements():
        print("\n❌ Setup failed at package installation")
        return
    
    # Step 2: Download NLTK data
    if not download_nltk_data():
        print("\n⚠️ Warning: NLTK data download failed, but continuing...")
    
    # Step 3: Verify installation
    if not verify_installation():
        print("\n❌ Installation verification failed")
        return
    
    # Success message
    print("\n" + "=" * 60)
    print("✅ Setup completed successfully!")
    print("=" * 60)
    print("\n📖 To run the application:")
    print("   streamlit run app.py")
    print("\n💡 Tips:")
    print("   - The app will open in your browser at http://localhost:8501")
    print("   - Upload resumes in PDF, DOCX, or TXT format")
    print("   - Try both User Mode and HR Mode")
    print("\n🎯 Enjoy using the Resume Screening System!")
    print("=" * 60)

if __name__ == "__main__":
    main()