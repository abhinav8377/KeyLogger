# Encrypted Keylogger PoC - Educational Research Project
- ⚠️ <i>ETHICAL DISCLAIMER</i> ⚠️ This keylogger is developed for **EDUCATIONAL AND SECURITY RESEARCH PURPOSES ONLY**.

### Legal and Ethical Guidelines: 
- ✅ Only use on systems you own or have explicit permission to test
- ❌ Never deploy on systems without proper authorization
- 🎓 Intended for cybersecurity education and penetration testing
- ⚖️ Users are responsible for compliance with local laws and regulations
- 📝 Requires explicit consent file (consent.txt) to operate

## 🚀 Features
### Core Functionality  
- **🔒 Encrypted Keystroke Capture** - Uses Fernet symmetric encryption
- **📊 Real-time Monitoring** - Captures keystrokes with timestamps
- **💾 Secure Storage** - Local encrypted log storage
- **🔄 Persistence** - Windows registry startup persistence

### Security & Safety  
- **🛑 Kill Switch** - Multiple termination methods
- **⏰ Runtime Limits** - Auto-termination after 24 hours
- **🚫 Sensitive App Detection** - Skips specified applications
- **📋 Consent Mechanism** - Requires explicit user consent
- **🧹 Auto Cleanup** - Removes old logs automatically

## 📦 Installation 
### Prerequisites 
- Python 3.7+
- Windows OS (for persistence features)
- Administrator privileges (recommended)

### Setup
```bash
# Clone or download the project
cd "Intern Project"

# Install dependencies
pip install -r requirements.txt

# Create consent file (required)
python keylogger.py
# Follow prompts to create consent.txt
```
## 🎯 Usage 
### Starting the Keylogger
```bash
python keylogger.py
```

### Project Structure
Intern Project/ <br>
├── keylogger.py        # Main keylogger application <br>
├── config.py           # Configuration settings <br>
├── utils.py            # Utility functions <br>
├── requirements.txt    # Python dependencies <br>
├── README.md           # This file <br>
└── report.md           # Detailed technical report <br>

## 🛑 Kill Switch Options 
- **Keyboard Shortcut**: Ctrl+Shift+Q
- **Kill Switch File**: Create KILL_SWITCH.txt in project directory
- **Runtime Limit**: Automatically stops after 24 hours
- **Consent Removal**: Delete consent.txt file

## 🔧 Configuration Key settings in config.py: 
- **Exfiltration Interval**: 300 seconds (5 minutes)
- **Max Log Size**: 1MB - **Log Retention**: 7 days

## 🛡️ Security Features 
- **AES Encryption**: All logs encrypted with Fernet
- **Base64 Encoding**: Secure data transmission
- **Key Management**: Automatic key generation and storage
- **Session Tracking**: Unique session IDs for each run
- **Metadata Logging**: System info and timestamps

## 📊 Monitoring & Logs 
### Generated Files 
- **encrypted_logs.dat** - Encrypted keystroke data
- **encryption.key** - Fernet encryption key
- **warnings.log** - System warnings and events
- **consent.txt** - User consent file

## 🔍 Educational Value 
This project demonstrates: 
- **Malware Analysis** techniques
- **Encryption/Decryption** implementation
- **Network Communication** protocols
- **Windows Registry** manipulation
- **Ethical Hacking** principles
- **Security Research** methodologies

#### ⚠️ Disclaimer This tool is provided "as is" for educational purposes only. The authors assume no responsibility for any misuse, damage, or legal consequences resulting from the use of this software. Users must ensure compliance with all applicable laws and regulations in their jurisdiction.

#### 📚 Further Reading For detailed technical analysis, architecture overview, and implementation details, see [report.md](report.md).
