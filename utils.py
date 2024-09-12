from screeninfo import get_monitors
import os

def get_screen_info():
    """Fetches screen size and brightness information."""
    screen_size = get_monitors()[0].width / 100  # Simplified screen size in inches
    brightness = 70  # Placeholder for brightness (actual implementation needs a proper library)
    return screen_size, brightness

def shutdown():
    """Executes the system shutdown command."""
    os.system("shutdown /s /t 1")
