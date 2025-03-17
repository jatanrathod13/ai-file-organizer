import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from utils.file_analyzer import FileAnalyzer
import json

# Load environment variables
load_dotenv()

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_analyzer.py <file_path>")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"Error: File {file_path} does not exist")
        sys.exit(1)
    
    analyzer = FileAnalyzer()
    print(f"Analyzing file: {file_path}")
    
    try:
        analysis = analyzer.analyze_file(file_path)
        print(json.dumps(analysis, indent=2))
        print("\nAnalysis successful!")
    except Exception as e:
        print(f"Error analyzing file: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 