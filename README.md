# AI File Organizer

An intelligent file management assistant that automatically organizes your downloads using AI-powered analysis and categorization.

## Features

- 🔍 Automatic file analysis and categorization
- 🤖 AI-powered organization suggestions
- 📁 Smart file categorization based on content and type
- 📊 Detailed logging of all operations
- 🎯 Customizable organization rules
- 🔄 Real-time file monitoring
- 📱 Modern PyQt6-based GUI

## Requirements

- Python 3.8 or higher
- macOS (tested on macOS 13+)
- OpenAI API key
- Homebrew (for installing system dependencies)

## Installation

### Quick Setup (macOS)

Run the setup script to automatically install all dependencies and set up the environment:

```bash
./setup.sh
```

Then edit the `.env` file to add your OpenAI API key.

### Manual Setup

1. Install system dependencies:
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required system libraries
brew install libmagic
```

2. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-file-organizer.git
cd ai-file-organizer
```

3. Create and activate a virtual environment:
```bash
python -m venv myenv
source myenv/bin/activate  # On macOS/Linux
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

5. Set up your OpenAI API key:
   - Get an API key from [OpenAI Platform](https://platform.openai.com/api-keys)
   - Edit the `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```
   - Make sure to replace `your_actual_api_key_here` with your real API key
   - Keep this file secure and never commit it to version control

6. Test your API key:
```bash
python test_api.py
```

## Usage

1. Start the application:
```bash
# Using the run script
./run.sh

# Or manually
source myenv/bin/activate
python app.py
```

2. The application will automatically:
   - Monitor your Downloads folder
   - Analyze new files as they are downloaded
   - Categorize files based on type and content
   - Move files to appropriate folders in ~/SortedProjects
   - Provide AI-powered organization suggestions

3. Use the GUI to:
   - View detected files
   - Send commands to the AI assistant
   - Get organization suggestions
   - Monitor file processing status

## Testing

You can test individual components of the application:

1. Test the OpenAI API connection:
```bash
python test_api.py
```

2. Test the file analyzer on a specific file:
```bash
python test_analyzer.py /path/to/your/file.pdf
```

3. Create a sample file for testing:
```bash
# Create a 10KB sample file in your Downloads folder
python create_sample.py

# Create a sample file with a specific path and size
python create_sample.py /path/to/output.txt 100
```

4. Test the entire workflow:
```bash
python test_workflow.py
```
This will create a sample file, analyze it, get AI recommendations, and move it to the appropriate folder.

## File Categories

Files are organized into the following categories:
- Documents (PDFs, Word docs, spreadsheets, etc.)
- Images (JPG, PNG, GIF, etc.)
- Archives (ZIP, RAR, 7Z, etc.)
- Media (MP4, MP3, etc.)
- Code (Python, JavaScript, etc.)
- Data (CSV, JSON, etc.)

## Troubleshooting

If you encounter any issues:

1. Make sure all system dependencies are installed:
```bash
brew install libmagic
```

2. Check that your OpenAI API key is correctly set in the `.env` file:
```bash
python test_api.py
```

3. If you get permission errors, you may need to:
```bash
sudo chown -R $(whoami) /usr/local/lib/python*
```

4. If the application fails to start, check the logs at:
```
~/SortedProjects/logs/file_organizer.log
```

5. If you get OpenAI API errors, make sure:
   - Your API key is valid and has not expired
   - You have sufficient credits in your OpenAI account
   - Your account has access to the GPT-4 model

## Logging

Detailed logs are stored in `~/SortedProjects/logs/file_organizer.log`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for providing the GPT models
- LangChain for the AI framework
- PyQt6 for the GUI framework
- The open-source community for various tools and libraries 