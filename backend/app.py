import io
import re
import sqlite3
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from pdfminer.high_level import extract_text
import spacy
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from docx import Document

app = Flask(__name__)
# Allow requests from your local React app and your live Vercel app
CORS(app)

# --- LOAD NLP MODEL (Downloads automatically if missing) ---
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('careerpath.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT UNIQUE, password TEXT)''')
    conn.commit()
    conn.close()

init_db()

# ==========================================
# 1. AUTHENTICATION ENDPOINTS
# ==========================================
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = generate_password_hash(data.get('password'))

    try:
        conn = sqlite3.connect('careerpath.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        conn.commit()
        conn.close()
        return jsonify({"message": "Success", "user": {"name": name, "email": email}}), 200
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = sqlite3.connect('careerpath.db')
    c = conn.cursor()
    c.execute("SELECT name, password FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    conn.close()

    if user and check_password_hash(user[1], password):
        return jsonify({"message": "Success", "user": {"name": user[0], "email": email}}), 200
    return jsonify({"error": "Invalid credentials"}), 401

# ==========================================
# 2. SMART ANALYZER ENDPOINT
# ==========================================
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    role = request.form.get('role', 'AI/ML Engineer')
    github_user = request.form.get('github_user', '')
    
    # Extract Resume Text
    try:
        pdf_bytes = file.read()
        resume_text = extract_text(io.BytesIO(pdf_bytes))
    except Exception as e:
        return jsonify({"error": f"Failed to parse PDF: {str(e)}"}), 500
    
    # Define JD / Target Skills based on role
    domain_skills = {
        "AI/ML Engineer": "Python, Machine Learning, Deep Learning, TensorFlow, PyTorch, NLP, SQL, Data Science, Pandas, Numpy",
        "Full-Stack Developer": "JavaScript, React, Node.js, Express, MongoDB, SQL, HTML, CSS, Git, Docker, API",
        "Data Scientist": "Python, SQL, R, Machine Learning, Statistics, Data Visualization, Tableau, Pandas, Scikit-Learn",
        "Custom Job (Web Scraper)": "Python, Machine Learning, Deep Learning, SQL, Algorithms, Programming"
    }
    jd_text = domain_skills.get(role, domain_skills["AI/ML Engineer"])
    
    # GitHub API Integration (Optional)
    github_skills = []
    if github_user:
        try:
            gh_res = requests.get(f"https://api.github.com/users/{github_user}/repos?per_page=5")
            if gh_res.status_code == 200:
                for repo in gh_res.json():
                    lang = repo.get("language")
                    if lang and lang not in github_skills:
                        github_skills.append(lang)
                        resume_text += f" {lang}" # Add to resume text to boost score
        except:
            pass

    # Cosine Similarity Match Score
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
    score = round(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0] * 100)
    
    # Skill Gap Extraction using spaCy
    resume_doc = nlp(resume_text.lower())
    resume_tokens = set([token.text for token in resume_doc if not token.is_stop and token.is_alpha])
    
    jd_doc = nlp(jd_text.lower())
    jd_tokens = set([token.text for token in jd_doc if not token.is_stop and token.is_alpha])
    
    gaps = list(jd_tokens - resume_tokens)
    skill_gaps = [gap.title() for gap in gaps][:5] # Limit to top 5 gaps
    
    # Strategic Roadmap Generation
    study_plan = []
    try:
        weeks = int(request.form.get('timeline', '4'))
    except ValueError:
        weeks = 4
    
    if skill_gaps:
        chunk_size = max(1, len(skill_gaps) // weeks)
        for w in range(weeks):
            focus_skills = skill_gaps[w * chunk_size : (w + 1) * chunk_size]
            if focus_skills:
                study_plan.append({
                    "week": f"Week {w+1}",
                    "focus": f"Mastering {', '.join(focus_skills)}",
                    "tasks": [
                        f"Complete foundational tutorials on {focus_skills[0]}.",
                        f"Build a mini-project utilizing {', '.join(focus_skills)}.",
                        "Update resume and push code to GitHub."
                    ]
                })
    else:
         study_plan.append({
             "week": "Week 1-4",
             "focus": "Interview Prep & Advanced Projects",
             "tasks": ["Practice LeetCode problems.", "Conduct System Design Mock Interviews.", "Apply to Senior Roles."]
         })

    return jsonify({
        "match_score_percentage": score,
        "skill_gaps": skill_gaps,
        "study_plan": study_plan,
        "github_skills": github_skills
    }), 200

# ==========================================
# 3. MOCK ASSESSMENT SIMULATOR ENDPOINT
# ==========================================
QUESTION_BANK = {
    "python": [
        {"q": "What is the primary difference between a list and a tuple in Python?", "options": ["Lists are immutable; tuples are mutable", "Lists are mutable; tuples are immutable", "Tuples cannot store integers", "Lists cannot store strings"], "ans": 1, "exp": "Tuples are immutable sequences, while lists can be modified in-place."},
        {"q": "How does Python handle memory management?", "options": ["Manual deallocation only", "Reference counting and a generational garbage collector", "Purely static stack allocation", "Via the C++ runtime"], "ans": 1, "exp": "Python uses reference counting alongside a cyclic generational garbage collector."},
        {"q": "What is the Global Interpreter Lock (GIL)?", "options": ["A tool to lock files on disk", "A mutex that allows only one native thread to execute Python bytecode at a time", "A compiler optimization engine", "A security gate for pip packages"], "ans": 1, "exp": "The GIL prevents multi-core parallel execution of pure Python bytecode within a single process."},
        {"q": "What does the `yield` keyword do in a function?", "options": ["Terminates the program", "Pauses function execution and returns a generator iterator", "Allocates heap memory", "Imports a dynamic module"], "ans": 1, "exp": "Functions with `yield` produce generators, returning items lazily one at a time."},
        {"q": "Which method is called when an object is instantiated?", "options": ["__new__ then __init__", "__del__", "__str__", "__repr__"], "ans": 0, "exp": "`__new__` creates the object instance, and `__init__` initializes its state."},
        {"q": "What is the time complexity of looking up a key in a Python dict on average?", "options": ["O(n)", "O(log n)", "O(1)", "O(n^2)"], "ans": 2, "exp": "Python dictionaries are hash tables, offering O(1) average lookup time."},
        {"q": "What is a decorator in Python?", "options": ["A CSS styling utility", "A callable that modifies or extends another function/class", "A loop counter", "A syntax error handler"], "ans": 1, "exp": "Decorators wrap functions or methods using `@decorator_name` syntax to modify behavior."},
        {"q": "What is the output of `bool([])` in Python?", "options": ["True", "False", "None", "Error"], "ans": 1, "exp": "Empty sequences (lists, tuples, dicts, strings) evaluate to False in boolean contexts."},
        {"q": "What is the difference between `deepcopy` and `copy`?", "options": ["Deepcopy clones compound objects recursively; shallow copy inserts references", "No difference", "Copy works only on integers", "Deepcopy deletes the original object"], "ans": 0, "exp": "`copy.deepcopy()` duplicates all nested child objects recursively."},
        {"q": "Which built-in module provides support for asynchronous programming in Python?", "options": ["threading", "multiprocessing", "asyncio", "socket"], "ans": 2, "exp": "`asyncio` provides the event loop, coroutines (`async`/`await`), and task scheduling."}
    ],
    "sql": [
        {"q": "What is the main difference between WHERE and HAVING?", "options": ["WHERE filters rows before aggregation; HAVING filters aggregated groups", "HAVING works on single rows only", "WHERE cannot be used with SELECT", "They are identical"], "ans": 0, "exp": "`WHERE` filters before `GROUP BY`; `HAVING` filters aggregate functions after grouping."},
        {"q": "Which JOIN returns all rows from both tables whether matched or not?", "options": ["INNER JOIN", "LEFT JOIN", "FULL OUTER JOIN", "CROSS JOIN"], "ans": 2, "exp": "`FULL OUTER JOIN` retains records from both left and right tables with NULLs where keys don't match."},
        {"q": "What is an index primarily used for in relational databases?", "options": ["Encrypting records", "Speeding up query retrieval operations", "Normalizing tables", "Enforcing referential integrity"], "ans": 1, "exp": "Indexes (like B-Trees) accelerate query search times at the cost of additional write overhead."},
        {"q": "What does ACID stand for in database transactions?", "options": ["Action, Count, Index, Delete", "Atomicity, Consistency, Isolation, Durability", "Access, Control, Integrate, Deploy", "Asynchronous, Compact, Internal, Direct"], "ans": 1, "exp": "ACID guarantees transactional reliability in relational database engines."},
        {"q": "What does a UNIQUE constraint enforce?", "options": ["Prevents NULL values only", "Ensures all column values are distinct across rows", "Encrypts column values", "Restricts table creation"], "ans": 1, "exp": "A UNIQUE constraint guarantees distinctness across rows."},
        {"q": "Which SQL statement is used to remove a table structure entirely?", "options": ["DELETE TABLE", "DROP TABLE", "TRUNCATE TABLE", "CLEAR TABLE"], "ans": 1, "exp": "`DROP TABLE` removes both the data and the table schema definition permanently."},
        {"q": "What does TRUNCATE do compared to DELETE?", "options": ["TRUNCATE drops the schema", "TRUNCATE deletes all rows without logging individual row deletions, making it faster", "DELETE is always faster", "TRUNCATE requires a WHERE clause"], "ans": 1, "exp": "`TRUNCATE` is a DDL operation that empties the table quickly without row-by-row triggers."},
        {"q": "What is the difference between UNION and UNION ALL?", "options": ["UNION removes duplicate rows; UNION ALL keeps duplicates", "UNION ALL sorts the output", "UNION cannot combine tables", "They produce identical outputs"], "ans": 0, "exp": "`UNION` performs an implicit DISTINCT operation to remove duplicates; `UNION ALL` retains all records."},
        {"q": "Which normal form eliminates partial dependency on composite keys?", "options": ["1NF", "2NF", "3NF", "BCNF"], "ans": 1, "exp": "Second Normal Form (2NF) requires 1NF and no non-prime attribute depending on a subset of any candidate key."},
        {"q": "What is a foreign key?", "options": ["A key from an external database", "A field in one table that uniquely identifies a row of another table", "A primary key encrypted with SSL", "A transient auto-incrementing id"], "ans": 1, "exp": "A foreign key establishes a link and referential integrity between two tables."}
    ],
    "machine_learning": [
        {"q": "What is the primary cause of overfitting in ML models?", "options": ["Model is too simple", "Model learns training noise and captures patterns that do not generalize", "Dataset has too many rows", "Learning rate is too high"], "ans": 1, "exp": "Overfitting occurs when a high-capacity model fits the training noise rather than the underlying distribution."},
        {"q": "Which metric is best suited for an imbalanced classification problem?", "options": ["Accuracy", "F1-Score / PR-AUC", "Mean Squared Error", "R-Squared"], "ans": 1, "exp": "Accuracy is misleading in severe class imbalance; Precision, Recall, and F1-Score give a reliable picture."},
        {"q": "What is the purpose of regularisation techniques like L1 and L2?", "options": ["Speed up data download", "Penalize large model weights to prevent overfitting", "Increase model capacity", "Normalize labels"], "ans": 1, "exp": "L1 (Lasso) and L2 (Ridge) add weight penalty terms to the loss function to limit variance."},
        {"q": "What is the difference between Bagging and Boosting?", "options": ["Bagging trains models in sequence; Boosting trains in parallel", "Bagging trains independent models in parallel; Boosting trains models sequentially to correct past errors", "Bagging only works on neural networks", "Boosting does not use decision trees"], "ans": 1, "exp": "Random Forest is bagging (parallel voting); XGBoost/AdaBoost is sequential error correction."},
        {"q": "What does the vanishing gradient problem affect most?", "options": ["Linear regression", "Deep neural networks with saturating activations like Sigmoid/Tanh", "Decision trees", "K-Means"], "ans": 1, "exp": "Derivatives of sigmoid saturations approach zero, causing gradients to decay exponentially across deep layers."},
        {"q": "Which activation function is most widely used to avoid vanishing gradients in hidden layers?", "options": ["Sigmoid", "Step function", "ReLU", "Softmax"], "ans": 2, "exp": "ReLU provides constant gradient 1 for positive inputs, mitigating vanishing gradients."},
        {"q": "What is the primary difference between Supervised and Unsupervised learning?", "options": ["Supervised uses labeled data; Unsupervised operates on unlabeled data", "Unsupervised requires neural networks", "Supervised has no target variable", "Unsupervised only does regression"], "ans": 0, "exp": "Supervised learning maps inputs to known ground truth targets."},
        {"q": "What does PCA (Principal Component Analysis) achieve?", "options": ["Supervised classification", "Dimensionality reduction while maximizing variance", "Data encryption", "Hyperparameter tuning"], "ans": 1, "exp": "PCA projects high-dimensional data onto orthogonal axes of maximum variance."},
        {"q": "What does the Confusion Matrix diagonal represent?", "options": ["False Positives and False Negatives", "True Positives and True Negatives (Correct predictions)", "Total dataset count", "Standard deviation of errors"], "ans": 1, "exp": "The diagonal cells in a confusion matrix indicate correct predictions for each class."},
        {"q": "What is cross-validation primarily used for?", "options": ["Testing model generalization performance on unseen subsets", "Speeding up training epoch time", "Cleaning dirty database rows", "Compressing model weights"], "ans": 0, "exp": "K-fold cross-validation estimates out-of-sample performance and guards against validation bias."}
    ],
    "react": [
        {"q": "What is the primary role of the Virtual DOM in React?", "options": ["Direct manipulation of browser DOM nodes", "In-memory representation used to compute minimal DOM diffs for batch updates", "Database connection pooling", "Server routing"], "ans": 1, "exp": "React diffs the Virtual DOM against previous snapshots and reconciles changes efficiently."},
        {"q": "Which React hook is used to handle side-effects like data fetching?", "options": ["useState", "useEffect", "useMemo", "useContext"], "ans": 1, "exp": "`useEffect` runs side effects following component render cycles."},
        {"q": "Why should you never mutate state directly in React?", "options": ["JavaScript does not allow it", "React will not trigger a re-render because shallow reference checks detect no change", "It crashes Node.js", "It causes syntax errors"], "ans": 1, "exp": "React relies on immutability and object reference changes to trigger reconciliation."},
        {"q": "What is the purpose of the `key` prop in React lists?", "options": ["CSS identification", "Helps React identify which items have changed, been added, or been removed", "Enables encryption", "Connects to localStorage"], "ans": 1, "exp": "Keys provide identity to array elements during Virtual DOM reconciliation."},
        {"q": "What is the difference between `useMemo` and `useCallback`?", "options": ["useMemo caches computed values; useCallback caches function definitions", "They are identical", "useMemo only works on strings", "useCallback renders HTML"], "ans": 0, "exp": "`useMemo` memoizes return values; `useCallback` returns a memoized function instance."},
        {"q": "What is prop drilling in React?", "options": ["Drilling holes in hardware", "Passing props down through multiple layers of intermediate components that do not need them", "Using Redux for state", "Compiling TypeScript"], "ans": 1, "exp": "Prop drilling is passing state through intermediaries, often solved with Context API or state stores."},
        {"q": "What does `React.StrictMode` do in development?", "options": ["Prevents code from running", "Executes double renders and warns about deprecated APIs and side-effects", "Minifies code", "Enables production mode"], "ans": 1, "exp": "Strict mode intentionally mounts components twice in development to uncover impure lifecycles."},
        {"q": "When does a React component re-render by default?", "options": ["Only when the browser refreshes", "When its state changes or its parent component re-renders", "Every 5 seconds", "Only on click events"], "ans": 1, "exp": "State updates, prop changes, or parent re-renders trigger reconciliation on child components."},
        {"q": "What is the purpose of the Context API?", "options": ["Managing global or shared state without manually passing props at every level", "Replacing CSS stylesheets", "Making HTTP POST requests", "Creating database migrations"], "ans": 0, "exp": "Context shares data (like authenticated user, theme, or locale) throughout a subtree."},
        {"q": "What is JSX?", "options": ["A separate language entirely", "A syntax extension for JavaScript that looks like HTML and compiles to React.createElement calls", "A database engine", "A CSS preprocessor"], "ans": 1, "exp": "JSX allows writing declarative UI markup that compilers convert to JS objects."}
    ]
}

@app.route('/generate_interview', methods=['POST'])
def generate_interview():
    try:
        data = request.get_json() or {}
        skills = data.get('skills', [])
        
        selected_questions = []
        for s in skills:
            clean_s = s.strip().lower().replace(" ", "_").replace("/", "_")
            matched_key = None
            
            # Map user input to our static keys
            for key in QUESTION_BANK.keys():
                if key in clean_s or clean_s in key:
                    matched_key = key
                    break
            
            if matched_key:
                for q in QUESTION_BANK[matched_key]:
                    item = dict(q)
                    topic_title = matched_key.replace("_", " ").title()
                    item["topic"] = topic_title
                    selected_questions.append(item)
            else:
                # Fallback generic questions if skill not strictly in bank
                for i in range(1, 11):
                    selected_questions.append({
                        "topic": s.title(),
                        "q": f"Core concept check #{i} for {s}: How do you approach production scalability and error handling with {s}?",
                        "options": [
                            f"Standard error handling and logging pipelines for {s}",
                            f"Ignoring exceptions and relying on restarts",
                            f"Disabling concurrency guards",
                            f"Hardcoding configuration parameters"
                        ],
                        "ans": 0,
                        "exp": f"Enterprise development in {s} mandates structured exception handling, modular separation, and health logging."
                    })

        # Ensure we return exactly 10 questions max per request to avoid overwhelming UI
        return jsonify({"questions": selected_questions[:10], "total": 10}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================================
# 4. ATS RESUME SCANNER ENDPOINT
# ==========================================
@app.route('/review_resume', methods=['POST'])
def review_resume():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    try:
        pdf_bytes = file.read()
        text = extract_text(io.BytesIO(pdf_bytes))
    except Exception as e:
        return jsonify({"error": f"Failed to parse PDF: {str(e)}"}), 500
    
    structural_issues = []
    text_lower = text.lower()
    
    # Required ATS Sections
    if "education" not in text_lower:
        structural_issues.append("Missing 'Education' section header.")
    if "experience" not in text_lower and "employment" not in text_lower:
        structural_issues.append("Missing 'Experience' section header.")
    if "skills" not in text_lower:
        structural_issues.append("Missing 'Skills' section header.")
        
    # Spell Check Using TextBlob
    blob = TextBlob(text)
    spelling_alerts = []
    
    # Limit spell check to a sample of 50 words to prevent slow processing timeouts
    words = blob.words[:50]
    for word in words:
        if len(word) > 4:
            corrected = word.correct()
            # Ignore standard tech jargon that TextBlob doesn't know
            if word.lower() != corrected.lower() and word.lower() not in ["numpy", "pandas", "pytorch", "tensorflow", "github", "react", "flask", "js", "html", "css"]:
                spelling_alerts.append(f"Possible typo: '{word}' -> Did you mean '{corrected}'?")
                if len(spelling_alerts) >= 5: # Cap alerts so UI isn't flooded
                    break
    
    # Deduct points for errors
    score = 100 - (len(structural_issues) * 15) - (len(spelling_alerts) * 5)
    score = max(0, score)

    return jsonify({
        "score": score,
        "structural_issues": structural_issues,
        "spelling_alerts": list(set(spelling_alerts))
    }), 200

# ==========================================
# 5. DOWNLOAD TEMPLATE ENDPOINT
# ==========================================
@app.route('/download_template/<domain>', methods=['GET'])
def download_template(domain):
    doc = Document()
    clean_domain = domain.replace("_", " ")
    doc.add_heading(f'Resume Template: {clean_domain}', 0)
    
    doc.add_heading('Summary', level=1)
    doc.add_paragraph('Driven professional with expertise in building scalable applications...')
    
    doc.add_heading('Skills', level=1)
    doc.add_paragraph('Languages: Python, JavaScript, SQL\nFrameworks: React, Flask, Node.js')
    
    doc.add_heading('Experience', level=1)
    doc.add_paragraph('Company XYZ - Software Engineer\n- Developed REST APIs\n- Improved performance by 30%')
    
    doc.add_heading('Education', level=1)
    doc.add_paragraph('B.Tech in Computer Science\nMalla Reddy University')

    # Save to memory instead of disk
    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)
    
    return send_file(file_stream, as_attachment=True, download_name=f"{domain}_Template.docx")

# ==========================================
# 6. GENERATE COVER LETTER ENDPOINT
# ==========================================
@app.route('/generate_cover_letter', methods=['POST'])
def generate_cover_letter():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    role = request.form.get('role', 'Software Engineer')
    company = request.form.get('company', 'Hiring Company')
    
    try:
        pdf_bytes = file.read()
        text = extract_text(io.BytesIO(pdf_bytes))
    except Exception as e:
        return jsonify({"error": f"Failed to parse PDF: {str(e)}"}), 500
    
    # Regex Extraction for Contact Info
    emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
    email = emails[0] if emails else "[Your Email]"
    
    phones = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    phone = phones[0] if phones else "[Your Phone]"

    # NLP Extraction for Name
    doc = nlp(text)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    name = names[0] if names else "[Your Name]"

    cover_letter = f"""
{name}
{email} | {phone}

Dear Hiring Manager at {company},

I am writing to express my strong interest in the {role} position. With my robust technical background and hands-on experience developing data-driven, scalable applications, I am confident in my ability to deliver immediate value to {company}.

In my recent academic and professional projects, I have successfully designed decoupled architectures, integrated complex APIs, and implemented machine learning models to solve real-world problems. I am particularly drawn to {company} because of your commitment to innovation.

I have attached my resume for your review, which further details my technical stack and project history. I welcome the opportunity to discuss how my skills align with the goals of your engineering team.

Thank you for your time and consideration.

Sincerely,
{name}
"""
    return jsonify({"cover_letter": cover_letter}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)