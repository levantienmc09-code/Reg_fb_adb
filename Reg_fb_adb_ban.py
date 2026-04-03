#!/usr/bin/env python3
# File: facebook_full_auto.py

import uiautomator2 as u2
import time
import random
import requests
import os
import subprocess
import base64
import urllib.parse
import re
import string
import json
import sys
import io
import html
import uuid
import struct
from colorama import Fore, Style
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

os.system('cls' if os.name=='nt' else 'clear')

# ==========       MÀU       ==========
trang = Style.BRIGHT + Fore.WHITE
xanh = Style.BRIGHT + Fore.GREEN
do = Style.BRIGHT + Fore.RED

# ========== FILE CONFIG ==========
CONFIG_FILE = "config_reg_fb.json"

# Config mặc định
DEFAULT_CONFIG = {
    "delay_mua_mail_het_hang": 15,
    "delay_mua_mail_loi": 15,
    "delay_sau_khi_mua_mail": 0,
    "delay_mo_facebook": 15,
    "delay_chon_khong_cho_phep": 0.5,
    "delay_chon_toi_co_tai_khoan_roi": 0.5,
    "delay_click_tao_tk_lan1": 1,
    "delay_click_tao_tk_lan2": 0.5,
    "delay_chon_khong_cho_phep_lan2": 0.1,
    "delay_nhap_ho": 0.1,
    "delay_nhap_ten": 0.1,
    "delay_click_tiep_lan1": 1,
    "delay_click_chon": 0.5,
    "delay_click_tiep_lan2": 0.15,
    "delay_click_tiep_lan3": 1,
    "delay_nhap_tuoi": 0.1,
    "delay_click_tiep_lan4": 0.5,
    "delay_click_ok": 0.5,
    "delay_chon_gioi_tinh": 0.5,
    "delay_click_tiep_lan5": 1,
    "delay_nhap_sdt": 0.1,
    "delay_click_tiep_sdt": 1.5,
    "delay_click_tiep_tuc_tao_tk": 0.5,
    "delay_kiem_tra_sdt": 0.5,
    "delay_nhap_mat_khau": 1,
    "delay_click_tiep_sau_mk": 1.5,
    "delay_click_luu": 0.5,
    "delay_cho_toi_dong_y": 25,
    "delay_kiem_tra_loi": 1,
    "delay_click_tiep_tuc": 0.5,
    "delay_click_khong_cho_phep": 0.25,
    "delay_click_khong_cho_phep_lan2": 0,
    "delay_buoc_dung_fb": 0.1,
    "delay_mo_lai_fb": 10,
    "delay_click_toi_khong_nhan_duoc_ma": 0.75,
    "delay_click_xac_nhan_email": 0,
    "delay_nhap_email": 1,
    "delay_click_tiep_sau_email": 1,
    "delay_get_code": 2,
    "delay_nhap_code": 1,
    "delay_click_tiep_cuoi": 5,
    "delay_giua_cac_lan_chay": 5,
    "delay_thu_lai_khi_loi": 6,
    "so_lan_thu_mua_mail": 0,
    "so_lan_thu_get_code": 20,
    "mat_khau_fb": "@Letien09"
}

def doc_config():
    """Đọc file config, nếu không có thì tạo mới"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                # Cập nhật các key mới nếu thiếu
                for key, value in DEFAULT_CONFIG.items():
                    if key not in config:
                        config[key] = value
                return config
        except:
            return DEFAULT_CONFIG.copy()
    else:
        # Tạo file config mới
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4, ensure_ascii=False)
        return DEFAULT_CONFIG.copy()

def luu_config(config):
    """Lưu config vào file"""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

def nhap_delay(tieu_de, gia_tri_mac_dinh):
    """Nhập delay từ user"""
    try:
        nhap = input(f"   {tieu_de} ({gia_tri_mac_dinh} giây): ").strip()
        if nhap:
            return float(nhap)
        return gia_tri_mac_dinh
    except:
        return gia_tri_mac_dinh

def cau_hinh_delay():
    """Menu cấu hình delay"""
    print("\n" + "─"*70)
    print(f"{trang}⚙️  CẤU HÌNH DELAY")
    print("─"*70)
    
    config = doc_config()
    
    print("\n📌 CÁC THÔNG SỐ DELAY (giây):")
    print("─"*50)
    
    # Nhóm 0: Đặt Mật Khẩu
    print(f"\n{trang}【MẬT KHẨU FACEBOOK】{trang}")
    mat_khau_moi = input(f"   Nhập mật khẩu muốn đặt: ").strip()
    if mat_khau_moi:
        config["mat_khau_fb"] = mat_khau_moi
    # Nhóm 1: Mua mail
    print(f"\n{trang}【MUA MAIL】{trang}")
    config["delay_mua_mail_het_hang"] = nhap_delay("Delay khi hết hàng", config["delay_mua_mail_het_hang"])
    config["delay_mua_mail_loi"] = nhap_delay("Delay khi lỗi mua mail", config["delay_mua_mail_loi"])
    config["delay_sau_khi_mua_mail"] = nhap_delay("Delay sau khi mua mail", config["delay_sau_khi_mua_mail"])
    
    # Nhóm 2: Mở app
    print(f"\n{trang}【MỞ FACEBOOK】{trang}")
    config["delay_mo_facebook"] = nhap_delay("Delay mở Facebook", config["delay_mo_facebook"])
    
    # Nhóm 3: Các bước đăng ký
    print(f"\n{trang}【CÁC BƯỚC ĐĂNG KÝ】{trang}")
    config["delay_chon_khong_cho_phep"] = nhap_delay("Delay chọn Không cho phép", config["delay_chon_khong_cho_phep"])
    config["delay_chon_toi_co_tai_khoan_roi"] = nhap_delay("Delay chọn Tôi có tài khoản rồi", config["delay_chon_toi_co_tai_khoan_roi"])
    config["delay_click_tao_tk_lan1"] = nhap_delay("Delay click Tạo tài khoản lần 1", config["delay_click_tao_tk_lan1"])
    config["delay_click_tao_tk_lan2"] = nhap_delay("Delay click Tạo tài khoản lần 2", config["delay_click_tao_tk_lan2"])
    config["delay_chon_khong_cho_phep_lan2"] = nhap_delay("Delay chọn Không cho phép lần 2", config["delay_chon_khong_cho_phep_lan2"])
    config["delay_nhap_ho"] = nhap_delay("Delay sau nhập Họ", config["delay_nhap_ho"])
    config["delay_nhap_ten"] = nhap_delay("Delay sau nhập Tên", config["delay_nhap_ten"])
    config["delay_click_tiep_lan1"] = nhap_delay("Delay click Tiếp lần 1", config["delay_click_tiep_lan1"])
    config["delay_click_chon"] = nhap_delay("Delay click CHỌN", config["delay_click_chon"])
    config["delay_click_tiep_lan2"] = nhap_delay("Delay click Tiếp lần 2", config["delay_click_tiep_lan2"])
    config["delay_click_tiep_lan3"] = nhap_delay("Delay click Tiếp lần 3", config["delay_click_tiep_lan3"])
    config["delay_nhap_tuoi"] = nhap_delay("Delay sau nhập Tuổi", config["delay_nhap_tuoi"])
    config["delay_click_tiep_lan4"] = nhap_delay("Delay click Tiếp lần 4", config["delay_click_tiep_lan4"])
    config["delay_click_ok"] = nhap_delay("Delay click OK", config["delay_click_ok"])
    config["delay_chon_gioi_tinh"] = nhap_delay("Delay sau chọn giới tính", config["delay_chon_gioi_tinh"])
    config["delay_click_tiep_lan5"] = nhap_delay("Delay click Tiếp lần 5", config["delay_click_tiep_lan5"])
    
    # Nhóm 4: Nhập SĐT và MK
    print(f"\n{trang}【NHẬP SĐT & MK】{trang}")
    config["delay_nhap_sdt"] = nhap_delay("Delay sau nhập SĐT", config["delay_nhap_sdt"])
    config["delay_click_tiep_sdt"] = nhap_delay("Delay click Tiếp sau SĐT", config["delay_click_tiep_sdt"])
    config["delay_click_tiep_tuc_tao_tk"] = nhap_delay("Delay click Tiếp tục tạo TK", config["delay_click_tiep_tuc_tao_tk"])
    config["delay_kiem_tra_sdt"] = nhap_delay("Delay kiểm tra SĐT hợp lệ", config["delay_kiem_tra_sdt"])
    config["delay_nhap_mat_khau"] = nhap_delay("Delay sau nhập Mật khẩu", config["delay_nhap_mat_khau"])
    config["delay_click_tiep_sau_mk"] = nhap_delay("Delay click Tiếp sau MK", config["delay_click_tiep_sau_mk"])
    config["delay_click_luu"] = nhap_delay("Delay click Lưu", config["delay_click_luu"])
    config["delay_cho_toi_dong_y"] = nhap_delay("Delay chờ Tôi đồng ý", config["delay_cho_toi_dong_y"])
    config["delay_kiem_tra_loi"] = nhap_delay("Delay kiểm tra lỗi đăng ký", config["delay_kiem_tra_loi"])
    config["delay_click_tiep_tuc"] = nhap_delay("Delay click Tiếp tục", config["delay_click_tiep_tuc"])
    config["delay_click_khong_cho_phep"] = nhap_delay("Delay click Không cho phép", config["delay_click_khong_cho_phep"])
    config["delay_click_khong_cho_phep_lan2"] = nhap_delay("Delay click Không cho phép lần 2", config["delay_click_khong_cho_phep_lan2"])
    
    # Nhóm 5: Xác nhận email
    print(f"\n{trang}【XÁC NHẬN EMAIL】{trang}")
    config["delay_buoc_dung_fb"] = nhap_delay("Delay buộc dừng FB", config["delay_buoc_dung_fb"])
    config["delay_mo_lai_fb"] = nhap_delay("Delay mở lại FB", config["delay_mo_lai_fb"])
    config["delay_click_toi_khong_nhan_duoc_ma"] = nhap_delay("Delay click Tôi không nhận được mã", config["delay_click_toi_khong_nhan_duoc_ma"])
    config["delay_click_xac_nhan_email"] = nhap_delay("Delay click Xác nhận bằng email", config["delay_click_xac_nhan_email"])
    config["delay_nhap_email"] = nhap_delay("Delay sau nhập Email", config["delay_nhap_email"])
    config["delay_click_tiep_sau_email"] = nhap_delay("Delay click Tiếp sau Email", config["delay_click_tiep_sau_email"])
    config["delay_get_code"] = nhap_delay("Delay giữa các lần get code", config["delay_get_code"])
    config["delay_nhap_code"] = nhap_delay("Delay sau nhập Code", config["delay_nhap_code"])
    config["delay_click_tiep_cuoi"] = nhap_delay("Delay click Tiếp lần cuối", config["delay_click_tiep_cuoi"])
    
    # Nhóm 6: Vòng lặp
    print(f"\n{trang}【VÒNG LẶP】{trang}")
    config["delay_giua_cac_lan_chay"] = nhap_delay("Delay giữa các lần chạy", config["delay_giua_cac_lan_chay"])
    config["delay_thu_lai_khi_loi"] = nhap_delay("Delay thử lại khi lỗi", config["delay_thu_lai_khi_loi"])
    config["so_lan_thu_mua_mail"] = int(nhap_delay("Số lần thử mua mail (0=infinite)", config["so_lan_thu_mua_mail"]))
    config["so_lan_thu_get_code"] = int(nhap_delay("Số lần thử get code", config["so_lan_thu_get_code"]))
    

    luu_config(config)
    print("\n✅ Đã lưu cấu hình!")
    return config

# ========== PHẦN DONGVAN ==========
FILE_NAME = "Dongvan.txt"
HOTMAIL_FILE = "HOTMAIL_DONGVAN.txt"
GOM_HOTMAIL_FILE = "Gom_Hotmail_Dongvan.txt"
FB_ACCOUNT_FILE = "FB_NhaTrong.txt"
TELE_FILE = "Token-ID-Tele.txt"

def toast(text):
    try:
        os.system(f'termux-toast "{text}" &')
    except:
        pass
       
def format_money(money):
    return f"{money:,}".replace(",", ".")

def doc_tai_khoan():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            dong = f.readline().strip()
            if "|" in dong:
                return dong.split("|")
    return None, None

def luu_tai_khoan(tk, mk):
    with open(FILE_NAME, "w") as f:
        f.write(f"{tk}|{mk}")

def doc_email_tu_file():
    """Đọc email, password, refresh_token, client_id từ file Gom_Hotmail_Dongvan.txt"""
    if os.path.exists(GOM_HOTMAIL_FILE):
        with open(GOM_HOTMAIL_FILE, "r") as f:
            dong = f.readline().strip()
            if "|" in dong:
                parts = dong.split("|")
                if len(parts) >= 4:
                    return parts[0], parts[1], parts[2], parts[3], dong
    return None, None, None, None, None

def xoa_email_da_dung(dong_cu):
    """Xóa dòng đã dùng trong file Gom_Hotmail_Dongvan.txt"""
    if os.path.exists(GOM_HOTMAIL_FILE):
        with open(GOM_HOTMAIL_FILE, "r") as f:
            lines = f.readlines()
        with open(GOM_HOTMAIL_FILE, "w") as f:
            for line in lines:
                if line.strip() != dong_cu.strip():
                    f.write(line)

def doc_tele():
    """Đọc token và id tele từ file"""
    if os.path.exists(TELE_FILE):
        with open(TELE_FILE, "r") as f:
            lines = f.readlines()
            token = None
            id_tele = None
            for line in lines:
                if line.startswith("Token:"):
                    token = line.replace("Token:", "").strip()
                elif line.startswith("ID:"):
                    id_tele = line.replace("ID:", "").strip()
            return token, id_tele
    return None, None

def luu_tele(token, id_tele):
    """Lưu token và id tele vào file"""
    with open(TELE_FILE, "w") as f:
        f.write(f"Token: {token}\n")
        f.write(f"ID: {id_tele}\n")

def gui_tele(token, id_tele, noi_dung):
    """Gửi tin nhắn về Telegram"""
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": id_tele,
            "text": noi_dung,
            "parse_mode": "HTML"
        }
        requests.post(url, json=payload, timeout=10)
        return True
    except Exception as e:
        print(f"   ⚠️ Gửi tele thất bại: {e}")
        return False

def luu_hotmail(email, password, refresh_token, client_id):
    with open(HOTMAIL_FILE, "a") as f:
        f.write(f"{email}|{password}|{refresh_token}|{client_id}\n")
    print(f"   ✅ Đã lưu vào {HOTMAIL_FILE}: {email}|{password}|{refresh_token}|{client_id}")

def luu_tai_khoan_fb(uid, email, password, cookie, token):
    with open(FB_ACCOUNT_FILE, "a") as f:
        f.write(f"{uid} | {email} | {password} | {cookie} | {token}\n")
    print(f"   ✅ Đã lưu vào {FB_ACCOUNT_FILE}: {uid}|{email}")

def chay_lenh_adb(cmd):
    try:
        subprocess.run(f"adb {cmd}", shell=True, capture_output=True)
    except:
        pass

def khoa_xoay_man_hinh():
    chay_lenh_adb("shell settings put system accelerometer_rotation 0")

def xoa_du_lieu_fb():
    print("\n🗑️ ĐANG XÓA DỮ LIỆU FACEBOOK...")
    chay_lenh_adb("shell pm clear com.facebook.katana")
    time.sleep(0.2)
    chay_lenh_adb("shell pm clear com.facebook.katana")
    time.sleep(0.2)
    chay_lenh_adb("shell am force-stop com.facebook.katana")
    time.sleep(0.2)
    chay_lenh_adb("shell am force-stop com.facebook.katana")
    time.sleep(0.2)
    print("   ✅ Đã xóa dữ liệu và buộc dừng Facebook xong!")
    time.sleep(0.5)

# ========== PHẦN MUA MAIL ==========
def mua_mail(api_key, config):
    print("\n" + "─"*70)
    print("📧 MUA MAIL")
    print("─"*70)
    
    url_mua = f"https://api.dongvanfb.net/user/buy?apikey={api_key}&account_type=1&quality=1&type=full"
    
    lan_thu = 0
    max_thu = config["so_lan_thu_mua_mail"]
    
    while True:
        lan_thu += 1
        if max_thu > 0 and lan_thu > max_thu:
            print(f"\n❌ Đã thử {max_thu} lần nhưng không mua được mail!")
            return None, None, None, None
            
        print(f"\n🔄 Lần thử mua mail thứ {lan_thu}...")
        
        try:
            ket_qua = requests.get(url_mua)
            du_lieu = ket_qua.json()
            
            print(f"📊 Tin nhắn: {du_lieu.get('message')}")
            
            if "out of stock" in du_lieu.get('message', '').lower() or "hết hàng" in du_lieu.get('message', '').lower():
                delay = config["delay_mua_mail_het_hang"]
                print(f"⏰ Hết hàng rồi, Chờ {delay} giây rồi thử lại...")
                time.sleep(delay)
                continue
            
            if not du_lieu.get("status"):
                print(f"❌ Mua mail thất bại: {du_lieu.get('message')}")
                delay = config["delay_mua_mail_loi"]
                print(f"⏰ Chờ {delay} giây rồi thử lại...")
                time.sleep(delay)
                continue
            
            thong_tin = du_lieu.get("data", {})
            print(f"📦 Mã đơn hàng: {thong_tin.get('order_code')}")
            print(f"💰 Tổng tiền: {format_money(thong_tin.get('total_amount', 0))}")
            print(f"💵 Số dư còn lại: {format_money(thong_tin.get('balance', 0))}")
            
            for acc in thong_tin.get("list_data", []):
                phan_tach = acc.split("|")
                email = phan_tach[0]
                mat_khau_mail = phan_tach[1]
                refresh_token = phan_tach[2]
                client_id = phan_tach[3]
                
                print("\n" + "─"*70)
                print("📧 MAIL NHẬN ĐƯỢC")
                print("─"*70)
                print(f"Email: {email}")
                print(f"Mật khẩu: {mat_khau_mail}")
                print(f"Refresh Token: {refresh_token}")
                print(f"Client ID: {client_id}")
                print("─"*70)
                
                luu_hotmail(email, mat_khau_mail, refresh_token, client_id)
                delay = config["delay_sau_khi_mua_mail"]
                if delay > 0:
                    print(f"⏰ Chờ {delay} giây...")
                    time.sleep(delay)
                return email, mat_khau_mail, refresh_token, client_id
            
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            delay = config["delay_mua_mail_loi"]
            print(f"⏰ Chờ {delay} giây rồi thử lại...")
            time.sleep(delay)
            continue


# ========== PHẦN FACEBOOK LOGIN ==========
APP_TOKEN = "350685531728|62f8ce9f74b12f84c123cc23437a4a32"

class Facebook:
    def MaHoaMatKhau(self, mat_khau):
        try:
            url = 'https://b-graph.facebook.com/pwd_key_fetch'
            params = {
                'version': '2',
                'flow': 'CONTROLLER_INITIALIZATION',
                'method': 'GET',
                'fb_api_req_friendly_name': 'pwdKeyFetch',
                'fb_api_caller_class': 'com.facebook.auth.login.AuthOperations',
                'access_token': '438142079694454|fc0a7caa49b192f64f6f5a6d9643bb28'
            }
            response = requests.post(url, params=params).json()
            public_key = response.get('public_key')
            key_id = str(response.get('key_id', '25'))
            
            rand_key = get_random_bytes(32)
            iv = get_random_bytes(12)
            
            pubkey = RSA.import_key(public_key)
            cipher_rsa = PKCS1_v1_5.new(pubkey)
            encrypted_rand_key = cipher_rsa.encrypt(rand_key)
            
            cipher_aes = AES.new(rand_key, AES.MODE_GCM, nonce=iv)
            current_time = int(time.time())
            cipher_aes.update(str(current_time).encode("utf-8"))
            encrypted_passwd, auth_tag = cipher_aes.encrypt_and_digest(mat_khau.encode("utf-8"))
            
            buf = io.BytesIO()
            buf.write(bytes([1, int(key_id)]))
            buf.write(iv)
            buf.write(struct.pack("<h", len(encrypted_rand_key)))
            buf.write(encrypted_rand_key)
            buf.write(auth_tag)
            buf.write(encrypted_passwd)
            encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
            return f"#PWD_FB4A:2:{current_time}:{encoded}"
        except Exception as e:
            raise Exception(f"Lỗi khi mã hóa mật khẩu: {e}")
    
    @staticmethod
    def _tao_machine_id():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=24))
    
    def __init__(self, email=None, mat_khau=None, auth=None):
        self.email = email
        self.mat_khau = self.MaHoaMatKhau(mat_khau) if mat_khau else None
        self.auth = auth.replace(" ", "") if auth else None
        self.URL = "https://b-graph.facebook.com/auth/login"
        self.API_KEY = "882a8490361da98702bf97a021ddc14d"
        self.SIG = "214049b9f17c38bd767de53752b53946"
        self.device_id = str(uuid.uuid4())
        self.adid = str(uuid.uuid4())
        self.secure_family_device_id = str(uuid.uuid4())
        self.machine_id = self._tao_machine_id()
        self.jazoest = ''.join(random.choices(string.digits, k=5))
        self.HEADERS = {
            "content-type": "application/x-www-form-urlencoded",
            "x-fb-net-hni": "45201",
            "zero-rated": "0",
            "x-fb-sim-hni": "45201",
            "x-fb-connection-quality": "EXCELLENT",
            "x-fb-friendly-name": "authenticate",
            "x-fb-connection-bandwidth": "78032897",
            "x-tigon-is-retry": "False",
            "authorization": "OAuth null",
            "x-fb-connection-type": "WIFI",
            "x-fb-device-group": "3342",
            "priority": "u=3,i",
            "x-fb-http-engine": "Liger",
            "x-fb-client-ip": "True",
            "x-fb-server-cluster": "True",
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"350685531728","retry_attempt":"0"},"application_tags":"unknown"}',
            "user-agent": "Dalvik/2.1.0 (Linux; U; Android 9; 23113RKC6C Build/PQ3A.190705.08211809) [FBAN/FB4A;FBAV/417.0.0.33.65;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/480086274;FBCR/MobiFone;FBMF/Redmi;FBBD/Redmi;FBDV/23113RKC6C;FBSV/9;FBCA/x86:armeabi-v7a;FBDM/{density=1.5,width=1280,height=720};FB_FW/1;FBRV/0;]"
        }
    
    def DangNhap(self, app_token, config):
        self.data = {
            'email': self.email,
            'password': self.mat_khau,
            'generate_session_cookies': '1',
            'locale': 'vi_VN',
            'client_country_code': 'VN',
            'access_token': app_token,
            "api_key": self.API_KEY,
            "adid": self.adid,
            "account_switcher_uids": f'["{self.email}"]',
            "source": "login",
            "machine_id": self.machine_id,
            "jazoest": self.jazoest,
            "meta_inf_fbmeta": "V2_UNTAGGED",
            "fb_api_req_friendly_name": "authenticate",
            "fb_api_caller_class": "Fb4aAuthHandler",
            "sig": self.SIG
        }
        
        try:
            ket_qua = requests.post(self.URL, headers=self.HEADERS, data=self.data).json()
            
            if 'error' in ket_qua:
                error_msg = ket_qua.get('error', {}).get('message', 'Lỗi không xác định')
                error_data = ket_qua.get('error', {}).get('error_data', {})
                
                if 'login_first_factor' in error_data and 'uid' in error_data:
                    if self.auth:
                        try:
                            import pyotp
                            ma_2fa = pyotp.TOTP(self.auth).now()
                        except:
                            ma_2fa = input(f"Nhập mã 2FA cho {self.email}: ")
                    else:
                        ma_2fa = input(f"Nhập mã 2FA cho {self.email}: ")
                    
                    data_2fa = {
                        'locale': 'vi_VN',
                        'format': 'json',
                        'email': self.email,
                        'device_id': self.device_id,
                        'access_token': app_token,
                        'generate_session_cookies': 'true',
                        'generate_machine_id': '1',
                        'twofactor_code': ma_2fa,
                        'credentials_type': 'two_factor',
                        'error_detail_type': 'button_with_disabled',
                        'first_factor': error_data['login_first_factor'],
                        'password': self.mat_khau,
                        'userid': error_data['uid'],
                        'machine_id': error_data['login_first_factor']
                    }
                    ket_qua = requests.post(self.URL, headers=self.HEADERS, data=data_2fa).json()
                else:
                    return {'status': 401, 'msg': error_msg}
            
            if 'access_token' in ket_qua:
                access_token = ket_qua.get('access_token')
                cookies_string = "; ".join(f"{c['name']}={c['value']}" for c in ket_qua.get("session_cookies", []))
                return {'status': 200, 'data': {'cookies': cookies_string, 'token': access_token}}
            else:
                error_msg = ket_qua.get('error', {}).get('message', 'Đăng nhập thất bại')
                return {'status': 401, 'msg': error_msg}
                
        except Exception as e:
            return {'status': 401, 'msg': str(e)}

def lay_uid_tu_cookie(cookies: str):
    match = re.search(r"c_user=(\d+)", cookies)
    return match.group(1) if match else None
        
# ========== PHẦN FACEBOOK UI ==========
class FacebookUI:
    def __init__(self, config):
        self.d = u2.connect()
        self.package = "com.facebook.katana"
        self.config = config
        
    def lay_code_tu_mail(self, email, refresh_token, client_id, api_key):
        print("\n🔍 ĐANG LẤY CODE XÁC NHẬN...")
        so_lan_thu = self.config["so_lan_thu_get_code"]
        delay = self.config["delay_get_code"]
        
        for i in range(so_lan_thu):
            print(f"   Lần thử {i+1}/{so_lan_thu}...", end='\r')
        
            url_code = "https://tools.dongvanfb.net/api/graph_code"
            payload_code = {
                "email": email,
                "refresh_token": refresh_token,
                "client_id": client_id,
                "type": "facebook"
            }
        
            try:
                ket_qua_code = requests.post(url_code, json=payload_code)
                du_lieu_code = ket_qua_code.json()
                if du_lieu_code.get("status") and du_lieu_code.get("code"):
                    code = du_lieu_code.get("code")
                    print(f"\n🎉 CODE: {code}")
                    return code
            except:
                pass
            time.sleep(delay)
    
        toast("❌ Không lấy được code")
        print("\n❌ Không lấy được code!")
        xoa_du_lieu_fb()
        return self.chay_dang_ky(api_key)
    
    def click_text_chua(self, text, ten_nut, so_lan_thu=3, delay=1, click_duoi=False):
        for lan in range(so_lan_thu):
            print(f"   🔍 Đang tìm '{text}' (lần {lan + 1}/{so_lan_thu})...")
            if self.d(textContains=text).exists:
                elements = self.d(textContains=text)
                if click_duoi:
                    elem = elements[-1]
                else:
                    elem = elements[0] if hasattr(elements, '__getitem__') else elements
                vi_tri = elem.center()
                print(f"   ✅ Tìm thấy tại ({vi_tri[0]}, {vi_tri[1]})")
                print(f"\n🎯 Click '{ten_nut}'...")
                elem.click()
                return True
            if lan < so_lan_thu - 1:
                print(f"   ⏰ Chưa thấy, chờ {delay} giây...")
                time.sleep(delay)
        print(f"   ❌ Không tìm thấy '{text}' sau {so_lan_thu} lần thử")
        return False
    
    def click_toi_dong_y(self):
        if self.d(textContains="Tôi đồng ý").exists:
            elements = self.d(textContains="Tôi đồng ý")
            elements[-1].click()
            return True
        return False
    
    def click_text(self, text, ten_nut, so_lan_thu=3, delay=1):
        for lan in range(so_lan_thu):
            print(f"   🔍 Đang tìm '{text}' (lần {lan + 1}/{so_lan_thu})...")
            if self.d(text=text).exists:
                elem = self.d(text=text)
                vi_tri = elem.center()
                print(f"   ✅ Tìm thấy tại ({vi_tri[0]}, {vi_tri[1]})")
                print(f"\n🎯 Click '{ten_nut}'...")
                elem.click()
                return True
            if lan < so_lan_thu - 1:
                print(f"   ⏰ Chưa thấy, chờ {delay} giây...")
                time.sleep(delay)
        print(f"   ❌ Không tìm thấy '{text}' sau {so_lan_thu} lần thử")
        return False
    
    def click_truong(self, ten_truong, double=False, so_lan_thu=3, delay=1):
        for lan in range(so_lan_thu):
            print(f"   🔍 Đang tìm trường '{ten_truong}' (lần {lan + 1}/{so_lan_thu})...")
            if self.d(text=ten_truong).exists:
                phan_tu = self.d(text=ten_truong)
                vi_tri = phan_tu.center()
                print(f"   ✅ Tìm thấy tại ({vi_tri[0]}, {vi_tri[1]})")
                if double:
                    print(f"\n🎯 Double click trường '{ten_truong}'...")
                    phan_tu.click()
                    time.sleep(0.2)
                    phan_tu.click()
                else:
                    print(f"\n🎯 Click trường '{ten_truong}'...")
                    phan_tu.click()
                return True
            if lan < so_lan_thu - 1:
                print(f"   ⏰ Chưa thấy, chờ {delay} giây...")
                time.sleep(delay)
        print(f"   ❌ Không tìm thấy trường '{ten_truong}' sau {so_lan_thu} lần thử")
        return False
    
    def nhap_text(self, text):
        self.d.send_keys(text)
        time.sleep(0.3)
    
    def kiem_tra_text(self, danh_sach_text, so_lan_thu=2, delay=1):
        for lan in range(so_lan_thu):
            for text in danh_sach_text:
                if self.d(text=text).exists or self.d(textContains=text).exists:
                    return True
            if lan < so_lan_thu - 1:
                time.sleep(delay)
        return False
    
    def kiem_tra_loi_dang_ky(self):
        texts_loi = [
            "Để đăng ký, hãy đọc cũng như đồng ý với các điều khoản và chính sách của chúng tôi",
            "Tìm hiểu thêm",
            "Chính sách cookie"
        ]
        return self.kiem_tra_text(texts_loi, 2, 1)
    
    def tao_so_dien_thoai(self):
        dau_so = ["333", "338", "339", "358", "359", "368", "369", "378", "379", "388", "389",
                  "396", "397", "398", "399", "777", "778", "779", "787", "788", "789", 
                  "968", "969", "978", "979", "988", "989"]
        so = random.choice(dau_so) + ''.join(random.choices(string.digits, k=6))
        return f"+84{so}"
    
    def tao_ho(self):
        ho_list = ["Nguyen", "Tran", "Le", "Pham", "Hoang", "Huynh", "Phan", "Vu", "Vo", "Dang"]
        return random.choice(ho_list)
    
    def tao_ten(self):
        ten_list = ["An", "Binh", "Cuong", "Dung", "Duc", "Ha", "Hieu", "Hoa", "Hung", "Minh"]
        return random.choice(ten_list)
    
    def sdt(self, api_key, email_da_co=None, mat_khau_da_co=None, refresh_token_da_co=None, client_id_da_co=None, dong_email_cu=None):
        while True:
            print("\n[21] Nhập số điện thoại...")
            so_dt = self.tao_so_dien_thoai()
            toast(f"Nhập SĐT: {so_dt}")
            if self.click_truong("Số di động", False, 3, 1):
                self.nhap_text(so_dt)
                print(f"   ✅ Đã nhập số: {so_dt}")
            time.sleep(self.config["delay_nhap_sdt"])
            
            print("\n[22] Click Tiếp...")
            if not self.click_text_chua("Tiếp", "Tiếp", 3, 1):
                return None
            time.sleep(self.config["delay_click_tiep_sdt"])
            
            print("\nClick Tiếp tục tạo tài khoản")
            if not self.click_text_chua("Tiếp tục tạo tài khoản", "Tiếp tục tạo tài khoản", 3, 1, click_duoi=True):
               print("   ⚠️ Không tìm thấy, bỏ qua...")
            time.sleep(self.config["delay_click_tiep_tuc_tao_tk"])
            
            texts_loi = [
                "Số di động của bạn là gì?",
                "Nhập số di động có thể dùng để liên hệ với bạn. Sẽ không ai nhìn thấy thông tin này trên trang cá nhân của bạn."
            ]
            
            if self.kiem_tra_text(texts_loi, 2, self.config["delay_kiem_tra_sdt"]):
                print("\n⚠️ Số điện thoại không hợp lệ, nhập lại...")
                self.click_truong("Số di động", False, 2, 0.5)
                time.sleep(0.3)
                self.d.clear_text()
                time.sleep(0.5)
                continue
            
            print("\n✅ Số điện thoại hợp lệ!")
            break
        
        mat_khau_fb = self.config["mat_khau_fb"]
        toast(f"🔑 Nhập Mk: {mat_khau_fb}")
        print("\n[23] Nhập Mật khẩu...")
        if self.click_truong("Mật khẩu", False, 5, 1):
            self.nhap_text(mat_khau_fb)
            print(f"   ✅ Đã nhập mật khẩu: {mat_khau_fb}")
        else:
            print("   ❌ Không tìm thấy trường Mật khẩu!")
            return None
        time.sleep(self.config["delay_nhap_mat_khau"])
        
        print("\n[24] Click Tiếp...")
        if not self.click_text_chua("Tiếp", "Tiếp", 3, 1):
            return None
        time.sleep(self.config["delay_click_tiep_sau_mk"])
        
        print("\n[28] Click Lưu")
        if not self.click_text_chua("Lưu", "Lưu", 2, 0.5, click_duoi=True):
            print("   ⚠️ Không tìm thấy, bỏ qua...")
        time.sleep(self.config["delay_click_luu"])
        
        print("\n[25] Click Tôi đồng ý...")
        self.click_toi_dong_y()
        toast("Click Tôi đồng ý")

        print("\n[26] Đang chờ...")
        time.sleep(self.config["delay_cho_toi_dong_y"])
        
        if self.kiem_tra_loi_dang_ky():
            print("\n⚠️ Phát hiện lỗi đăng ký, thoát...")
            toast("⚠️ Phát hiện lỗi đăng ký, thoát")
            return None
        
        print("\n[27] Click Tiếp tục...")
        if not self.click_text_chua("Tiếp tục", "Tiếp tục", 3, 1):
            print("   ⚠️ Không tìm thấy nút Tiếp tục, bỏ qua...")
        time.sleep(self.config["delay_click_tiep_tuc"])
        
        print("\n[28] Click Không cho phép lần 1...")
        if not (self.click_text_chua("Không cho phép", "Không cho phép", 2, 0.5) or
               self.click_text_chua("TỪ CHỐI", "TỪ CHỐI", 2, 0.5)):
            print("   ⚠️ Không tìm thấy, bỏ qua...")
        time.sleep(self.config["delay_click_khong_cho_phep"])
        
        print("\n[29] Click Không cho phép lần 2...")
        if not (self.click_text_chua("Không cho phép", "Không cho phép", 2, 0.5) or
               self.click_text_chua("TỪ CHỐI", "TỪ CHỐI", 2, 0.5)):
            print("   ⚠️ Không tìm thấy, bỏ qua...")
        time.sleep(self.config["delay_click_khong_cho_phep_lan2"])
        
        print("\n[30] Buộc dừng Facebook...")
        chay_lenh_adb("shell am force-stop com.facebook.katana")
        khoa_xoay_man_hinh()
        time.sleep(self.config["delay_buoc_dung_fb"])
        
        print("\n[31] Mở lại Facebook...")
        self.d.app_start(self.package)
        khoa_xoay_man_hinh()
        toast("📱 Mở lại Facebook")
        time.sleep(self.config["delay_mo_lai_fb"])
        
        print("\n[32] Click Tôi không nhận được mã...")
        self.click_text_chua("Tôi không nhận được mã", "Tôi không nhận được mã", 3, 1)
        time.sleep(self.config["delay_click_toi_khong_nhan_duoc_ma"])
        
        print("\n[33] Click Xác nhận bằng email...")
        self.click_text_chua("Xác nhận bằng email", "Xác nhận bằng email", 3, 1)
        time.sleep(self.config["delay_click_xac_nhan_email"])
        
        # Lấy email và các thông tin cần thiết
        if email_da_co and refresh_token_da_co and client_id_da_co:
            email = email_da_co
            refresh_token = refresh_token_da_co
            client_id = client_id_da_co
            print(f"\n📧 Sử dụng email từ file: {email}")
            # Xóa email đã dùng khỏi file
            if dong_email_cu:
                xoa_email_da_dung(dong_email_cu)
        else:
            email, pass_mail, refresh_token, client_id = mua_mail(api_key, self.config)
            if not email:
                return None
        
        toast(f"📧 Nhập email: {email}")
        print("\n[34] Nhập Email...")
        if self.click_truong("Email", False, 3, 1):
            self.nhap_text(email)
            print(f"   ✅ Đã nhập email: {email}")
        time.sleep(self.config["delay_nhap_email"])
        
        print("\n[35] Click Tiếp...")
        if not self.click_text_chua("Tiếp", "Tiếp", 3, 1):
            return None
        time.sleep(self.config["delay_click_tiep_sau_email"])
        toast("Đang get code")
        # Lấy code (cả email từ file và mua mới đều get code)
        code = self.lay_code_tu_mail(email, refresh_token, client_id, api_key)
        
        print("\n[36] Nhập mã xác nhận...")
        if self.click_text_chua("Mã xác nhận", "Mã xác nhận", 3, 1):
            if code:
                self.nhap_text(code)
                toast(f"🔓 Nhập Mã: {code}")
                print(f"   ✅ Đã nhập code: {code}")
            else:
                toast("⚠️ Không có code để nhập")
                print("   ⚠️ Không có code để nhập!")
                xoa_du_lieu_fb()
                return self.chay_dang_ky(api_key)
        time.sleep(self.config["delay_nhap_code"])
        
        print("\n[37] Click Tiếp lần cuối...")
        if self.click_text_chua("Tiếp", "Tiếp lần cuối", 3, 1):
            time.sleep(self.config["delay_click_tiep_cuoi"])
            print("\n✅ HOÀN TẤT ĐĂNG KÝ!")
            return email, mat_khau_fb, refresh_token, client_id
        
        return None
    
    def chay_dang_ky(self, api_key, email_da_co=None, mat_khau_da_co=None, refresh_token_da_co=None, client_id_da_co=None, dong_email_cu=None):
        print("─"*70)
        print("📘 FACEBOOK - QUY TRÌNH ĐĂNG KÝ")
        print("─"*70)
        
        print("[2] Đang mở Facebook...")
        self.d.app_start(self.package)
        print("   ✅ Đã mở")
        
        print("[3] Đang khóa xoay màn hình...")
        khoa_xoay_man_hinh()
        print("   ✅ Đã khóa xoay dọc")
        
        toast("📱 Mở Facebook")
        
        print(f"[4] Đang chờ {self.config['delay_mo_facebook']} giây...")
        time.sleep(self.config["delay_mo_facebook"])
        
        print("\n[28] Click Không cho phép lần 1...")
        if not (self.click_text_chua("Không cho phép", "Không cho phép", 2, 0.5, click_duoi=True) or
               self.click_text_chua("TỪ CHỐI", "TỪ CHỐI", 2, 0.5, click_duoi=True)):
            print("   ⚠️ Không tìm thấy, bỏ qua...")
        time.sleep(self.config["delay_chon_khong_cho_phep"])
        
        print("\n[28] Click Tôi có tài khoản rồi")
        if not (self.click_text_chua("Tôi có tài khoản rồi", "Tôi có tài khoản rồi", 2, 0.5, click_duoi=True) or
               self.click_text_chua("I already have a profile", "I already have a profile", 2, 0.5, click_duoi=True)):
            print("   ⚠️ Không tìm thấy, bỏ qua...")
        time.sleep(self.config["delay_chon_toi_co_tai_khoan_roi"])
        
        print("\n[5] Click Tạo tài khoản mới lần 1...")
        if not self.click_text_chua("Tạo tài khoản mới", "Tạo tài khoản mới lần 1", 3, 1):
                xoa_du_lieu_fb()
                return self.chay_dang_ky(api_key)
        time.sleep(self.config["delay_click_tao_tk_lan1"])
        
        print("\n[6] Click Tạo tài khoản mới lần 2...")
        if not self.click_text_chua("Tạo tài khoản mới", "Tạo tài khoản mới", 3, 0.5, click_duoi=True):
            print("   ⚠️ Không tìm thấy, bỏ qua...")
        time.sleep(self.config["delay_click_tao_tk_lan2"])
        
        print("\n[7] Đang chờ...")
        time.sleep(1)
        
        print("\n[8] Click Không cho phép...")
        if not (self.click_text_chua("Không cho phép", "Không cho phép", 2, 0.5, click_duoi=True) or
               self.click_text_chua("TỪ CHỐI", "TỪ CHỐI", 2, 0.5, click_duoi=True)):
            return None
        time.sleep(self.config["delay_chon_khong_cho_phep_lan2"])
        
        ho = self.tao_ho()
        ten = self.tao_ten()
        toast(f"✍️ Nhập Họ Tên: {ho} {ten}")
        w, h = self.d.window_size()
        self.d.click(int(w / 2), int(h / 2))
        print("\n[9] Nhập Họ...")
        if self.click_truong("Họ", False, 3, 1):
            self.nhap_text(ho)
            print(f"   ✅ Đã nhập họ: {ho}")
        time.sleep(self.config["delay_nhap_ho"])
        
        w, h = self.d.window_size()
        self.d.click(int(w / 2), int(h / 2))
        print("\n[10] Nhập Tên...")
        if self.click_truong("Tên", False, 3, 1):
            self.nhap_text(ten)
            print(f"   ✅ Đã nhập tên: {ten}")
        time.sleep(self.config["delay_nhap_ten"])
        
        w, h = self.d.window_size()
        self.d.click(int(w / 2), int(h / 2))
        print("\n[11] Click Tiếp lần 1...")
        if not self.click_text_chua("Tiếp", "Tiếp lần 1", 3, 1):
            return None
        time.sleep(self.config["delay_click_tiep_lan1"])
        
        print("\n[12] Click CHỌN...")
        if not (self.click_text("CHỌN", "CHỌN", 3, 1)or
               self.click_text_chua("SET", "SET", 2, 0.5, click_duoi=True)):
            self.d.click(696, 1491)
        time.sleep(self.config["delay_click_chon"])
        
        print("\n[13] Click Tiếp lần 2...")
        if not self.click_text_chua("Tiếp", "Tiếp lần 2", 3, 1):
            return None
        time.sleep(self.config["delay_click_tiep_lan2"])
        
        print("\n[14] Click Tiếp lần 3...")
        if not self.click_text_chua("Tiếp", "Tiếp lần 3", 3, 1):
            return None
        time.sleep(self.config["delay_click_tiep_lan3"])
        
        print("\n[15] Nhập Tuổi...")
        tuoi = str(random.randint(18, 40))
        toast(f"✍️ Nhập Tuổi: {tuoi}")
        if self.click_truong("Tuổi", False, 3, 1):
            self.nhap_text(tuoi)
            print(f"   ✅ Đã nhập tuổi: {tuoi}")
        time.sleep(self.config["delay_nhap_tuoi"])
        
        print("\n[16] Click Tiếp lần 4...")
        if not self.click_text_chua("Tiếp", "Tiếp lần 4", 3, 1):
            return None
        time.sleep(self.config["delay_click_tiep_lan4"])
        
        print("\n[17] Click OK...")
        self.click_text("OK", "OK", 3, 1)
        time.sleep(self.config["delay_click_ok"])
        
        gioi_tinh = random.choice(["Nam", "Nữ"])
        toast(f"🚻 Chọn giới tính: {gioi_tinh}")
        print("\n[18] Chọn giới tính...")
        self.click_text(gioi_tinh, gioi_tinh, 3, 1)
        time.sleep(self.config["delay_chon_gioi_tinh"])
        
        print("\n[19] Click Tiếp lần 5...")
        if not self.click_text_chua("Tiếp", "Tiếp lần 5", 3, 1):
            return None
        time.sleep(self.config["delay_click_tiep_lan5"])
        
        print("\n[20] Click Số di động...")
        if not self.click_text_chua("Số di động", "Số di động", 3, 1):
            return None
        
        return self.sdt(api_key, email_da_co, mat_khau_da_co, refresh_token_da_co, client_id_da_co, dong_email_cu)

def dang_nhap_va_luu_fb(email, mat_khau, config):
    print("\n" + "─"*70)
    print("🔐 ĐĂNG NHẬP FACEBOOK")
    print("─"*70)
    
    try:
        fb = Facebook(email, mat_khau, auth=None)
        for i in range(2):
            print(f"🔄 Thử đăng nhập lần {i+1}...")
            ket_qua = fb.DangNhap(APP_TOKEN, config)
            if ket_qua.get("status") == 200:
               break
            time.sleep(config["delay_thu_lai_khi_loi"])
        
        if ket_qua.get("status") == 200:
            du_lieu = ket_qua["data"]
            token = du_lieu.get("token", "")
            cookie = du_lieu.get("cookies", "")
            uid = lay_uid_tu_cookie(cookie)
            
            print("\n✅ ĐĂNG NHẬP THÀNH CÔNG!")
            print(f"📧 Email: {email}")
            print(f"🆔 UID: {uid if uid else 'N/A'}")
            print(f"🔑 Token: {token[:1000]}")
            
            luu_tai_khoan_fb(uid, email, mat_khau, cookie, token)
            
            # Gửi về tele nếu đã cấu hình
            token_tele, id_tele = doc_tele()
            if token_tele and id_tele:
                noi_dung = f"""✅ <b>FACEBOOK ĐĂNG KÝ THÀNH CÔNG</b>
<b>📧 Email:</b> <code>{html.escape(email)}</code>
<b>🔑 Pass:</b> <code>{html.escape(mat_khau)}</code>
<b>🆔 UID:</b> <code>{html.escape(uid)}</code>



<b>🍪 Cookie:</b>
<code>{html.escape(cookie[:1000])}</code>


<b>🔑 Token:</b>
<code>{html.escape(token[:1000])}</code>
"""
                gui_tele(token_tele, id_tele, noi_dung)
                print("   ✅ Đã gửi về Telegram")
            
            return True
        else:
            print(f"\n❌ ĐĂNG NHẬP THẤT BẠI!")
            print(f"📧 Email: {email}")
            print(f"❌ Lỗi: {ket_qua.get('msg')}")
            return False
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        return False

def main():
    # Kiểm tra và hỏi dùng config cũ hay cấu hình mới
    print("\n" + "─"*70)
    print(f"{trang}🤖 𝗧𝗢𝗢𝗟 𝗖𝗥𝗘𝗔𝗧𝗘 𝗔𝗖𝗖𝗢𝗨𝗡𝗧 𝗙𝗔𝗖𝗘𝗕𝗢𝗢𝗞 𝗔𝗗𝗕")
    print("─"*70)
    
    if os.path.exists(CONFIG_FILE):
        chon_config = input("Dùng lại config delay cũ không (y/n): ").strip().lower()
        if chon_config == "y":
            config = doc_config()
            print("✅ Đã tải cấu hình cũ!")
        else:
            config = cau_hinh_delay()
    else:
        print("⚠️ Chưa có file cấu hình! Hãy cấu hình delay lần đầu.")
        config = cau_hinh_delay()
    
    # Đọc thông tin tele đã lưu
    token_tele, id_tele = doc_tele()
    
    # Hiển thị menu chính
    print("\n" + "─"*70)
    print(f"{trang}📋  MENU CHÍNH")
    print("─"*70)
    
    # Kiểm tra đã login DongVan chưa
    tk_da_luu, mk_da_luu = doc_tai_khoan()
    toast(f"Chào Mừng {tk_da_luu} Đã Đến Với Tool Reg FB ADB")
    trang_thai_dv = f"{xanh}✔{trang} Đã Login" if tk_da_luu else f"{do}✘{trang} Chưa Login"
    ten_dv = f" • {tk_da_luu}" if tk_da_luu else ""
    print(f"1. Login DongVan │ {trang_thai_dv}{ten_dv}")
    print(f"2. Gửi Về Tele   │ {f'{xanh}✔{trang} Đã cấu hình' if token_tele and id_tele else f'{do}✘{trang} Chưa cấu hình'}")
    print(f"3. Cấu Hình Delay │ {xanh}✔{trang} Đã có config")
    print("─"*70)
    
    chon = input("Chọn Đi Bé (1, 2 hoặc 3): ").strip()

    if chon == "2":
       print("\n" + "─"*70)
       print("📧 CẤU HÌNH TELEGRAM")
       print("─"*70)

       token_tele, id_tele = doc_tele()

       # Nếu chưa cấu hình
       if not token_tele or not id_tele:
          print("⚠️ Chưa cấu hình Telegram!\n")
          token_tele_moi = input("Nhập Token: ").strip()
          id_tele_moi = input("Nhập ID Acc Tele Của Bạn: ").strip()

          if token_tele_moi and id_tele_moi:
              luu_tele(token_tele_moi, id_tele_moi)
              print("✅ Đã lưu cấu hình Telegram!")
          else:
              print("❌ Token hoặc ID không hợp lệ!")

       else:
           print(f"🔑 Token hiện tại: {token_tele}")
           print(f"🆔 ID hiện tại: {id_tele}")

           print("\n1. Dùng Lại Token Và ID Cũ")
           print("2. Cấu Hình Lại")
           print("3. Hủy Cấu Hình")

           chon_tele = input("Chọn: ").strip()

           if chon_tele == "1":
               print("✅ Sử dụng cấu hình cũ!")

           elif chon_tele == "2":
               token_tele_moi = input("Nhập Token mới: ").strip()
               id_tele_moi = input("Nhập ID Acc Tele Của Bạn: ").strip()

               if token_tele_moi and id_tele_moi:
                   luu_tele(token_tele_moi, id_tele_moi)
                   print("✅ Đã cập nhật cấu hình Telegram!")
               else:
                   print("❌ Token hoặc ID không hợp lệ!")

           elif chon_tele == "3":
               if os.path.exists(TELE_FILE):
                   os.remove(TELE_FILE)
                   print("🗑️ Đã xóa cấu hình Telegram!")
               else:
                   print("⚠️ Không có cấu hình để xóa!")

           else:
               print("❌ Lựa chọn không hợp lệ!")

       print("\n✅ Hoàn tất cấu hình! Chạy lại tool để bắt đầu.")
       return

    if chon == "3":
        cau_hinh_delay()
        print("\n✅ Đã cấu hình xong! Chạy lại tool để bắt đầu.")
        return

# Nếu không phải 1 thì báo lỗi
    if chon != "1":
       print("❌ Lựa chọn không hợp lệ!")
       return
    
    # Đăng nhập DongVan
    if tk_da_luu and mk_da_luu:
        chon_dv = input(f"Có Login Acc {tk_da_luu} Không (y/n): ")
        if chon_dv.lower() == "y":
            ten_dang_nhap = tk_da_luu
            mat_khau_dv = mk_da_luu
        else:
            ten_dang_nhap = input("Tài khoản DongVan: ")
            mat_khau_dv = input("Mật khẩu DongVan: ")
            luu_tai_khoan(ten_dang_nhap, mat_khau_dv)
    else:
        ten_dang_nhap = input("Tài khoản DongVan: ")
        mat_khau_dv = input("Mật khẩu DongVan: ")
        luu_tai_khoan(ten_dang_nhap, mat_khau_dv)
    
    url_dang_nhap = "https://api.dongvanfb.net/api/user/login?locale=vn"
    headers = {"Accept": "application/json, text/plain, */*", "Content-Type": "application/json"}
    payload = {"username": ten_dang_nhap, "password": mat_khau_dv}
    
    try:
        ket_qua = requests.post(url_dang_nhap, json=payload, headers=headers)
        du_lieu = ket_qua.json()
        
        print("\nTin nhắn:", du_lieu.get("message"))
        
        if not du_lieu.get("status"):
            print("❌ Đăng nhập thất bại!")
            return
        
        nguoi_dung = du_lieu.get("user_data", {})
        api_key = nguoi_dung.get("api_key")
        
        print("\n" + "─"*70)
        print("📊 THÔNG TIN TÀI KHOẢN DONGVAN")
        print("─"*70)
        print(f"Tên đăng nhập: {nguoi_dung.get('username')}")
        print(f"ID: {nguoi_dung.get('id')}")
        print(f"Email: {nguoi_dung.get('email')}")
        print(f"Số dư: {format_money(nguoi_dung.get('money', 0))}")
        print("─"*70)
        
        # Hỏi chọn phương thức lấy email
        print("\n" + "─"*70)
        print("📧 CHỌN PHƯƠNG THỨC LẤY EMAIL")
        print("─"*70)
        print("1. Buy Hotmail")
        print(f"2. Lấy Từ File {GOM_HOTMAIL_FILE}")
        lua_chon = input("Chọn Đi Bé (1 hoặc 2): ").strip()
        
        email_da_co = None
        mat_khau_da_co = None
        refresh_token_da_co = None
        client_id_da_co = None
        dong_email_cu = None
        
        if lua_chon == "2":
            email_da_co, mat_khau_da_co, refresh_token_da_co, client_id_da_co, dong_email_cu = doc_email_tu_file()
            if not email_da_co:
                print("⚠️ Không có email trong file, chuyển sang mua mail...")
                lua_chon = "1"
        
        fb_ui = FacebookUI(config)
        
        print("\n🗑️ XÓA DỮ LIỆU LẦN ĐẦU...")
        xoa_du_lieu_fb()
        
        lan_chay = 0
        while True:
            lan_chay += 1
            print("\n" + "─"*70)
            print(f"🔄 LẦN CHẠY THỨ {lan_chay}")
            print("─"*70)
            
            if lua_chon == "2" and email_da_co:
                ket_qua_dang_ky = fb_ui.chay_dang_ky(api_key, email_da_co, mat_khau_da_co, refresh_token_da_co, client_id_da_co, dong_email_cu)
                # Sau khi dùng, lấy email tiếp theo cho lần sau
                email_da_co, mat_khau_da_co, refresh_token_da_co, client_id_da_co, dong_email_cu = doc_email_tu_file()
                if not email_da_co:
                    print("⚠️ Hết email trong file, chuyển sang mua mail...")
                    lua_chon = "1"
            else:
                ket_qua_dang_ky = fb_ui.chay_dang_ky(api_key)
            
            if ket_qua_dang_ky:
                email, mat_khau_fb, refresh_token, client_id = ket_qua_dang_ky
                print(f"\n✅ Đăng ký thành công! Email: {email}")
                time.sleep(5)
                dang_nhap_va_luu_fb(email, mat_khau_fb, config)
            else:
                print("\n❌ Đăng ký thất bại!")
            
            xoa_du_lieu_fb()
            delay_giua_lan = config["delay_giua_cac_lan_chay"]
            print(f"\n⏳ CHỜ {delay_giua_lan} GIÂY...")
            time.sleep(delay_giua_lan)
            
    except KeyboardInterrupt:
        print("\n\n🛑 ĐÃ DỪNG")
        sys.exit(0)
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    main()
