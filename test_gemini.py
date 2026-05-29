from google import genai
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)

# Ask Gemini something
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Who is virat kohli?"
)

# Print response
print(response.text)