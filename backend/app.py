from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import fitz

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

TECHNICAL_SKILLS_KEYWORD = "TECHNICAL SKILLS"
WORK_EXPERIENCE_KEYWORD = "WORK EXPERIENCE"

skills_dictionary = {
    "Python", "Java", "JavaScript", "C++", "C#", "Ruby", "Swift", "Kotlin", "PHP", "Go",
    "HTML", "CSS", "React", "Angular", "Vue.js", "Node.js", "Django", "Flask", "ASP.NET", "Express.js",
    "SQL", "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Oracle", "Redis", "Firebase", "Cassandra", "DynamoDB",
    "Git", "SVN", "Mercurial", "Bitbucket", "GitHub", "GitLab",
    "Spring", ".NET", "Ruby on Rails", "Laravel", "Symfony", "Hibernate", "Express.js", "Flask", "Django", "ASP.NET Core",
    "JUnit", "Selenium", "Pytest", "Mocha", "Jasmine", "RSpec", "JUnit", "NUnit", "TestNG",
    "Docker", "Kubernetes", "Jenkins", "Travis CI", "CircleCI", "Ansible", "Terraform", "AWS", "Azure", "Google Cloud",
    "AWS", "Azure", "Google Cloud", "IBM Cloud", "Oracle Cloud", "Alibaba Cloud", "DigitalOcean", "Heroku", "Firebase", "VMware",
    "Linux", "Windows", "macOS", "Unix", "FreeBSD", "Ubuntu", "CentOS", "Red Hat", "Debian", "Fedora",
    "Sorting", "Searching", "Linked Lists", "Stacks", "Queues", "Trees", "Graphs", "Dynamic Programming", "Big O Notation", "Hashing",
    "Inheritance", "Polymorphism", "Encapsulation", "Abstraction", "Design Patterns", "SOLID Principles", "UML", "Agile Methodologies", "Scrum", "Kanban",
    "Encryption", "Authentication", "Authorization", "SSL/TLS", "OWASP Top 10", "Cryptography", "Security Best Practices", "Penetration Testing", "Security Auditing", "Vulnerability Assessment",
    "Verbal Communication", "Written Communication", "Technical Writing", "Documentation", "Presentations", "Active Listening", "Team Collaboration", "Remote Collaboration", "Conflict Resolution", "Feedback Delivery",
    "Analytical Thinking", "Critical Thinking", "Debugging", "Troubleshooting", "Creative Thinking", "Decision Making", "Logical Reasoning", "Root Cause Analysis", "Problem Decomposition", "Risk Management",
    "Continuous Integration", "Continuous Deployment", "Continuous Delivery", "Build Automation", "Pipeline Orchestration", "Automated Testing", "Release Management", "Versioning", "Configuration Management", "Infrastructure as Code",
    "Android", "iOS", "React Native", "Flutter", "Xamarin", "SwiftUI", "JavaFX", "Ionic", "Cordova", "PhoneGap",
    "TensorFlow", "PyTorch", "Scikit-learn", "Keras", "OpenCV", "Natural Language Processing", "Computer Vision", "Deep Learning", "Reinforcement Learning", "Data Mining",
    "Microservices", "Service-Oriented Architecture (SOA)", "Monolithic Architecture", "Event-Driven Architecture", "Layered Architecture", "Component-Based Architecture", "Hexagonal Architecture", "Clean Architecture", "Domain-Driven Design (DDD)", "Model-View-Controller (MVC)",
    "Wireframing", "Prototyping", "User Research", "User Testing", "Interaction Design", "Visual Design", "Responsive Design", "Accessibility", "Usability", "Information Architecture",
    "Performance Tuning", "Memory Management", "Algorithm Optimization", "Database Optimization", "Network Optimization", "Concurrency", "Parallel Computing", "Load Balancing", "Scalability", "Caching",
    "Agile Methodologies", "Scrum", "Kanban", "Lean", "Extreme Programming (XP)", "Feature-Driven Development (FDD)", "Crystal", "Dynamic Systems Development Method (DSDM)", "Adaptive Software Development (ASD)", "Agile Unified Process (AUP)", "Disciplined Agile Delivery (DAD)",
    "API Documentation", "User Manuals", "System Manuals", "Tutorials", "Code Comments", "Architecture Diagrams", "Technical Specifications", "Release Notes", "Knowledge Base", "White Papers", "Problem-solving"
}


@app.route('/')
def hello():
    return 'hello'


@app.route('/preprocess', methods=['POST'])
def preprocess():

    if 'resume' not in request.files:
        return jsonify({'error': 'No file part'})

    resume = request.files['resume']
    if resume.filename == '':
        return jsonify({'error': 'No selected file'})

    filename = resume.filename
    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    resume.save(resume_path)

    # Extracting text
    try:
        text = extract_text_from_pdf(resume_path)
    except Exception as e:
        return jsonify({'error': f'Error extracting text: {e}'})

    # Extracting skills from technical skills section
    technical_skills_section = extract_technical_skills_section(text)
    if technical_skills_section:
        skills_mentioned = extract_skills_from_section(
            technical_skills_section)
        print("Skills mentioned:", skills_mentioned)
    else:
        skills_mentioned = []

    job_description = request.form.get('job_description', '')
    if job_description:
        skills_in_description = extract_skills_from_description(
            job_description, skills_dictionary)
        print("Skills in description:", skills_in_description)
    else:
        skills_in_description = []

    return jsonify({
        'message': 'Skills extracted successfully',
        'skills_from_resume': skills_mentioned,
        'skills_from_description': skills_in_description,
        'common_skills': list(set(skills_mentioned) & set(skills_in_description))
    })


def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf_file:
        for page_num in range(len(pdf_file)):
            page = pdf_file.load_page(page_num)
            text += page.get_text()
    return text


def extract_technical_skills_section(text):
    start_index = text.find(TECHNICAL_SKILLS_KEYWORD)
    if start_index != -1:
        end_index = text.find(WORK_EXPERIENCE_KEYWORD, start_index)
        if end_index != -1:
            return text[start_index:end_index]
    return None


def extract_skills_from_section(section):
    lines = section.split('\n')
    skills = []
    for line in lines:
        if line.strip() and ':' not in line:
            skills.extend(line.strip().split(','))
    return skills[1:]


def extract_skills_from_description(description, skills_dict):
    matching_skills = []
    # Convert the job description to lowercase for case-insensitive matching
    description_lower = description.lower()
    # Compare each skill in the dictionary with the lowercase job description
    for skill in skills_dict:
        if skill.lower() in description_lower:
            matching_skills.append(skill)
    return matching_skills


if __name__ == '__main__':
    app.run(debug=True, port=8000)
