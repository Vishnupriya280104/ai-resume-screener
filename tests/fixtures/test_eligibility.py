import pytest
from src.eligibility.checker import verify_eligibility

def test_eligible_candidate():
    """Test that a candidate with both Python and AI skills passes the filter"""
    skills = ["Python", "FastAPI", "LangChain"]
    text = "Built a RAG pipeline using LangChain framework."
    
    is_eligible, reasons = verify_eligibility(skills, text)
    
    assert is_eligible is True
    assert len(reasons) == 0

def test_missing_python_rejected():
    """Test that a candidate with AI skills but NO Python is correctly rejected"""
    skills = ["Java", "Spring Boot", "LangChain"]
    text = "Built a RAG pipeline in Java environments."
    
    is_eligible, reasons = verify_eligibility(skills, text)
    
    assert is_eligible is False
    assert "No evidence of Python stack found." in reasons

def test_missing_ai_rejected():
    """Test that a pure Python developer with no AI experience is correctly rejected"""
    skills = ["Python", "Django", "PostgreSQL"]
    text = "Developed enterprise web apps with Django backend systems."
    
    is_eligible, reasons = verify_eligibility(skills, text)
    
    assert is_eligible is False
    assert "No AI, RAG, or agentic systems project evidence found." in reasons
