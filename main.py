import argparse
import sys
from src.pipeline.runner import run_screening_pipeline

def main():
    parser = argparse.ArgumentParser(description="AI Resume Screening & Ranking CLI Tool")
    
    parser.add_argument(
        "--input", 
        default="./resumes", 
        help="Path targeting the source resumes directory folder location"
    )
    parser.add_argument(
        "--output", 
        default="./output/results.json", 
        help="Target output filepath location destination for JSON generation parameters"
    )
    
    args = parser.parse_args()
    
    print("==================================================")
    print(" Production AI Resume Screening & Ranking Engine")
    print("==================================================")
    
    run_screening_pipeline(args.input, args.output)

if __name__ == "__main__":
    main()
