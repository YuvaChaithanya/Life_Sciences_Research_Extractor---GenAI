from google import genai
from dotenv import load_dotenv
import fitz
import os

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)

# PDF path
pdf_path = "research_papers/paper.pdf"

# Open PDF
document = fitz.open(pdf_path)

# Extract text
all_text = ""

for page_number in range(len(document)):
    page = document[page_number]
    text = page.get_text()
    all_text += text

# Ask user question
user_question = input("Ask a question about the research paper: ")

# Create prompt
prompt = f"""
You are a scientific research assistant.

Answer the user's question ONLY using the research paper content provided.

If the answer is not available in the paper, say:
'The paper does not provide this information.'

Research Paper:
{all_text}

User Question:
{user_question}
"""

# Send to Gemini
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

# Print answer
print("\nAnswer:")
print(response.text)