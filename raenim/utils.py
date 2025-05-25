import platform

def _pick_mono_font() -> str:
    system = platform.system()
    if system == "Windows":
        return "Consolas"
    elif system == "Linux":
        return "Noto Mono"
    elif system == "Darwin":
        return "Menlo"
    else:
        return "Courier New"

MONO_FONT = _pick_mono_font()