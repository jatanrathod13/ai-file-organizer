#!/bin/bash

# AI File Organizer Setup Script
echo "🚀 Setting up AI File Organizer..."

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "Homebrew already installed ✅"
fi

# Install libmagic
echo "Installing libmagic..."
brew install libmagic

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv myenv

# Activate virtual environment
echo "Activating virtual environment..."
source myenv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    echo "# Replace this with your actual OpenAI API key" > .env
    echo "# You can get an API key from https://platform.openai.com/api-keys" >> .env
    echo "OPENAI_API_KEY=your_openai_api_key_here" >> .env
    echo "Please edit the .env file and add your OpenAI API key."
else
    echo ".env file already exists ✅"
fi

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p ~/SortedProjects/logs

echo "✅ Setup complete! You can now run the application with:"
echo "source myenv/bin/activate"
echo "python app.py" 