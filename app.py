import os
import shutil
import time
import sys
import magic
import PyPDF2
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QLabel, QLineEdit, QTextEdit, QProgressBar, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from config import (
    DOWNLOADS_FOLDER, SORTED_FOLDER, WINDOW_TITLE,
    WINDOW_SIZE, REFRESH_INTERVAL, PROCESSING_DELAY, AI_MODEL
)
from utils.logger import setup_logger, log_file_operation
from utils.file_analyzer import FileAnalyzer
from agents.file_agent import FileManagementAgent

# Load environment variables
load_dotenv()

# Get API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Please set OPENAI_API_KEY in your .env file")

# Directories
DOWNLOADS_FOLDER = Path(DOWNLOADS_FOLDER)
SORTED_FOLDER = Path(SORTED_FOLDER)
LOG_FILE = os.path.expanduser("~/SortedProjects/classification_log.txt")

# AI File Manager
chat = ChatOpenAI(
    model=AI_MODEL,
    openai_api_key=OPENAI_API_KEY,
    temperature=0.2
)

# Set up logging
logger = setup_logger("FileOrganizer")

class FileHandler(FileSystemEventHandler):
    def __init__(self, app):
        self.app = app
        self.file_analyzer = FileAnalyzer()
        self.file_agent = FileManagementAgent()
    
    def on_created(self, event):
        if not event.is_directory:
            file_path = Path(event.src_path)
            self.app.process_new_file(file_path)


def start_monitor(app):
    observer = Observer()
    event_handler = FileHandler(app)
    observer.schedule(event_handler, DOWNLOADS_FOLDER, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def track_download(file_path):
    """Process a file with AI assistance."""
    system_message = """You are an intelligent file management assistant. Your role is to sort and organize files."""
    
    prompt = f"Sort and organize {file_path} into a relevant project folder."
    
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=prompt)
    ]
    
    response = chat.invoke(messages).content
    return response


def classify_file(file_path):
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(file_path)
    if "pdf" in file_type:
        return "Documents"
    elif "image" in file_type:
        return "Images"
    elif "zip" in file_type or "compressed" in file_type:
        return "Archives"
    else:
        return "Other"


def organize_file(file_path):
    category = classify_file(file_path)
    project_folder = os.path.join(SORTED_FOLDER, category)
    os.makedirs(project_folder, exist_ok=True)
    shutil.move(file_path, os.path.join(project_folder, os.path.basename(file_path)))
    return f"File {file_path} moved to {project_folder}"


def open_file(file_path):
    if sys.platform == "darwin":  # macOS
        os.system(f"open {file_path}")
    elif sys.platform == "win32":  # Windows
        os.startfile(file_path)
    else:  # Linux
        os.system(f"xdg-open {file_path}")
    return f"Opened file {file_path}"


def rename_file(file_path, new_name):
    dir_name = os.path.dirname(file_path)
    new_path = os.path.join(dir_name, new_name)
    os.rename(file_path, new_path)
    return f"Renamed {file_path} to {new_name}"


def extract_zip(file_path):
    import zipfile
    extract_folder = os.path.join(os.path.dirname(file_path), "Extracted")
    os.makedirs(extract_folder, exist_ok=True)
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)
    return f"Extracted {file_path} to {extract_folder}"


class AIFileOrganizerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(200, 200, *WINDOW_SIZE)
        
        self.file_analyzer = FileAnalyzer()
        self.file_agent = FileManagementAgent()
        
        self.setup_ui()
        self.setup_file_monitoring()
        self.refresh_file_list()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Status section
        self.status_label = QLabel("📂 File Organizer Status: Active")
        layout.addWidget(self.status_label)
        
        # File list section
        self.file_label = QLabel("📂 Detected Files:")
        layout.addWidget(self.file_label)
        
        self.file_list = QListWidget()
        layout.addWidget(self.file_list)
        
        # Progress section
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Command section
        self.command_label = QLabel("📝 AI Assistant Commands:")
        layout.addWidget(self.command_label)
        
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Type a command, e.g., 'Organize files by project'")
        layout.addWidget(self.command_input)
        
        self.send_button = QPushButton("Send Command")
        self.send_button.clicked.connect(self.send_command)
        layout.addWidget(self.send_button)
        
        # Add execute organization button
        self.execute_button = QPushButton("🔄 Execute Organization")
        self.execute_button.clicked.connect(self.execute_organization)
        self.execute_button.setEnabled(False)  # Disabled by default until we have suggestions
        layout.addWidget(self.execute_button)
        
        # Output section
        self.output_label = QLabel("🤖 AI Assistant Output:")
        layout.addWidget(self.output_label)
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)
        
        # Refresh button
        self.refresh_button = QPushButton("🔄 Refresh File List")
        self.refresh_button.clicked.connect(self.refresh_file_list)
        layout.addWidget(self.refresh_button)
        
        self.setLayout(layout)
    
    def setup_file_monitoring(self):
        self.observer = Observer()
        self.event_handler = FileHandler(self)
        self.observer.schedule(self.event_handler, str(DOWNLOADS_FOLDER), recursive=False)
        self.observer.start()
        
        # Set up refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_file_list)
        self.refresh_timer.start(REFRESH_INTERVAL)
    
    def process_new_file(self, file_path: Path):
        """Process a newly downloaded file."""
        try:
            # Wait for file to be fully written
            time.sleep(PROCESSING_DELAY)
            
            # Analyze file
            file_info = self.file_analyzer.analyze_file(file_path)
            
            if "error" in file_info:
                self.log_message(f"Error analyzing file {file_path.name}: {file_info['error']}")
                return
            
            # Get AI analysis
            analysis = self.file_agent.analyze_file(file_info)
            
            # Log the analysis
            self.log_message(f"Analyzed file: {file_path.name}")
            self.log_message(f"Category: {file_info['category']}")
            self.log_message(f"AI Recommendations: {analysis['ai_analysis']}")
            
            # Move file to appropriate category folder
            category_folder = SORTED_FOLDER / file_info['category']
            category_folder.mkdir(exist_ok=True)
            
            new_path = category_folder / file_path.name
            file_path.rename(new_path)
            
            log_file_operation(logger, "move", file_path, True)
            self.log_message(f"Moved file to: {new_path}")
            
        except Exception as e:
            log_file_operation(logger, "process", file_path, False, e)
            self.log_message(f"Error processing file {file_path.name}: {str(e)}")
    
    def refresh_file_list(self):
        """Refresh the list of files in the downloads folder."""
        self.file_list.clear()
        for file_path in DOWNLOADS_FOLDER.glob("*"):
            if file_path.is_file():
                self.file_list.addItem(file_path.name)
    
    def send_command(self):
        """Send a command to the AI assistant."""
        command = self.command_input.text()
        if command:
            self.log_message(f"User: {command}")
            
            try:
                # Get all files in downloads
                files = []
                for file_path in DOWNLOADS_FOLDER.glob("*"):
                    if file_path.is_file():
                        file_info = self.file_analyzer.analyze_file(file_path)
                        if "error" not in file_info:
                            files.append(file_info)
                
                # Get AI suggestions
                self.current_suggestions = self.file_agent.suggest_organization(files)
                self.current_files = files
                self.log_message(f"AI: {self.current_suggestions['organization_suggestions']}")
                
                # Enable execute button if we have suggestions
                self.execute_button.setEnabled(True)
                
            except Exception as e:
                self.log_message(f"Error processing command: {str(e)}")
                self.execute_button.setEnabled(False)
    
    def execute_organization(self):
        """Execute the current organization suggestions."""
        try:
            if hasattr(self, 'current_suggestions') and hasattr(self, 'current_files'):
                self.log_message("Executing organization suggestions...")
                
                # Execute the organization
                results = self.file_agent.execute_organization(
                    self.current_files,
                    self.current_suggestions
                )
                
                # Log results
                if "error" in results:
                    self.log_message(f"❌ Error executing organization: {results['error']}")
                else:
                    if results["successful_moves"]:
                        self.log_message("✅ Successfully moved files:")
                        for move in results["successful_moves"]:
                            self.log_message(f"  • {move['source']} → {move['destination']}")
                    
                    if results["failed_moves"]:
                        self.log_message("❌ Failed to move files:")
                        for move in results["failed_moves"]:
                            self.log_message(f"  • {move['source']} → {move['destination']}")
                            self.log_message(f"    Error: {move['error']}")
                
                # Refresh the file list
                self.refresh_file_list()
                
                # Disable execute button until next command
                self.execute_button.setEnabled(False)
            else:
                self.log_message("❌ No organization suggestions available. Please send a command first.")
        except Exception as e:
            self.log_message(f"❌ Error executing organization: {str(e)}")
            self.execute_button.setEnabled(False)
    
    def log_message(self, message: str):
        """Log a message to the output text area."""
        self.output_text.append(message)
        self.output_text.verticalScrollBar().setValue(
            self.output_text.verticalScrollBar().maximum()
        )
    
    def closeEvent(self, event):
        """Handle application closure."""
        self.observer.stop()
        self.observer.join()
        event.accept()

if __name__ == "__main__":
    try:
        logger.info("Starting AI File Organizer")
        app = QApplication(sys.argv)
        main_window = AIFileOrganizerApp()
        main_window.show()
        sys.exit(app.exec())
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        sys.exit(1)