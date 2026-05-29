from google import genai
from dotenv import load_dotenv
import fitz
import os

# Load environment variables
load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)

# PDF path
pdf_path = "research_papers/paper.pdf"

# Open PDF
document = fitz.open(pdf_path)

# Store extracted text
all_text = ""

# Read every page
for page_number in range(len(document)):
    page = document[page_number]
    text = page.get_text()
    all_text += text

# Prompt for Gemini
prompt = f"""
You are a research assistant.

Read the following research paper and summarize it into:

1. Background
2. Methods
3. Results
4. Conclusion

Explain clearly in simple language.

Research Paper:
{all_text}
"""

# Send to Gemini
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

# Print summary
print(response.text)