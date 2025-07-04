from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy
import nltk
import string
import os

app = Flask(__name__)
CORS(app)

# ✅ Dynamically load spaCy model (handles first-time deploys)
try:
    nlp = spacy.load('en_core_web_sm')
except:
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load('en_core_web_sm')

# ✅ Download NLTK stopwords safely (idempotent)
nltk.download('stopwords')

# Sample certification recommendations per skill
certifications_database = {
    "Python": ["Python for Everybody", "Google IT Automation with Python"],
    "SQL": ["SQL for Data Science", "Database Management Certification"],
    "JavaScript": ["JavaScript Algorithms and Data Structures", "Frontend Developer Certification"],
}

# Skill keywords database
skills_database = [
    "python", "sql", "javascript", "node.js", "react", "react native", "html", "css", "mongodb", "express.js",
    "pandas", "numpy", "matplotlib", "tensorflow", "pytorch", "scikit-learn", "opencv",
    "linux", "docker", "kubernetes", "jenkins", "aws", "azure", "google cloud",
    "firebase", "android", "ios", "network security", "ethical hacking", "cyber threat intelligence",
]

def extract_skills(resume_text):
    resume_text = resume_text.lower()
    resume_text = resume_text.translate(str.maketrans('', '', string.punctuation))
    extracted = [skill for skill in skills_database if skill in resume_text]
    return list(set(extracted))

def find_skill_gaps(extracted_skills, target_skills):
    return [skill for skill in target_skills if skill.lower() not in map(str.lower, extracted_skills)]

def recommend_certifications(missing_skills):
    return {skill: certifications_database.get(skill, []) for skill in missing_skills}

@app.route('/')
def home():
    return jsonify({"message": "Resume Analysis API is running"})

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    data = request.get_json()
    resume_text = data.get('resumeText', '')
    target_role = data.get('targetRole', '')

    # Target skills mapped by role
    role_skills = {
        "Full Stack Developer": ["javascript", "react", "node.js", "mongodb", "html", "css"],
        "Data Analyst": ["python", "sql", "pandas", "numpy", "matplotlib"],
        "DevOps Engineer": ["linux", "docker", "kubernetes", "jenkins", "aws"],
        "Cybersecurity Specialist": ["network security", "cyber threat intelligence", "ethical hacking"],
        "AI Engineer": ["python", "tensorflow", "pytorch", "opencv"],
        "Cloud Engineer": ["aws", "azure", "google cloud", "docker", "kubernetes"],
        "Mobile App Developer": ["react native", "android", "ios", "firebase"],
        "Machine Learning Engineer": ["python", "tensorflow", "pytorch", "scikit-learn"],
    }

    target_skills = role_skills.get(target_role, [])
    extracted_skills = extract_skills(resume_text)
    missing_skills = find_skill_gaps(extracted_skills, target_skills)
    recommended_certifications = recommend_certifications(missing_skills)

    result = {
        "extractedSkills": extracted_skills,
        "missingSkills": missing_skills,
        "recommendedCertifications": recommended_certifications
    }

    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port)
