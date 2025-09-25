from pydantic import BaseModel
from typing import List, Optional

class Offer(BaseModel):
    name: str
    value_props: List[str]
    ideal_use_cases: List[str]
    icp_industries: Optional[List[str]] = None

class Lead(BaseModel):
    name: str
    role: str
    company: str
    industry: str
    location: str
    linkedin_bio: str

class ScoredLead(Lead):
    intent: str
    score: int
    reasoning: str
