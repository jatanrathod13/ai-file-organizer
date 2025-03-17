from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from pathlib import Path
from typing import Dict, Any, List
import json
from datetime import datetime
from config import OPENAI_API_KEY, AI_MODEL

class FileManagementAgent:
    def __init__(self):
        self.chat = ChatOpenAI(
            model=AI_MODEL,
            openai_api_key=OPENAI_API_KEY,
            temperature=0.2
        )
        
        self.system_message = """You are an intelligent file management assistant. Your role is to:
            1. Analyze files and suggest appropriate organization
            2. Provide insights about file content and relationships
            3. Suggest file naming conventions and organization patterns
            4. Help with file categorization and metadata management
            5. Provide recommendations for file organization based on content and usage patterns
            
            Always consider:
            - File type and content
            - Creation and modification dates
            - File relationships and dependencies
            - User's organization preferences
            - Security and privacy concerns"""
    
    def analyze_file(self, file_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get AI analysis and recommendations for a file.
        
        Args:
            file_info (Dict[str, Any]): Information about the file
            
        Returns:
            Dict[str, Any]: AI analysis and recommendations
        """
        prompt = f"""Analyze this file and provide recommendations:
        Name: {file_info['name']}
        Type: {file_info['mime_type']}
        Category: {file_info['category']}
        Size: {file_info['size']}
        Created: {file_info['created']}
        Modified: {file_info['modified']}
        Metadata: {json.dumps(file_info['metadata'], indent=2)}
        
        Please provide:
        1. Suggested organization location
        2. Recommended naming convention
        3. Related file types to consider
        4. Any security considerations
        5. Additional metadata suggestions"""
        
        messages = [
            SystemMessage(content=self.system_message),
            HumanMessage(content=prompt)
        ]
        
        response = self.chat.invoke(messages).content
        
        return {
            "timestamp": datetime.now().isoformat(),
            "file_info": file_info,
            "ai_analysis": response
        }
    
    def suggest_organization(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get AI suggestions for organizing multiple files.
        
        Args:
            files (List[Dict[str, Any]]): List of file information
            
        Returns:
            Dict[str, Any]: Organization suggestions
        """
        prompt = f"""Analyze these files and suggest an organization structure:
        {json.dumps(files, indent=2)}
        
        Please provide:
        1. Suggested folder structure
        2. File grouping recommendations
        3. Naming conventions
        4. Any patterns or relationships to consider
        5. Security and privacy recommendations"""
        
        messages = [
            SystemMessage(content=self.system_message),
            HumanMessage(content=prompt)
        ]
        
        response = self.chat.invoke(messages).content
        
        return {
            "timestamp": datetime.now().isoformat(),
            "files": files,
            "organization_suggestions": response
        }
    
    def generate_metadata(self, file_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate enhanced metadata suggestions for a file.
        
        Args:
            file_info (Dict[str, Any]): Information about the file
            
        Returns:
            Dict[str, Any]: Enhanced metadata suggestions
        """
        prompt = f"""Generate enhanced metadata suggestions for this file:
        {json.dumps(file_info, indent=2)}
        
        Please provide:
        1. Suggested tags
        2. Keywords
        3. Description
        4. Related files
        5. Usage recommendations"""
        
        messages = [
            SystemMessage(content=self.system_message),
            HumanMessage(content=prompt)
        ]
        
        response = self.chat.invoke(messages).content
        
        return {
            "timestamp": datetime.now().isoformat(),
            "file_info": file_info,
            "metadata_suggestions": response
        }
    
    def execute_organization(self, files: List[Dict[str, Any]], suggestions: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the organization suggestions by creating subfolders and moving files.
        
        Args:
            files (List[Dict[str, Any]]): List of file information
            suggestions (Dict[str, Any]): Organization suggestions from AI
            
        Returns:
            Dict[str, Any]: Results of the organization operation
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "successful_moves": [],
            "failed_moves": []
        }
        
        try:
            # Parse the AI suggestions to get the folder structure
            prompt = f"""Based on these organization suggestions, provide a JSON structure of where each file should go.
            Original files: {json.dumps(files, indent=2)}
            Suggestions: {suggestions['organization_suggestions']}
            
            Create a JSON object where:
            1. Keys are source file paths
            2. Values are destination paths (relative to the source directory)
            3. Use descriptive subfolder names based on projects or categories
            4. Keep the paths within the same parent directory
            
            Example format:
            {{
                "/path/to/file.txt": "Project A/docs/file.txt",
                "/path/to/image.png": "Project B/assets/image.png"
            }}"""
            
            messages = [
                SystemMessage(content=self.system_message),
                HumanMessage(content=prompt)
            ]
            
            response = self.chat.invoke(messages).content
            
            # Parse the JSON response
            try:
                file_moves = json.loads(response)
            except json.JSONDecodeError:
                # If the response isn't valid JSON, try to extract it from the text
                import re
                json_match = re.search(r'\{.*\}', response.replace('\n', ''), re.DOTALL)
                if json_match:
                    file_moves = json.loads(json_match.group())
                else:
                    raise ValueError("Could not parse AI suggestions into valid file moves")
            
            # Get the base directory from the first file
            if files and 'path' in files[0]:
                base_dir = str(Path(files[0]['path']).parent)
            else:
                raise ValueError("No valid files to organize")
            
            # Execute the moves
            for source, dest in file_moves.items():
                try:
                    source_path = Path(source)
                    # Make sure the destination is relative to the base directory
                    dest_path = Path(base_dir) / dest
                    
                    # Skip if source and destination are the same
                    if source_path == dest_path:
                        continue
                    
                    # Create destination directory if it doesn't exist
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Move the file
                    if source_path.exists():
                        # If destination exists, add a number to the filename
                        counter = 1
                        original_dest_path = dest_path
                        while dest_path.exists():
                            stem = original_dest_path.stem
                            suffix = original_dest_path.suffix
                            dest_path = original_dest_path.parent / f"{stem}_{counter}{suffix}"
                            counter += 1
                        
                        import shutil
                        shutil.move(str(source_path), str(dest_path))
                        results["successful_moves"].append({
                            "source": str(source_path),
                            "destination": str(dest_path)
                        })
                    else:
                        results["failed_moves"].append({
                            "source": str(source_path),
                            "destination": str(dest_path),
                            "error": "Source file does not exist"
                        })
                except Exception as e:
                    results["failed_moves"].append({
                        "source": str(source_path),
                        "destination": str(dest_path),
                        "error": str(e)
                    })
            
            return results
            
        except Exception as e:
            return {
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "successful_moves": [],
                "failed_moves": []
            } 