from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import io
import tempfile
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from docx import Document
from pdfminer.high_level import extract_text
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
CORS(app)

# Load the NLP model securely
try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    print("Warning: spacy model not found. Run: python -m spacy download en_core_web_sm")

# ==========================================
# DATABASE INITIALIZATION
# ==========================================
def get_db_connection():
    conn = sqlite3.connect('careerpath.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    # Create Users Table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db() # Run this once when the server starts

# ==========================================
# AUTHENTICATION ROUTES (Login & Register)
# ==========================================
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    hashed_password = generate_password_hash(password)
    
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, hashed_password))
        conn.commit()
        
        # Fetch the newly created user to log them in immediately
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        return jsonify({"message": "User registered successfully", "user": {"id": user['id'], "name": user['name'], "email": user['email']}})
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 409
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()

    if user and check_password_hash(user['password'], password):
        return jsonify({"message": "Login successful", "user": {"id": user['id'], "name": user['name'], "email": user['email']}})
    else:
        return jsonify({"error": "Invalid email or password"}), 401

# ==========================================
# FEATURE 1: SMART ANALYZER
# ==========================================
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
        
    file = request.files['file']
    role = request.form.get('role', 'AI/ML Engineer')
    timeline = request.form.get('timeline', '4')
    jd_url = request.form.get('jd_url', '')
    github_input = request.form.get('github_user', '').strip()
    
    temp_path = os.path.join(tempfile.gettempdir(), file.filename)
    file.save(temp_path)
    try:
        resume_text = extract_text(temp_path).lower()
    except Exception as e:
        return jsonify({"error": "Failed to read PDF"}), 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    github_skills_list = []
    github_skills_text = ""
    
    if github_input:
        if "github.com/" in github_input:
            gh_user = github_input.split("github.com/")[-1].strip('/')
        else:
            gh_user = github_input
            
        try:
            gh_res = requests.get(f"https://api.github.com/users/{gh_user}/repos", timeout=5)
            if gh_res.status_code == 200:
                repos = gh_res.json()
                languages = [repo.get('language') for repo in repos if repo.get('language')]
                github_skills_list = list(set(str(l).lower() for l in languages))
                github_skills_text = " " + " ".join(github_skills_list) * 3 
        except:
            pass 

    combined_user_text = resume_text + github_skills_text

    jd_text = ""
    if role == 'Custom Job (Web Scraper)' and jd_url.strip():
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            page = requests.get(jd_url.strip(), headers=headers, timeout=5)
            soup = BeautifulSoup(page.content, 'html.parser')
            jd_text = soup.get_text(separator=' ').lower()
        except:
            jd_text = "python java javascript react sql aws docker api ci/cd algorithms"
    else:
        jds = {
            'AI/ML Engineer': 'python machine learning deep learning tensorflow pytorch nlp computer vision sql algorithms data structures',
            'Full-Stack Developer': 'react node html css javascript typescript sql mongodb aws docker api git ci/cd',
            'Data Scientist': 'python r sql pandas numpy scikit-learn machine learning statistics data visualization tableau kaggle'
        }
        jd_text = jds.get(role, jds['AI/ML Engineer']).lower()

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([combined_user_text, jd_text])
    score = round(cosine_similarity(vectors[0:1], vectors[1:2])[0][0] * 100)

    required_skills = [word for word in jd_text.split() if len(word) > 2]
    unique_required = list(set(required_skills))
    missing_skills = [skill for skill in unique_required if skill not in combined_user_text]
    
    missing_skills = sorted(missing_skills, key=lambda x: required_skills.count(x), reverse=True)
    top_gaps = [skill for skill in missing_skills if not skill.isnumeric()][:6]

    study_plan = []
    weeks = int(timeline)
    tasks_per_week = max(1, len(top_gaps) // weeks) if top_gaps else 1
    
    for w in range(weeks):
        week_skills = top_gaps[w*tasks_per_week : (w+1)*tasks_per_week]
        if not week_skills:
            week_skills = ["Portfolio Building", "System Design"]
        
        study_plan.append({
            "week": f"Week {w+1}",
            "focus": f"Mastering {', '.join(week_skills).title()}",
            "tasks": [f"Complete hands-on tutorial for {skill.title()}" for skill in week_skills] + ["Build a mini-project"]
        })

    return jsonify({
        "match_score_percentage": min(score + 35, 99),
        "skill_gaps": top_gaps, 
        "study_plan": study_plan,
        "github_skills": github_skills_list
    })

# ==========================================
# FEATURE 2: ATS RESUME FIXER
# ==========================================
@app.route('/review_resume', methods=['POST'])
def review_resume():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
        
    file = request.files['file']
    
    temp_path = os.path.join(tempfile.gettempdir(), file.filename)
    file.save(temp_path)
    try:
        text = extract_text(temp_path)
    except:
        return jsonify({"error": "Failed to read PDF"}), 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    lower_text = text.lower()
    structural_issues = []
    
    required_sections = ['experience', 'education', 'skills', 'projects']
    for req in required_sections:
        if req not in lower_text:
            structural_issues.append(f"Missing '{req.title()}' section.")

    spelling_alerts = []
    tech_words = ['python', 'react', 'java', 'sql', 'aws', 'docker', 'machine', 'learning', 'github']
    
    doc = nlp(text)
    words_to_check = [
        token.text for token in doc 
        if token.is_alpha and len(token.text) > 4 
        and token.pos_ != "PROPN"
        and token.text.lower() not in tech_words
    ]
    
    for word in list(set(words_to_check))[:30]:  
        tb_word = TextBlob(word)
        if tb_word.words:
            w = tb_word.words[0]
            if w.spellcheck()[0][1] < 0.8:
                correction = w.correct()
                if str(w).lower() != str(correction).lower():
                    spelling_alerts.append(f"Check spelling: '{w}' -> Did you mean '{correction}'?")

    spelling_alerts = list(set(spelling_alerts))[:4]

    score = 100 - (len(structural_issues) * 10) - (len(spelling_alerts) * 5)

    return jsonify({
        "score": max(score, 20),
        "structural_issues": structural_issues,
        "spelling_alerts": spelling_alerts
    })

# ==========================================
# FEATURE 3: TEMPLATE ENGINE
# ==========================================
@app.route('/download_template/<domain>', methods=['GET'])
def download_template(domain):
    doc = Document()
    clean_domain = domain.replace("_", " ")
    
    doc.add_heading(f'[YOUR NAME] - {clean_domain}', 0)
    doc.add_paragraph('Phone: (123) 456-7890 | Email: youremail@domain.com | LinkedIn: linkedin.com/in/yourprofile')
    
    doc.add_heading('Professional Summary', level=1)
    doc.add_paragraph(f'Results-driven {clean_domain} with experience in building scalable solutions and a dedication to continuous improvement.')

    doc.add_heading('Technical Skills (ATS Optimized)', level=1)
    doc.add_paragraph('• Languages: Python, JavaScript, SQL\n• Frameworks: React, Flask\n• Tools: Git, Docker, AWS')

    doc.add_heading('Professional Experience', level=1)
    doc.add_heading('Software Engineering Intern | Company Name', level=2)
    doc.add_paragraph('• Developed features resulting in a 20% increase in efficiency.\n• Reduced server response time by optimizing database queries.')

    doc.add_heading('Education', level=1)
    doc.add_paragraph('B.Tech in Computer Science\nMalla Reddy University, Hyderabad\nExpected Graduation: 2026')

    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)
    
    return send_file(
        file_stream, 
        as_attachment=True, 
        download_name=f"{clean_domain.replace(' ', '_')}_ATS_Template.docx",
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )

# ==========================================
# FEATURE 4: MOCK INTERVIEW SIMULATOR
# ==========================================
@app.route('/generate_interview', methods=['POST'])
def generate_interview():
    data = request.json
    skills = data.get('skills', [])
    
    question_bank = {
        "docker": {"q": "How does Docker differ from a traditional Virtual Machine?", "hint": "Focus on OS kernel sharing and reduced overhead."},
        "kubernetes": {"q": "What happens when a Pod fails in Kubernetes?", "hint": "Discuss self-healing mechanisms and the Control Plane."},
        "react": {"q": "Explain the Virtual DOM and why it makes React fast.", "hint": "Mention the reconciliation process."},
        "python": {"q": "What is the Global Interpreter Lock (GIL)?", "hint": "Explain how it affects multi-threading."},
        "sql": {"q": "Explain the difference between an INNER JOIN and a LEFT JOIN.", "hint": "INNER returns only matches. LEFT returns all left rows."},
        "pandas": {"q": "How do you handle missing data (NaN) in a Pandas DataFrame?", "hint": "Discuss dropna(), fillna(), or imputation strategies."},
        "aws": {"q": "When would you choose AWS Lambda over Amazon EC2?", "hint": "Lambda is Serverless/event-driven. EC2 is IaaS (always-on)."},
    }
    
    interview_prep = []
    
    for skill in skills:
        clean_skill = skill.strip().lower()
        if clean_skill in question_bank:
            interview_prep.append({
                "skill": skill.strip(), 
                "question": question_bank[clean_skill]["q"], 
                "hint": question_bank[clean_skill]["hint"]
            })
        else:
            interview_prep.append({
                "skill": skill.strip(), 
                "question": f"Can you walk me through a complex project where you utilized {skill.strip()}?", 
                "hint": "Use the STAR method: Situation, Task, Action, Result."
            })
            
    return jsonify({"questions": interview_prep})

# ==========================================
# FEATURE 5: AI COVER LETTER
# ==========================================
@app.route('/generate_cover_letter', methods=['POST'])
def generate_cover_letter():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
        
    file = request.files['file']
    role = request.form.get('role', 'Software Engineer')
    company = request.form.get('company', 'your esteemed company')
    
    temp_path = os.path.join(tempfile.gettempdir(), file.filename)
    file.save(temp_path)
    
    try:
        raw_text = extract_text(temp_path)
        resume_text = raw_text.lower()
        
        lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
        user_name = lines[0].title() if lines else "[Your Name]"
        if len(user_name) > 30:
            user_name = "[Your Name]"

        email_match = re.search(r'[\w\.-]+@[\w\.-]+', resume_text)
        user_email = email_match.group(0) if email_match else "[Your Email]"

        phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4,5}', resume_text)
        user_phone = phone_match.group(0) if phone_match else "[Your Phone]"

    except Exception as e:
        return jsonify({"error": "Failed to read PDF. Try a different file."}), 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    tech_keywords = ['python', 'java', 'react', 'machine learning', 'sql', 'aws', 'docker', 'kubernetes', 'html', 'css', 'node']
    found_skills = [skill for skill in tech_keywords if skill in resume_text]
    
    if len(found_skills) >= 3:
        skills_str = f"{found_skills[0].title()}, {found_skills[1].title()}, and {found_skills[2].title()}"
    elif len(found_skills) > 0:
        skills_str = found_skills[0].title()
    else:
        skills_str = "modern software development methodologies"

    cover_letter = f"""Dear Hiring Manager,

I am writing to express my strong interest in the {role} position at {company}. With a solid foundation in computer science and hands-on experience in building scalable applications, I am eager to contribute to your engineering team.

In my recent academic and personal projects, I have developed a strong proficiency in {skills_str}. My focus has always been on writing clean, efficient code and solving complex logical problems. I am particularly drawn to {company} because of your commitment to innovation.

What sets me apart is my ability to rapidly learn new technology stacks and my dedication to continuous improvement. I am confident that my technical background makes me a strong fit for this role.

Thank you for considering my application. I have attached my resume for your review.

Sincerely,

{user_name}
{user_phone} | {user_email}"""

    return jsonify({"cover_letter": cover_letter})

if __name__ == '__main__':
    print("🚀 API Backend running on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)