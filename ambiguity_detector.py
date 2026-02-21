AMBIGUOUS_TERMS = [
    "fast", "secure", "user-friendly", "scalable",
    "efficient", "robust", "reliable",
    "quick", "optimize", "easy"
]

def detect_ambiguities(text):
    found = []
    text_lower = text.lower()

    for word in AMBIGUOUS_TERMS:
        if word in text_lower:
            found.append(f"Ambiguous term detected: '{word}'")

    return found