from google import genai
from dotenv import load_dotenv
import fitz
import os
import json

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

# Prompt
prompt = f"""
You are a scientific research assistant.

Read the following research paper and provide output in EXACTLY this format:

Background:
[Write background]

Methods:
[Write methods]

Results:
[Write results]

Conclusion:
[Write conclusion]

Research Paper:
{all_text}
"""

# Send to Gemini
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

summary_text = response.text

# Print summary
print(summary_text)

# Create dictionary
summary_data = {
    "summary": summary_text
}

# Save JSON
with open("output/summary.json", "w", encoding="utf-8") as json_file:
    json.dump(summary_data, json_file, indent=4)

# Save Markdown
with open("output/summary.md", "w", encoding="utf-8") as md_file:
    md_file.write("# Research Paper Summary\n\n")
    md_file.write(summary_text)

print("\nFiles saved successfully!")
print("JSON: output/summary.json")
print("Markdown: output/summary.md")