# Resume–Job Matching System

Beginner-friendly project: FastAPI + React + MySQL. Features: register/login with Werkzeug password hashing, 10 job roles stored in MySQL, PDF/DOCX text extraction, role and experience input, explainable match score, matched/missing skills.

## Requirements
Python 3.10+, Node.js/npm, MySQL Server.

## 1. Create database
Run in MySQL Workbench:
```sql
CREATE DATABASE resume_matcher;
```

## 2. Backend (PowerShell)
```powershell
cd backend
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```
Edit `.env` with your MySQL password. Example:
`DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/resume_matcher`
Then run:
```powershell
uvicorn main:app --reload
```
Open http://127.0.0.1:8000/docs. Tables and 10 sample roles are created at startup.

## 3. Frontend (second terminal)
```powershell
cd frontend
npm install
npm run dev
```
Open the local URL Vite prints, usually http://localhost:5173.

## Match formula
Skill score = matching required skills / total required skills × 100. Experience score is 100 when the user-entered experience meets the role's minimum; otherwise it is proportional to that minimum. Final score = 80% skill score + 20% experience score. This is a keyword-based compatibility score, not a hiring probability. Experience is user-reported, not verified.

PDF extraction uses PyMuPDF; DOCX uses python-docx. Scanned/image-only PDFs need OCR, not included. Files are processed in memory and not saved permanently.

Security note: this is a learning demo. Login returns success but does not establish a persistent session or protect the analysis endpoint. React page changes are not backend authorization. For production, add a session/JWT and enforce per-user access in the backend.
