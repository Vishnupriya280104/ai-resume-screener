import os
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Scoring Parameters (Total 100 Points)
SCORING_WEIGHTS = {
    "ai_project_depth": 40,
    "python_backend": 30,
    "cloud_fullstack": 15,
    "github": 10,
    "engineering_depth": 5
}

# Penalties
THIN_WRAPPER_PENALTY = 15  # Max penalty for shallow API-wrapper projects
