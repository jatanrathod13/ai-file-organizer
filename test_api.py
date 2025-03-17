import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check for API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ Error: OPENAI_API_KEY not found in .env file")
    exit(1)

# Set API key in environment
os.environ["OPENAI_API_KEY"] = api_key

from openai import OpenAI

try:
    # Initialize client
    client = OpenAI()
    
    # Test API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, are you working?"}
        ]
    )
    
    print("\n✅ API Key is working! Response:")
    print(response.choices[0].message.content)
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    print("Please check your API key and internet connection.") 