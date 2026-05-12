# utils/text_normalizer.py

import re

def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = text.strip().lower()

    replacements = {
        "ي": "ی",
        "ك": "ک",
        "ة": "ه",
        "أ": "ا",
        "إ": "ا",
        "ؤ": "و",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r'\s+', ' ', text)
    return text
