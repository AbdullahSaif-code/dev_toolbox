import os
import google.generativeai as genai
from .logging import get_logger

logger = get_logger(__name__)

_MODEL = None
DEFAULT_API_KEY = "AIzaSyCOeZ4lKpLFZ-ep57Wzibtols8o-XglEZQ"
CONFIG_DIR = os.path.expanduser("~/.config/dev_toolbox")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.env")

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

def _load_api_key_from_disk() -> str:
    try:
        if os.path.isfile(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('GEMINI_API_KEY='):
                        return line.split('=', 1)[1].strip()
    except Exception as e:
        logger.error(f"Failed to read API key from disk: {e}")
    return ""

def _save_api_key_to_disk(api_key: str) -> bool:
    try:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(CONFIG_PATH, 'w') as f:
            f.write(f"GEMINI_API_KEY={api_key}\n")
        return True
    except Exception as e:
        logger.error(f"Failed to save API key: {e}")
        return False

def is_configured() -> bool:
    return _MODEL is not None

def initialize_gemini():
    """Initialize model from env var if present. Safe to call multiple times."""
    global _MODEL
    if _MODEL is not None:
        return _MODEL
    # Prefer persisted key, then env, then default
    api_key = _load_api_key_from_disk() or os.getenv('GEMINI_API_KEY') or DEFAULT_API_KEY
    try:
        _MODEL = _build_model(api_key)
    except Exception:
        _MODEL = None
    return _MODEL

def set_api_key(api_key: str) -> bool:
    """Configure the model at runtime. Returns True if configured successfully."""
    global _MODEL
    try:
        _MODEL = _build_model(api_key)
        if _MODEL is None:
            return False
        _save_api_key_to_disk(api_key)
        return True
    except Exception:
        _MODEL = None
        return False

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
