import os
import google.generativeai as genai
from .logging import get_logger

logger = get_logger(__name__)

_MODEL = None

def _build_model(api_key: str):
    genai.configure(api_key=api_key)
    preferred = 'models/gemini-2.5-pro'
    try:
        return genai.GenerativeModel(preferred)
    except Exception:
        # Fallback for environments not supporting 2.5 yet
        return genai.GenerativeModel('models/gemini-1.5-pro')

def is_configured() -> bool:
    return _MODEL is not None

def initialize_gemini():
    """Initialize model from env var if present. Safe to call multiple times."""
    global _MODEL
    if _MODEL is not None:
        return _MODEL
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        logger.warning("GEMINI_API_KEY not set. Gemini features disabled.")
        return None
    try:
        _MODEL = _build_model(api_key)
    except Exception as e:
        logger.error(f"Failed to configure Gemini: {e}")
        _MODEL = None
    return _MODEL

def set_api_key(api_key: str) -> bool:
    """Configure the model at runtime. Returns True if configured successfully."""
    global _MODEL
    try:
        _MODEL = _build_model(api_key)
        return True
    except Exception as e:
        logger.error(f"Failed to set Gemini API key: {e}")
        _MODEL = None
        return False

def analyze_logs(model, logs):
    if not model:
        return "Gemini API not configured. Set GEMINI_API_KEY to enable log analysis."
    try:
        prompt = f"Analyze these installation logs for errors and suggest fixes:\n\n{logs}"
        response = model.generate_content(prompt)
        return response.text if response else "No response from Gemini."
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return f"Error querying Gemini: {str(e)}"
