from pydantic import BaseModel, ConfigDict

class usercreate(BaseModel):
    username: str
    password: str

class userlogin(BaseModel):
    username: str
    password: str

class jobres(BaseModel):
    id: int
    title: str
    description: str
    required_skills: str
    min_experience: float
    max_experience: float
    model_config = ConfigDict(from_attributes=True)

class matchres(BaseModel):
    job_title: str
    match_percentage: float
    skill_score: float
    experience_score: float
    matched_skills: list[str]
    missing_skills: list[str]
    user_experience: float
    required_experience: str
    note: str
