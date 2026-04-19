import hashlib
import re
from typing import Optional
from app.services.ingest.types import LoadedDocument

def normalize_text(text: str) -> str:
    """
    Clean up whitespace and normalize line breaks.
    """
    # Replace multiple spaces with one
    text = re.sub(r'[ \t]+', ' ', text)
    # Normalize line breaks
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()

def generate_content_hash(text: str) -> str:
    """
    Generate a stable SHA256 hash of the normalized text.
    """
    normalized = normalize_text(text)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

def extract_fallback_title(doc: LoadedDocument) -> str:
    """
    Attempt to find a title from the first line or URI.
    """
    if doc.title:
        return doc.title
    
    lines = doc.text.split('\n')
    for line in lines:
        clean = line.strip('# \t')
        if clean:
            return clean[:100]
            
    return doc.source_uri.split('/')[-1] or "Untitled Document"
