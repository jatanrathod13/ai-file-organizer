import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
from utils.file_analyzer import FileAnalyzer
from agents.file_agent import FileManagementAgent
import shutil

# Load environment variables
load_dotenv()

def test_workflow():
    """Test the entire file organization workflow."""
    print("🚀 Testing AI File Organizer workflow...")
    
    # Create test directories
    home_dir = Path.home()
    downloads_dir = home_dir / "Downloads"
    sorted_dir = home_dir / "SortedProjects"
    sorted_dir.mkdir(exist_ok=True)
    
    # Create a sample file
    sample_file = downloads_dir / "test_sample.txt"
    print(f"Creating sample file at {sample_file}")
    with open(sample_file, 'w') as f:
        f.write("This is a test file for the AI File Organizer.")
    
    # Wait for file to be fully written
    time.sleep(1)
    
    # Initialize components
    file_analyzer = FileAnalyzer()
    file_agent = FileManagementAgent()
    
    # Analyze file
    print("Analyzing file...")
    file_info = file_analyzer.analyze_file(sample_file)
    print(f"File categorized as: {file_info['category']}")
    
    # Get AI analysis
    print("Getting AI recommendations...")
    analysis = file_agent.analyze_file(file_info)
    print(f"AI Recommendations: {analysis['ai_analysis']}")
    
    # Move file to appropriate category folder
    category_folder = sorted_dir / file_info['category']
    category_folder.mkdir(exist_ok=True)
    
    new_path = category_folder / sample_file.name
    print(f"Moving file to: {new_path}")
    shutil.copy(sample_file, new_path)  # Use copy instead of move for testing
    
    print("✅ Workflow test completed successfully!")
    print(f"Original file: {sample_file}")
    print(f"Organized file: {new_path}")

if __name__ == "__main__":
    test_workflow() 