# main.py
import requests
import time
import hmac
import hashlib
import json
import re

# ==== КОНФІГ ====
DEYE_PLANT_ID = "61177575"
COOKIES = "cookiesession1=678A3E0ECBD6568A58D0528B06FA31BA; language=en; Hm_lvt_b68bec9f23007294c0091c33ec0962b6=1742206611; HMACCOUNT=02E54756E37851C5; firstPrivacy=true; ucToken=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsib2F1dGgyLXJlc291cmNlIl0sInVzZXJfbmFtZSI6IjBfc2h0eXJtb3Zpa0BnbWFpbC5jb21fMiIsInNjb3BlIjpbImFsbCJdLCJkZXRhaWwiOnsib3JnYW5pemF0aW9uSWQiOjAsInRvcEdyb3VwSWQiOm51bGwsImdyb3VwSWQiOm51bGwsInJvbGVJZCI6LTEsInVzZXJJZCI6MTMwNzA1OTIsInZlcnNpb24iOjEwMDIsImlkZW50aWZpZXIiOiJzaHR5cm1vdmlrQGdtYWlsLmNvbSIsImlkZW50aXR5VHlwZSI6MiwibWRjIjoidWMiLCJhcHBJZCI6bnVsbCwibWZhU3RhdHVzIjpudWxsLCJ0ZW5hbnQiOiJEZXllIn0sImV4cCI6MTc0ODEwNTg0MiwibWRjIjoidWMiLCJhdXRob3JpdGllcyI6WyJhbGwiXSwianRpIjoiNzIzMTMxNjAtYTE3NS00MzExLTk5Y2QtNzJlOWFjNDdkNDNjIiwiY2xpZW50X2lkIjoidGVzdCJ9.UCulpJ_8y_ll7P3FhPQnGkxpuHNEGbUQrhC-ToOV2chJiX3Vu6iq1Fr7O1Jgog0LmhG17nVljIBqW6P3fJ1ABq3bLtlo2xBJSL8oF6PBoN5TBsb2VxICQEUq3YFxWsRHMxDiEOL3TZNarn16cesy6PepmFioZ_cDnt-zo0qcZvAwlBdvq8Vg4PB7MQTT9DKvUOU6zg9HKRmr3C_FO95NUs1kccT1qtURDb4tpV_LF6x5FXE8Jt0KOC84ikxXuvDEKyhB7Zah676F945J-zPCkIWFOa2o63rv2Gbb7lVM6bukgY-SYOdtZnFiOd5MFweSsdvwKleGePxDZ-eu0bp9ew; refreshTokenKey=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsib2F1dGgyLXJlc291cmNlIl0sInVzZXJfbmFtZSI6IjBfc2h0eXJtb3Zpa0BnbWFpbC5jb21fMiIsInNjb3BlIjpbImFsbCJdLCJhdGkiOiJmZTgxYTM2ZC1mNTJkLTQ2NTMtYWQ0NC1hOTk5YWZiMGUyMjYiLCJkZXRhaWwiOnsib3JnYW5pemF0aW9uSWQiOjAsInRvcEdyb3VwSWQiOm51bGwsImdyb3VwSWQiOm51bGwsInJvbGVJZCI6LTEsInVzZXJJZCI6MTMwNzA1OTIsInZlcnNpb24iOjEwMDIsImlkZW50aWZpZXIiOiJzaHR5cm1vdmlrQGdtYWlsLmNvbSIsImlkZW50aXR5VHlwZSI6MiwibWRjIjoiZXUiLCJhcHBJZCI6bnVsbCwibWZhU3RhdHVzIjpudWxsLCJ0ZW5hbnQiOiJEZXllIn0sImV4cCI6MTc0ODEwNTg0MywibWRjIjoiZXUiLCJhdXRob3JpdGllcyI6WyJhbGwiXSwianRpIjoiOTIwZjQ0YzktOWMyMC00YmQyLTk2NzctNjBkZDg1NzQyYzJjIiwiY2xpZW50X2lkIjoidGVzdCJ9.kQW2PHHryYOJCtt0Mj5dOrds7-f6BJxQJna_5DU73Ol8tR4lRQLmiJx3Y7UZLtX0RzoarWm3BN4qqGif2ysgt5FgEv6_e_rQtIlwwqgDDnH8YHVVfbYcA9VsrdCyfiXGf3-qBzj-eiWGwFTPwXlqE5V_ef-98yA1nUDJzm0DliSJyWUx-MTLL8Iw1CbIp4fW_u01rqAmldoAFp_yvgAnjhuIJqNh8mdoD9uJqZfcb1FETiSp9UDgsPIhjMHWtKHXelkF4y166Wh5T0gJgSw2snKjWBsYZ7Ro9OHDjZkj_B9YUQuQ1MAzSN_gl94M5gsNKS_kyjriFYrQihczDwEq8w; Hm_lpvt_b68bec9f23007294c0091c33ec0962b6=1742921951" 

TUYA_DEVICE_ID = "bfe03c619fbc80c952gn2u"
TUYA_CLIENT_ID = "ptcd8c94tj954u555sxf"
TUYA_CLIENT_SECRET = "99e64991fb6a49a18436d3a683a571aa"
TELEGRAM_BOT_TOKEN = "8185893432:AAFvOXh_5H-G-4ma8M7DohCNahszs6TRnek"
TELEGRAM_CHAT_ID = "@shtyrmovik"

# ==== ПАРАМЕТРИ ====
PV_ON_THRESHOLD = 300
PV_OFF_THRESHOLD = 100
TOLERANCE = 0.1  # 10%

# ==== ОТРИМАТИ ДАНІ З DEYE ====
def get_pv_power():
    headers = {
        "Cookie": COOKIES,
        "Referer": f"https://www.deyecloud.com/station/new-main?t={int(time.time()*1000)}&id={DEYE_PLANT_ID}",
    }
    url = f"https://www.deyecloud.com/maintain-s/station/{DEYE_PLANT_ID}"
    try:
        r = requests.get(url, headers=headers)
        lines = r.text.splitlines()
        pv_line = [line for line in lines if 'PV' in line and 'W' in line and 'Battery' not in line]
        if pv_line:
            match = re.search(r'(\d+\.?\d*)\s*W', pv_line[0])
            if match:
                return float(match.group(1))
    except Exception as e:
        send_telegram(f"❌ Deye Error: {e}")
    return 0

# ==== TELEGRAM ====
def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    try:
        requests.post(url, data=payload)
    except:
        pass

# ==== TUYA ====
def get_tuya_token():
    t = str(int(time.time() * 1000))
    sign_str = TUYA_CLIENT_ID + t
    sign = hmac.new(TUYA_CLIENT_SECRET.encode(), sign_str.encode(), hashlib.sha256).hexdigest().upper()
    headers = {
        'client_id': TUYA_CLIENT_ID,
        'sign': sign,
        't': t,
        'sign_method': 'HMAC-SHA256',
    }
    r = requests.get("https://openapi.tuyaeu.com/v1.0/token?grant_type=1", headers=headers)
    return r.json()['result']['access_token']

def control_tuya(turn_on: bool, token):
    url = f"https://openapi.tuyaeu.com/v1.0/devices/{TUYA_DEVICE_ID}/commands"
    headers = {
        "client_id": TUYA_CLIENT_ID,
        "access_token": token,
        "sign_method": "HMAC-SHA256",
        "t": str(int(time.time() * 1000)),
    }
    data = json.dumps({"commands": [{"code": "switch_1", "value": turn_on}]})
    r = requests.post(url, headers=headers, data=data)
    return r.json()

# ==== MAIN ====
def main():
    pv = get_pv_power()
    msg = f"🔆 PV: {pv:.0f} Вт"

    token = get_tuya_token()
    if pv > PV_ON_THRESHOLD:
        control_tuya(True, token)
        msg += " ➕ Вмикаю бойлер"
    elif pv < PV_OFF_THRESHOLD:
        control_tuya(False, token)
        msg += " ➖ Вимикаю бойлер"
    else:
        msg += " ⏸️ Без змін"

    send_telegram(msg)
    print(msg)

if __name__ == "__main__":
    main()
