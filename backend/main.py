from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from database import sessionlocal, base, engine
from schemas import usercreate, userlogin, jobres, matchres
from models import users, jobs
from resume_reader import extract_resume_text
from matcher import calculate_match

base.metadata.create_all(bind=engine)
app = FastAPI(title="Resume Job Matching API")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

def add_sample_jobs(db):
    if db.query(jobs).count() > 0:
        return
    sample = [
        jobs(title="Python Developer", description="Build Python applications and APIs.", required_skills="Python, SQL, FastAPI, REST API, Git", min_experience=0, max_experience=2),
        jobs(title="Frontend Developer", description="Build responsive web interfaces.", required_skills="HTML, CSS, JavaScript, React, Git", min_experience=0, max_experience=2),
        jobs(title="Backend Developer", description="Develop server-side services and databases.", required_skills="Python, SQL, REST API, FastAPI, MySQL", min_experience=1, max_experience=3),
        jobs(title="Full Stack Developer", description="Build frontend and backend features.", required_skills="HTML, CSS, JavaScript, React, Python, SQL", min_experience=1, max_experience=3),
        jobs(title="Data Analyst", description="Analyze data and create reports.", required_skills="Python, SQL, Excel, Power BI, Statistics", min_experience=0, max_experience=2),
        jobs(title="Java Developer", description="Build object-oriented Java applications.", required_skills="Java, OOP, SQL, REST API, Git", min_experience=0, max_experience=2),
        jobs(title="SQL Developer", description="Write queries and maintain databases.", required_skills="SQL, MySQL, Database Design, Joins, Indexes", min_experience=1, max_experience=3),
        jobs(title="Data Engineer", description="Build data pipelines and data processing workflows.", required_skills="Python, SQL, ETL, Data Warehousing, Git", min_experience=1, max_experience=3),
        jobs(title="QA Engineer", description="Test software and report defects.", required_skills="Testing, Python, SQL, API Testing, Postman", min_experience=0, max_experience=2),
        jobs(title="Software Engineer", description="Develop, test and maintain software.", required_skills="Python, OOP, DSA, SQL, Git", min_experience=0, max_experience=2),
    ]
    db.add_all(sample)
    db.commit()

@app.on_event("startup")
def startup():
    db = sessionlocal()
    try:
        add_sample_jobs(db)
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Resume Job Matching API is running"}

@app.post("/register")
def register(user: usercreate, db: Session = Depends(get_db)):
    if db.query(users).filter(users.username == user.username).first():
        raise HTTPException(status_code=409, detail="Username already exists")
    new_user = users(username=user.username, password_hash=generate_password_hash(user.password))
    db.add(new_user)
    db.commit()
    return {"message": "Registration successful"}

@app.post("/login")
def login(user: userlogin, db: Session = Depends(get_db)):
    found = db.query(users).filter(users.username == user.username).first()
    if not found or not check_password_hash(found.password_hash, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful", "username": found.username}

@app.get("/jobs", response_model=list[jobres])
def get_jobs(db: Session = Depends(get_db)):
    return db.query(jobs).order_by(jobs.title).all()

@app.post("/analyze", response_model=matchres)
async def analyze_resume(role: str = Form(...), experience: float = Form(...), resume: UploadFile = File(...), db: Session = Depends(get_db)):
    if experience < 0 or experience > 60:
        raise HTTPException(status_code=400, detail="Experience must be between 0 and 60 years")
    if not resume.filename:
        raise HTTPException(status_code=400, detail="Please choose a resume file")
    file_bytes = await resume.read()
    if len(file_bytes) > 5 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Resume file must be 5 MB or smaller")
    try:
        resume_text = extract_resume_text(resume.filename, file_bytes)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    selected_job = db.query(jobs).filter(jobs.title == role).first()
    if not selected_job:
        raise HTTPException(status_code=404, detail="Job role not found")
    return calculate_match(resume_text, selected_job, experience)
