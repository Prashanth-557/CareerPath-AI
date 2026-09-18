from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match_score(resume_skills, job_requirements):
    """
    Calculates the similarity percentage between resume skills and job requirements
    using TF-IDF and Cosine Similarity.
    """
    resume_text = " ".join(resume_skills)
    job_text = " ".join(job_requirements)
    
    if not resume_text or not job_text:
        return 0.0

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_text])
    
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    return round(similarity * 100, 2)

def identify_skill_gaps(resume_skills, job_requirements):
    """
    Identifies the exact skills missing from the resume that the job requires.
    """
    resume_set = set([skill.lower().strip() for skill in resume_skills])
    job_set = set([skill.lower().strip() for skill in job_requirements])
    
    missing_skills = list(job_set - resume_set)
    
    # Return the missing skills capitalized nicely for the frontend
    return [skill.title() for skill in missing_skills]

if __name__ == "__main__":
    print("ML Analyzer is ready!")