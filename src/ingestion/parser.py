import os
import pdfplumber

def extract_text_from_pdf(file_path: str) -> str:
    """Safely extracts text from a PDF file without crashing the pipeline."""
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        print(f" Error reading PDF {os.path.basename(file_path)}: {str(e)}")
        return ""
