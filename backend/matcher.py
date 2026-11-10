import re

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def calculate_match(resume_text: str, job, user_experience: float) -> dict:
    resume_text = " " + clean_text(resume_text) + " "
    required_skills = [x.strip() for x in job.required_skills.split(",") if x.strip()]
    matched, missing = [], []
    for skill in required_skills:
        skill_clean = clean_text(skill)
        if skill_clean and f" {skill_clean} " in resume_text:
            matched.append(skill)
        else:
            missing.append(skill)
    skill_score = len(matched) / len(required_skills) * 100 if required_skills else 0
    minimum = float(job.min_experience or 0)
    maximum = float(job.max_experience or minimum)
    if minimum <= 0 or user_experience >= minimum:
        experience_score = 100.0
    else:
        experience_score = max(0.0, min(100.0, user_experience / minimum * 100))
    score = skill_score * 0.8 + experience_score * 0.2
    return {
        "job_title": job.title,
        "match_percentage": round(score, 1),
        "skill_score": round(skill_score, 1),
        "experience_score": round(experience_score, 1),
        "matched_skills": matched,
        "missing_skills": missing,
        "user_experience": user_experience,
        "required_experience": f"{minimum:g}-{maximum:g} years",
        "note": "Keyword-based compatibility score, not a hiring probability. Experience is user-reported."
    }
