import os
import google.generativeai as genai
from .logging import get_logger

logger = get_logger(__name__)

_MODEL = None
DEFAULT_API_KEY = "AIzaSyCOeZ4lKpLFZ-ep57Wzibtols8o-XglEZQ"

def _build_model(api_key: str):
    genai.configure(api_key=api_key)
    # Some older versions of google-generativeai do not expose GenerativeModel
    GM = getattr(genai, 'GenerativeModel', None)
    if GM is None:
        return None
    preferred = 'models/gemini-2.5-pro'
    try:
        return GM(preferred)
    except Exception:
        try:
            return GM('models/gemini-1.5-pro')
        except Exception:
            return None

def is_configured() -> bool:
    return _MODEL is not None

def initialize_gemini():
    """Initialize model using the fixed API key. Safe to call multiple times."""
    global _MODEL
    if _MODEL is not None:
        return _MODEL
    api_key = DEFAULT_API_KEY  # Always use fixed key
    try:
        _MODEL = _build_model(api_key)
    except Exception:
        _MODEL = None
    return _MODEL

def set_api_key(api_key: str) -> bool:
    """No-op since key is fixed. Returns False."""
    return False  # Key is fixed; no user setting allowed

def analyze_logs(model, logs):
    if not model:
        return ""
    try:
        prompt = (
            "You are a concise assistant. Read these installation logs and return a very short summary (1-2 lines) "
            "that mentions success/failure and the primary cause if any. Do not include code blocks or long text.\n\n"
            f"Logs:\n{logs}"
        )
        response = model.generate_content(prompt)
        text = (response.text or "").strip() if response else ""
        # Ensure max 2 lines
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        return " ".join(lines[:2]) if lines else ""
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return ""
