
import re

import pdfplumber

def extract_text_from_pdf(file_obj) -> str:
    text = ""

    # Ensure pointer is at start
    file_obj.seek(0)

    with pdfplumber.open(file_obj) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "

    return text.lower()



def clean_text(text: str) -> str:
    """
    Cleans resume text for NLP processing.
    """
    # Remove special characters
    text = re.sub(r"[^a-zA-Z0-9 ]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()

