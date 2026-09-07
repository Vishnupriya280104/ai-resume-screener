import requests
import re
from typing import Tuple

def extract_username(url: str) -> str:
    """Helper function to extract username from a GitHub URL link string."""
    if not url:
        return ""
    match = re.search(r"github\.com/([\w-]+)", url)
    return match.group(1) if match else ""

def enrich_from_github(github_url: str) -> Tuple[int, str]:
    """
    Queries the GitHub public API to pull data.
    Returns a tuple of (github_score, github_summary_string).
    Maximum score is capped at 10 points.
    """
    username = extract_username(github_url)
    if not username:
        return 0, "No public GitHub link provided on resume."
        
    url = f"https://github.com{username}/repos?per_page=10&sort=updated"
    
    try:
        # Simple fetch with a 5 second maximum timeout limit
        response = requests.get(url, timeout=5)
        
        if response.status_code == 404:
            return 0, "GitHub user account profile not found (404)."
        elif response.status_code == 403:
            return 0, "GitHub profile exists but API call hit a rate limit."
        elif response.status_code != 200:
            return 0, f"GitHub API failed with status code: {response.status_code}"
            
        repos = response.json()
        if not isinstance(repos, list):
            return 0, "GitHub profile parsed but returned zero repository data tracks."
            
        repo_count = len(repos)
        
        # Base activity calculations
        # Give points for having active visible repositories (up to 5 pts)
        activity_points = min(repo_count * 1, 5)
        # Give points for keywords in repo names (up to 5 pts)
        relevance_points = 0
        for r in repos:
            name = r.get("name", "").lower()
            desc = (r.get("description") or "").lower()
            if any(k in name or k in desc for k in ["python", "ai", "llm", "rag", "agent"]):
                relevance_points += 2
                
        relevance_points = min(relevance_points, 5)
        total_github_score = activity_points + relevance_points
        
        summary = f"Found {repo_count} public repositories. Calculated activity score: {activity_points}/5, framework alignment score: {relevance_points}/5."
        return total_github_score, summary
        
    except Exception as e:
        return 0, f"GitHub enrichment failed gracefully due to structural error: {str(e)}"
