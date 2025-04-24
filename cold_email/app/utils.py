import re

def clean_text(text):
    """
    Cleans the input text by removing unwanted characters and formatting.
    """
    # Remove HTML tags
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', text)

    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)

      # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s.,;:!?\'\"()\-]', '', text)

    # Remove extra spaces and newlines
    text = re.sub(r'\s+', ' ', text).strip()

  
    return text