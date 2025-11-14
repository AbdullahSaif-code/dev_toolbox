import os
import google.generativeai as genai
from .logging import get_logger

logger = get_logger(__name__)

_MODEL = None

def _build_model(api_key: str):
    if not api_key or api_key.startswith('AIzaSy'):
        logger.warning("Using demo API key - functionality limited")
    
    try:
        genai.configure(api_key=api_key)
        GM = getattr(genai, 'GenerativeModel', None)
        if GM is None:
            return None
        
        try:
            return GM('models/gemini-2.0-flash')
        except Exception:
            try:
                return GM('models/gemini-1.5-pro')
            except Exception:
                return None
    except Exception as e:
        logger.error(f"Model build error: {e}")
        return None

def is_configured() -> bool:
    return _MODEL is not None

def initialize_gemini():
    """Initialize model from environment or config file"""
    global _MODEL
    if _MODEL is not None:
        return _MODEL
    
    api_key = os.environ.get('GEMINI_API_KEY', '')
    
    if not api_key:
        config_dir = os.path.expanduser('~/.config/dev_toolbox')
        config_file = os.path.join(config_dir, '.gemini_key')
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    api_key = f.read().strip()
            except Exception as e:
                logger.warning(f"Could not read Gemini config: {e}")
    
    if api_key:
        _MODEL = _build_model(api_key)
    
    return _MODEL

def set_api_key(api_key: str) -> bool:
    """Save API key to config file"""
    try:
        config_dir = os.path.expanduser('~/.config/dev_toolbox')
        os.makedirs(config_dir, exist_ok=True)
        
        config_file = os.path.join(config_dir, '.gemini_key')
        with open(config_file, 'w') as f:
            f.write(api_key)
        os.chmod(config_file, 0o600)
        
        global _MODEL
        _MODEL = _build_model(api_key)
        return _MODEL is not None
    except Exception as e:
        logger.error(f"Failed to save API key: {e}")
        return False

def analyze_logs(model, logs):
    """Analyze successful installation logs"""
    if not model:
        return ""
    try:
        prompt = (
            "You are a technical assistant. Analyze these installation logs and provide a brief, "
            "professional summary (2-3 sentences max). Focus on what was successfully installed "
            "and any important next steps. Be concise.\n\n"
            f"Logs:\n{logs[-2000:]}"  # Last 2000 chars to avoid token limits
        )
        response = model.generate_content(prompt, safety_settings=[])
        text = (response.text or "").strip() if response else ""
        return text[:500]  # Limit response length
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return ""

def analyze_errors(model, logs):
    """Analyze error logs and provide actionable summary"""
    if not model:
        return ""
    try:
        prompt = (
            "You are a technical support specialist. Analyze these installation/operation logs that contain errors. "
            "Provide a brief, actionable summary (2-3 sentences) identifying:\n"
            "1. What went wrong\n"
            "2. The likely cause (in technical terms)\n"
            "3. A quick fix suggestion\n\n"
            "Be professional but concise.\n\n"
            f"Logs:\n{logs[-2000:]}"  # Last 2000 chars
        )
        response = model.generate_content(prompt, safety_settings=[])
        text = (response.text or "").strip() if response else ""
        return text[:500]  # Limit response length
    except Exception as e:
        logger.error(f"Gemini API error for error analysis: {e}")
        return ""
