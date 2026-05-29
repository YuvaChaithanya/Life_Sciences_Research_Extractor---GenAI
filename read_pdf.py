import fitz

# Path to PDF
pdf_path = "research_papers/paper.pdf"

# Open PDF
document = fitz.open(pdf_path)

# Empty string to store all text
all_text = ""

# Read every page
for page_number in range(len(document)):

    # Get page
    page = document[page_number]

    # Extract text from page
    text = page.get_text()

    # Add text to full text
    all_text += text

# Print extracted text
print(all_text[:3000])