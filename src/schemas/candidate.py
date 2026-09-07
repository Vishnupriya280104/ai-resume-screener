from pydantic import BaseModel, Field
from typing import List, Optional

class LLMResumeExtraction(BaseModel):
    """The structured data structure Gemini must return for a resume"""
    candidate_name: str = Field(description="Full name of the candidate")
    email: Optional[str] = Field(description="Email address found in resume")
    github_url: Optional[str] = Field(description="Full GitHub profile URL if available")
    matched_skills: List[str] = Field(description="List of skills found that match Python, Backend, or AI stacks")
    
    # Raw scores extracted from resume text matching the weights
    ai_project_depth_score: int = Field(description="Score from 0 to 40 based on depth of AI/RAG/Agents projects")
    python_backend_score: int = Field(description="Score from 0 to 30 based on Python, FastAPI, and Database usage")
    cloud_fullstack_score: int = Field(description="Score from 0 to 15 based on Cloud (GCP/AWS), Docker, or Full Stack items")
    engineering_depth_score: int = Field(description="Score from 0 to 5 for non-trivial items like caching, testing, queues")
    
    is_thin_wrapper: bool = Field(description="True if AI projects are just basic API wrappers with no real backend logic")
    project_summary: str = Field(description="A short summary of their project work")
    strengths: List[str] = Field(description="Top 2-3 technical strengths shown")
    concerns: List[str] = Field(description="Any technical missing links or weaknesses")

class FinalCandidateResult(BaseModel):
    """The structure for the final output report"""
    rank: int
    candidate_name: str
    eligible: bool
    rejection_reasons: List[str]
    total_score: int
    score_breakdown: dict
    matched_skills: List[str]
    project_summary: str
    github_summary: str
    strengths: List[str]
    concerns: List[str]
