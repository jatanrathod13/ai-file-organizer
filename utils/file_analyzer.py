import magic
import PyPDF2
from pathlib import Path
from typing import Dict, Any, Optional
import json
import csv
from datetime import datetime
from config import FILE_CATEGORIES, MAX_FILE_SIZE

class FileAnalyzer:
    def __init__(self):
        self.mime = magic.Magic(mime=True)
        
    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Analyze a file and return detailed information about it.
        
        Args:
            file_path (Path): Path to the file
            
        Returns:
            Dict[str, Any]: Dictionary containing file analysis results
        """
        try:
            file_size = file_path.stat().st_size
            if file_size > MAX_FILE_SIZE:
                return {
                    "error": "File too large",
                    "size": file_size,
                    "max_size": MAX_FILE_SIZE
                }
            
            mime_type = self.mime.from_file(str(file_path))
            category = self._determine_category(file_path, mime_type)
            
            analysis = {
                "name": file_path.name,
                "path": str(file_path),
                "size": file_size,
                "mime_type": mime_type,
                "category": category,
                "created": datetime.fromtimestamp(file_path.stat().st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                "extension": file_path.suffix.lower(),
                "metadata": self._extract_metadata(file_path, mime_type)
            }
            
            return analysis
            
        except Exception as e:
            return {
                "error": str(e),
                "path": str(file_path)
            }
    
    def _determine_category(self, file_path: Path, mime_type: str) -> str:
        """Determine the category of a file based on its extension and mime type."""
        extension = file_path.suffix.lower()
        
        # First try to match by extension
        for category, info in FILE_CATEGORIES.items():
            if extension in info["extensions"]:
                return category
        
        # Then try to match by mime type
        mime_prefix = mime_type.split('/')[0]
        if mime_prefix == 'image':
            return "Images"
        elif mime_prefix == 'video' or mime_prefix == 'audio':
            return "Media"
        elif mime_prefix == 'text':
            if any(ext in extension for ext in ['.py', '.js', '.java', '.cpp', '.c', '.h', '.html', '.css', '.php', '.rb']):
                return "Code"
            return "Documents"
        elif mime_prefix == 'application':
            if 'pdf' in mime_type:
                return "Documents"
            elif 'zip' in mime_type or 'rar' in mime_type or '7z' in mime_type:
                return "Archives"
            elif any(ext in extension for ext in ['.csv', '.json', '.xml', '.yaml', '.yml', '.sql', '.db']):
                return "Data"
        
        return "Other"
    
    def _extract_metadata(self, file_path: Path, mime_type: str) -> Dict[str, Any]:
        """Extract metadata from files based on their type."""
        metadata = {}
        
        try:
            if mime_type == 'application/pdf':
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    metadata = {
                        'pages': len(pdf_reader.pages),
                        'title': pdf_reader.metadata.get('/Title', ''),
                        'author': pdf_reader.metadata.get('/Author', ''),
                        'subject': pdf_reader.metadata.get('/Subject', ''),
                        'keywords': pdf_reader.metadata.get('/Keywords', '')
                    }
            
            elif mime_type == 'text/csv':
                with open(file_path, 'r') as file:
                    csv_reader = csv.reader(file)
                    headers = next(csv_reader, [])
                    row_count = sum(1 for row in csv_reader)
                    metadata = {
                        'headers': headers,
                        'row_count': row_count
                    }
            
            elif mime_type == 'application/json':
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    metadata = {
                        'type': type(data).__name__,
                        'size': len(str(data))
                    }
        
        except Exception as e:
            metadata['error'] = str(e)
        
        return metadata 