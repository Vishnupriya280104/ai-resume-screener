import os
import json
import pdfplumber
import docx
from src.llm.gemini_service import analyze_resume_text
from src.eligibility.checker import verify_eligibility
from src.github.enricher import enrich_from_github
from src.scoring.engine import calculate_final_score

def extract_text(file_path: str) -> str:
    """Reads content safely from PDF, DOCX, or TXT files."""
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    try:
        if ext == '.pdf':
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        elif ext == '.docx':
            doc = docx.Document(file_path)
            text = "\n".join([p.text for p in doc.paragraphs])
        elif ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as txt_file:
                text = txt_file.read()
        return text.strip()
    except Exception as e:
        print(f"Extraction failed for {os.path.basename(file_path)}: {str(e)}")
        return ""

def run_screening_pipeline(input_dir: str, output_filepath: str):
    """Executes ingestion, evaluation, scoring, and ranks multi-format resumes."""
    if not os.path.exists(input_dir):
        print(f" Input directory '{input_dir}' does not exist.")
        return
        
    # Accept multiple extensions simultaneously
    valid_extensions = ('.pdf', '.docx', '.txt')
    files = [f for f in os.listdir(input_dir) if f.lower().endswith(valid_extensions)]
    
    eligible_candidates = []
    rejected_candidates = []
    
    stats = {
        "total_resumes": len(files),
        "successfully_parsed": 0,
        "eligible": 0,
        "rejected": 0,
        "failed_unreadable": 0
    }
    
    print(f" Processing batch of {len(files)} multi-format files...")
    
    for file in files:
        full_path = os.path.join(input_dir, file)
        print(f" Reading: {file}")
        
        text = extract_text(full_path)
        if not text:
            stats["failed_unreadable"] += 1
            continue
            
        stats["successfully_parsed"] += 1
        extracted_data = analyze_resume_text(text)
        is_eligible, rejection_reasons = verify_eligibility(extracted_data.matched_skills, text)
        
        github_score = 0
        github_summary = "Skipped (Ineligible)"
        
        if is_eligible:
            stats["eligible"] += 1
            if extracted_data.github_url:
                github_score, github_summary = enrich_from_github(extracted_data.github_url)
            else:
                github_summary = "No profile link provided."
                
            final_score = calculate_final_score(
                ai_score=extracted_data.ai_project_depth_score,
                backend_score=extracted_data.python_backend_score,
                cloud_score=extracted_data.cloud_fullstack_score,
                eng_score=extracted_data.engineering_depth_score,
                github_score=github_score,
                is_thin_wrapper=extracted_data.is_thin_wrapper
            )
            
            eligible_candidates.append({
                "candidate_name": extracted_data.candidate_name,
                "file_processed": file,
                "eligible": True,
                "rejection_reasons": [],
                "total_score": final_score,
                "score_breakdown": {
                    "ai_project_depth": extracted_data.ai_project_depth_score,
                    "python_backend": extracted_data.python_backend_score,
                    "cloud_fullstack": extracted_data.cloud_fullstack_score,
                    "github": github_score,
                    "engineering_depth": extracted_data.engineering_depth_score
                },
                "matched_skills": extracted_data.matched_skills,
                "project_summary": extracted_data.project_summary,
                "github_summary": github_summary,
                "strengths": extracted_data.strengths,
                "concerns": extracted_data.concerns
            })
        else:
            stats["rejected"] += 1
            rejected_candidates.append({
                "candidate_name": extracted_data.candidate_name or file,
                "file_processed": file,
                "eligible": False,
                "rejection_reasons": rejection_reasons,
                "total_score": 0,
                "score_breakdown": {},
                "matched_skills": extracted_data.matched_skills,
                "project_summary": "Excluded due to hard criteria rules.",
                "github_summary": "Skipped.",
                "strengths": [],
                "concerns": []
            })

    eligible_candidates.sort(key=lambda x: x["total_score"], reverse=True)
    for idx, candidate in enumerate(eligible_candidates, start=1):
        candidate["rank"] = idx
    for candidate in rejected_candidates:
        candidate["rank"] = -1
        
    output_payload = {"batch_summary": stats, "results": eligible_candidates + rejected_candidates}
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    with open(output_filepath, 'w') as out_file:
        json.dump(output_payload, out_file, indent=2)
        
    print(f"\n Completed successfully! Summary: {stats}")
