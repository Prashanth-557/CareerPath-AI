# 🚀 CareerPath AI: Enterprise Career Guidance System

![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

An end-to-end, AI-powered career optimization platform designed to help software engineers bridge skill gaps, bypass Applicant Tracking Systems (ATS), and prepare for technical interviews. Built with a decoupled microservice architecture featuring a React/Vite frontend and a Python/Flask Machine Learning API.

## ✨ Core Architecture & Modules

The system is broken down into 5 independent ML and NLP-driven modules, secured behind a custom SQLite JWT-style authentication gate.

1. **🧠 Smart Skill Gap Analyzer (TF-IDF & Cosine Similarity)**
   - Parses user resumes (`pdfminer`) and cross-references them against live job descriptions scraped via `BeautifulSoup`.
   - Utilizes `scikit-learn` (TF-IDF Vectorization) to generate a mathematical match score.
   - Integrates with the **GitHub API** to dynamically extract and verify programming languages from the user's public repositories.

2. **🤖 ATS Resume Optimizer (spaCy POS Tagging)**
   - Scans documents for critical structural ATS compliance (Experience, Education, Skills).
   - Utilizes `TextBlob` for advanced spell-checking.
   - **Custom NLP Heuristic:** Implements `spaCy` Part-of-Speech (POS) tagging to actively ignore Proper Nouns (PROPN), preventing false-positive spell checks on Indian names and university titles.

3. **⚡ Interactive Mock Interview Simulator**
   - A step-by-step, stateful flashcard simulator.
   - Dynamically generates technical interview questions and ideal "STAR method" answer structures based on the user's identified tech stack gaps.

4. **📄 Automated Cover Letter Generator (Regex Engine)**
   - Applies Regular Expressions (`re`) to dynamically extract User Names, Emails, and Phone Numbers directly from the uploaded resume.
   - Generates a highly personalized, ready-to-copy Cover Letter targeted at specific companies.

5. **📋 Dynamic Template Engine**
   - Utilizes `python-docx` and in-memory byte streams (`io.BytesIO`) to instantly compile and download ATS-compliant `.docx` templates tailored to specific engineering domains (AI/ML, Full-Stack, Data Science).

## 🛠️ Local Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/CareerPath-AI.git](https://github.com/yourusername/CareerPath-AI.git)
cd CareerPath-AI