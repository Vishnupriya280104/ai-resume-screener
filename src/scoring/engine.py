from src.config.config import THIN_WRAPPER_PENALTY

def calculate_final_score(
    ai_score: int, 
    backend_score: int, 
    cloud_score: int, 
    eng_score: int, 
    github_score: int, 
    is_thin_wrapper: bool
) -> int:
    """Calculates the absolute total score, enforcing penalties and bounding values between 0-100."""
    
    total = ai_score + backend_score + cloud_score + eng_score + github_score
    
    if is_thin_wrapper:
        total -= THIN_WRAPPER_PENALTY
        
    # Clamp final results mathematically between absolute bounds 0 and 100
    return max(0, min(total, 100))
