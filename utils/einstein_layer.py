import re
from datetime import datetime
from openai import OpenAI
from utils.log_utils import save_log

# PII patterns
PII_PATTERNS = {
    "EMAIL": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "PHONE": r"\+?\d[\d\s\-]{8,}\d",
    "SSN": r"\b\d{3}-\d{2}-\d{4}\b"
}

def mask_sensitive_data(text):
    for tag, pattern in PII_PATTERNS.items():
        text = re.sub(pattern, f"[{tag}]", text)
    return text

def check_toxicity(text):
    client = OpenAI()
    try:
        response = client.moderations.create(model="omni-moderation-latest", input=text)
        flagged = response.results[0].flagged
        categories = response.results[0].categories
        return flagged, categories
    except Exception as e:
        # Fallback handling if moderation fails
        return False, {"error": str(e)}

def run_einstein_checks(text):
    masked = mask_sensitive_data(text)
    flagged, categories = check_toxicity(masked)

    log = {
        "original_text": text,
        "masked_text": masked,
        "flagged": flagged,
        "categories": {
            "harassment": getattr(categories, "harassment", False),
            "hate": getattr(categories, "hate", False),
            "self_harm": getattr(categories, "self_harm", False),
            "sexual": getattr(categories, "sexual", False),
            "violence": getattr(categories, "violence", False),
            "error": categories.get("error", None) if isinstance(categories, dict) else None,
        },
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    save_log(log)  # Save compliance log internally
    return masked, log