import spacy
from pdfminer.high_level import extract_text
import re

# Load the spaCy English language model
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    """Reads a PDF file and extracts all raw text."""
    try:
        text = extract_text(pdf_path)
        # Clean up excessive newlines
        cleaned_text = re.sub(r'\n+', '\n', text)
        return cleaned_text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_entities(text):
    """Uses NLP to find names, organizations, and an email."""
    doc = nlp(text)
    
    # Extract an email address using Regex
    email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    email = email_match.group(0) if email_match else "None found"

    # Extract named entities
    organizations = set([ent.text.replace('\n', ' ') for ent in doc.ents if ent.label_ == 'ORG'])
    names = set([ent.text for ent in doc.ents if ent.label_ == 'PERSON'])

    return {
        "Email": email,
        "Names": list(names)[:3], 
        "Organizations": list(organizations)
    }

if __name__ == "__main__":
    print("Parser is ready!")