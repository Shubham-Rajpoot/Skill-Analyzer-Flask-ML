from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy
import nltk
from nltk.corpus import stopwords
import string

app = Flask(__name__)
CORS(app)

nlp = spacy.load('en_core_web_sm')
nltk.download('stopwords')

certifications_database = {
    "Python": ["Python for Everybody", "Google IT Automation with Python"],
    "SQL": ["SQL for Data Science", "Database Management Certification"],
    "JavaScript": ["JavaScript Algorithms and Data Structures", "Frontend Developer Certification"],
}

# skills_database = ["python", "sql", "javascript", "node.js", "react", "html", "css", "mongodb", "express.js"]
skills_database = [
    "python", "sql", "javascript", "node.js", "react", "react native", "html", "css", "mongodb", "express.js",
    "pandas", "numpy", "matplotlib", "tensorflow", "pytorch", "scikit-learn", "opencv",
    "linux", "docker", "kubernetes", "jenkins", "aws", "azure", "google cloud",
    "firebase", "android", "ios", "network security", "ethical hacking", "cyber threat intelligence",
]


# def extract_skills(resume_text):
#     doc = nlp(resume_text)
#     # tokens = [token.text.lower() for token in doc if token.is_alpha and not token.is_stop]
#       tokens = [token.text.lower().strip(string.punctuation) for token in doc if not token.is_stop]

#     print(f"Tokens: {tokens}")  
    
#     extracted = [token for token in tokens if token in skills_database]
    
#     print(f"Extracted Skills: {extracted}")  
    
#     return list(set(extracted))

def extract_skills(resume_text):
    resume_text = resume_text.lower()
    resume_text = resume_text.translate(str.maketrans('', '', string.punctuation))
    
    extracted = [skill for skill in skills_database if skill in resume_text]
    
    print(f"Extracted Skills: {extracted}")
    
    return list(set(extracted))


def find_skill_gaps(extracted_skills, target_skills):
    extracted_skills_lower = [skill.lower() for skill in extracted_skills]
    target_skills_lower = [skill.lower() for skill in target_skills]
    
    print(f"Target Skills: {target_skills_lower}") 
    print(f"Extracted Skills: {extracted_skills_lower}")  
    
    missing = [skill for skill in target_skills_lower if skill not in extracted_skills_lower]
    
    print(f"Missing Skills: {missing}") 
    
    return missing

def recommend_certifications(missing_skills):
    return {skill: certifications_database.get(skill, []) for skill in missing_skills}

# route for testing k liye
@app.route('/')
def home():
    return jsonify({"message": "Resume Analysis API is running"})

# Route to analyze resume k liye
@app.route('/analyze', methods=['POST'])
def analyze_resume():
    data = request.get_json()
    resume_text = data.get('resumeText', '')
    target_role = data.get('targetRole', '')

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
    # debug k liye 
    print(f"Extracted Skills: {extracted_skills}")  
    
    missing_skills = find_skill_gaps(extracted_skills, target_skills)
    
    print(f"Missing Skills: {missing_skills}") 
    
    recommended_certifications = recommend_certifications(missing_skills)

    result = {
        "extractedSkills": extracted_skills,
        "missingSkills": missing_skills,
        "recommendedCertifications": recommended_certifications
    }
    
    return jsonify(result)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5001))  # Use Render's PORT or default to 5001
    app.run(host='0.0.0.0', port=port)

