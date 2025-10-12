import importlib
from .logging import get_logger

logger = get_logger(__name__)

def install_tools(tools):
    results = {}
    logs = []
    for tool in tools:
        try:
            module = importlib.import_module(f'app.installers.{tool}')
            func = getattr(module, f'install_{tool}')
            result = func()
            results[tool] = result
            logs.append(f"Tool: {tool} - {result}")
        except Exception as e:
            results[tool] = f"Error: {str(e)}"
            logs.append(f"Tool: {tool} - Error: {str(e)}")
    return results, logs
