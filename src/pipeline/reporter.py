import json
import os

def generate_static_html_report(json_filepath: str, output_html_path: str):
    """Compiles a read-only minimalist evaluation summary table from batch logs."""
    if not os.path.exists(json_filepath):
        print(f" Source results file not found at {json_filepath}")
        return
        
    with open(json_filepath, 'r') as f:
        data = json.load(f)
        
    stats = data.get("batch_summary", {})
    results = data.get("results", [])
    
    # Filter for eligible shortlist profiles only, sorted by rank
    shortlist = [c for c in results if c.get("eligible")]
    shortlist.sort(key=lambda x: x.get("rank", 99))
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>SDE Intern Screening Summary</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.5; color: #333; max-width: 900px; margin: 40px auto; padding: 0 20px; }}
        h1 {{ border-bottom: 2px solid #eee; padding-bottom: 10px; font-size: 24px; }}
        .stats {{ background: #f8f9fa; border: 1px solid #e9ecef; padding: 15px; border-radius: 6px; margin-bottom: 25px; font-size: 14px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ text-align: left; padding: 10px; border-bottom: 1px solid #dee2e6; font-size: 14px; }}
        th {{ bg-color: #f1f3f5; font-weight: 600; color: #495057; }}
        .rank {{ font-weight: bold; color: #1c7ed6; }}
        .score {{ font-weight: 600; color: #2b8a3e; }}
        .skills {{ font-size: 12px; color: #666; font-family: monospace; }}
    </style>
</head>
<body>

    <h1>SDE Intern Screening Batch Summary</h1>
    
    <div class="stats">
        <strong>Batch Ingestion Execution Metrics:</strong><br>
        Total Processed Documents: {stats.get('total_resumes', 0)} | 
        Successfully Parsed: {stats.get('successfully_parsed', 0)} | 
        Eligible Shortlist: {stats.get('eligible', 0)} | 
        Filtered Out: {stats.get('rejected', 0)}
    </div>

    <h2>Ranked Eligible Shortlist</h2>
    <table>
        <thead>
            <tr>
                <th style="width: 80px;">Rank</th>
                <th>Candidate Name</th>
                <th style="width: 100px;">Total Score</th>
                <th>Score Breakdown (AI / Py / Cld / Git / Eng)</th>
                <th>Matched Technical Stacks</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for c in shortlist:
        b = c.get("score_breakdown", {})
        breakdown_str = f"{b.get('ai_project_depth',0)}/40 | {b.get('python_backend',0)}/30 | {b.get('cloud_fullstack',0)}/15 | {b.get('github',0)}/10 | {b.get('engineering_depth',0)}/5"
        
        html_content += f"""
            <tr>
                <td class="rank">#{c.get('rank', '-')}</td>
                <td><strong>{c.get('candidate_name', 'Unknown')}</strong></td>
                <td class="score">{c.get('total_score', 0)}/100</td>
                <td>{breakdown_str}</td>
                <td class="skills">{', '.join(c.get('matched_skills', []))}</td>
            </tr>
        """
        
    html_content += """
        </tbody>
    </table>

</body>
</html>
"""
    
    os.makedirs(os.path.dirname(output_html_path), exist_ok=True)
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f" Static report card generated directly at: {output_html_path}")

if __name__ == "__main__":
    generate_static_html_report("./output/results.json", "./output/report.html")
