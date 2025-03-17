import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directories
HOME_DIR = Path.home()
DOWNLOADS_FOLDER = Path("/Users/jatanrathod/SortedProjects/Dummy Downloads")
SORTED_FOLDER = Path("/Users/jatanrathod/SortedProjects/Dummy Downloads")  # Same as DOWNLOADS_FOLDER
LOG_DIR = SORTED_FOLDER / "logs"

# Create necessary directories
SORTED_FOLDER.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# Logging configuration
LOG_FILE = LOG_DIR / "file_organizer.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"

# File categories and their extensions
FILE_CATEGORIES = {
    "Documents": {
        "extensions": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx"],
        "description": "Text documents, spreadsheets, and presentations"
    },
    "Images": {
        "extensions": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp"],
        "description": "Image files"
    },
    "Archives": {
        "extensions": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
        "description": "Compressed archives"
    },
    "Code": {
        "extensions": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".h", ".php", ".rb"],
        "description": "Source code files"
    },
    "Data": {
        "extensions": [".csv", ".json", ".xml", ".yaml", ".yml", ".sql", ".db"],
        "description": "Data and configuration files"
    }
}

# AI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AI_MODEL = "gpt-3.5-turbo"

# File processing settings
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
PROCESSING_DELAY = 1  # 1 second
MAX_RETRIES = 3  # maximum number of retries for file operations

# UI Configuration
WINDOW_TITLE = "AI File Organizer"
WINDOW_SIZE = (800, 600)
REFRESH_INTERVAL = 5000  # 5 seconds 