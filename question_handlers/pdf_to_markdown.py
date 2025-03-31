import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_path):
    # Open the PDF
    document = fitz.open(pdf_path)

    # Extract text from each page
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()

    return text

def convert_to_markdown(text):
    # Example: Convert headings based on line starts with 'H1', 'H2', etc.
    text = re.sub(r'^(.*)\n\s*-{3,}', r'# \1\n', text)  # Convert underline headings to Markdown

    # Example: Convert numbered lists
    text = re.sub(r'^\d+\.\s+(.*)', r'1. \1', text, flags=re.MULTILINE)

    # Example: Convert bullet points
    text = re.sub(r'^\* (.*)', r'* \1', text, flags=re.MULTILINE)

    # Remove extra newlines (if any) and other unnecessary spacing
    text = text.strip()

    return text

def pdf_to_markdown(pdf_path):
    """
    Convert a PDF file to Markdown format.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Markdown content extracted from the PDF.
    """
    # Extract text from the PDF
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()

    # Convert the extracted text to Markdown
    markdown_text = convert_to_markdown(text)

    return markdown_text
