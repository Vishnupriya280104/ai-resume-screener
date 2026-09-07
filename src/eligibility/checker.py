from typing import Tuple, List

def verify_eligibility(skills: List[str], text_content: str) -> Tuple[bool, List[str]]:
    """
    Checks if the candidate meets the core hard constraints.
    Returns a tuple of (is_eligible, list_of_rejection_reasons).
    """
    rejection_reasons = []
    
    # Convert everything to lowercase text for case-insensitive robust checking
    combined_source = ( " ".join(skills) + " " + text_content ).lower()
    
    # 1. Look for Python Evidence
    python_keywords = ["python", "fastapi", "django", "flask", "pytorch"]
    has_python = any(keyword in combined_source for keyword in python_keywords)
    
    # 2. Look for AI / Agentic Evidence
    ai_keywords = ["langchain", "langgraph", "llm", "rag", "llama-index", "agent", "embedding", "vector search", "tool-calling"]
    has_ai = any(keyword in combined_source for keyword in ai_keywords)
    
    if not has_python:
        rejection_reasons.append("No evidence of Python stack found.")
    if not has_ai:
        rejection_reasons.append("No AI, RAG, or agentic systems project evidence found.")
        
    is_eligible = len(rejection_reasons) == 0
    return is_eligible, rejection_reasons
