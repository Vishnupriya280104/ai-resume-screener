import google.generativeai as genai
from src.config.config import GEMINI_API_KEY
from src.schemas.candidate import LLMResumeExtraction

# Initialize the Gemini API client using the free key
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    raise ValueError(" GEMINI_API_KEY is missing from your .env file!")

def analyze_resume_text(resume_text: str) -> LLMResumeExtraction:
    """Sends the resume text to Gemini and forces it to return structured scoring data."""
    
    # We use gemini-1.5-flash because it is free, fast, and supports structured outputs
    model = genai.GenerativeModel("gemini-3.6-flash")

    
    prompt = f"""
    You are an expert technical recruiter screening candidates for an SDE Intern position.
    Analyze the following resume text and score it strictly based on these rules:
    
    1. AI Project Depth (Max 40 points): Look for real AI architectures like LangChain, RAG, Agents, and Vector DBs.
    2. Python Backend (Max 30 points): Look for FastAPI, Async code, PostgreSQL, Redis.
    3. Cloud/Fullstack (Max 15 points): Look for Docker, GCP, AWS, React/Next.js.
    4. Engineering Depth (Max 5 points): Look for unit tests, caching, message queues, logging.
    
    Identify if their AI projects are just 'thin wrappers' (e.g., just calling the OpenAI API via an basic wrapper script with no backend/workflow layer).
    
    Resume Text:
    \"\"\"{resume_text}\"\"\"
    """
    
    try:
        # Call the Gemini API and force it to return the structural data matching our Pydantic scheme
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
                response_schema=LLMResumeExtraction,
                temperature=0.1 # Low temperature ensures strict adherence to facts
            )
        )
        # Parse the JSON string output back directly into our Pydantic Object structure
        return LLMResumeExtraction.model_validate_json(response.text)
    except Exception as e:
        print(f"Gemini processing failed: {str(e)}. Creating fallback template.")
        # Fallback profile so the script keeps running even if API fails for one resume
        return LLMResumeExtraction(
            candidate_name="Unknown (Parse Failure)",
            email=None,
            github_url=None,
            matched_skills=[],
            ai_project_depth_score=0,
            python_backend_score=0,
            cloud_fullstack_score=0,
            engineering_depth_score=0,
            is_thin_wrapper=False,
            project_summary="Failed to parse content via AI model.",
            strengths=[],
            concerns=["API error or formatting issue occurred during ingestion."]
        )
