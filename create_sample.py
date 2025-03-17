import os
import sys
from pathlib import Path
import random
import string

def create_text_file(output_path, size_kb=10):
    """Create a sample text file of the specified size."""
    print(f"Creating sample text file at {output_path} ({size_kb}KB)")
    
    # Generate random content
    chars = string.ascii_letters + string.digits + string.punctuation + ' ' * 10
    content = ''.join(random.choice(chars) for _ in range(size_kb * 1024))
    
    # Write to file
    with open(output_path, 'w') as f:
        f.write(content)
    
    print(f"Sample file created successfully: {output_path}")

def main():
    if len(sys.argv) < 2:
        output_path = Path.home() / "Downloads" / "sample_file.txt"
    else:
        output_path = Path(sys.argv[1])
    
    size_kb = 10
    if len(sys.argv) >= 3:
        try:
            size_kb = int(sys.argv[2])
        except ValueError:
            print("Error: Size must be an integer (KB)")
            sys.exit(1)
    
    create_text_file(output_path, size_kb)

if __name__ == "__main__":
    main() 