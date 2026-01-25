import time
import json
import textwrap
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- CẤU HÌNH ---
URL = "https://saori-hara-create.github.io/fan-shop/"

# --- DỮ LIỆU KIỂM THỬ: PHÂN VÙNG TƯƠNG ĐƯƠNG (TC01 - TC12) ---
test_cases = [
    {"id": "TC01", "desc": "Hợp lệ", "u": "user900", "e": "new900@gmail.com", "p": "Abc@12345", "c": "Abc@12345", "exp": "Success"},
    {"id": "TC02", "desc": "User 3 ký tự", "u": "abc", "e": "new901@gmail.com", "p": "Abc@12345", "c": "Abc@12345", "exp": "Lỗi"},
    {"id": "TC03", "desc": "User đã tồn tại", "u": "user123", "e": "new902@gmail.com", "p": "Abc@12345", "c": "Abc@12345", "exp": "Lỗi"},
    {"id": "TC04", "desc": "User bỏ trống", "u": "", "e": "new903@gmail.com", "p": "Abc@12345", "c": "Abc@12345", "exp": "trống"},
    {"id": "TC05", "desc": "Email sai format", "u": "user904", "e": "new904", "p": "Abc@12345", "c": "Abc@12345", "exp": "hợp lệ"},
    # TC06: Đã sửa tên user để bắt lỗi trùng Email
    {"id": "TC06", "desc": "Email đã tồn tại", "u": "user905_new", "e": "exist@gmail.com", "p": "Abc@12345", "c": "Abc@12345", "exp": "Lỗi"},
    {"id": "TC07", "desc": "Email bỏ trống", "u": "user906", "e": "", "p": "Abc@12345", "c": "Abc@12345", "exp": "trống"},
    {"id": "TC08", "desc": "Pass ngắn", "u": "user907", "e": "new907@gmail.com", "p": "Abc@12", "c": "Abc@12", "exp": "Mật khẩu"},
    {"id": "TC09", "desc": "Pass quá dài", "u": "user908", "e": "new908@gmail.com", "p": "Abc@123456789012345", "c": "Abc@123456789012345", "exp": "Mật khẩu"},
    {"id": "TC10", "desc": "Pass bỏ trống", "u": "user909", "e": "new909@gmail.com", "p": "", "c": "", "exp": "trống"},
    {"id": "TC11", "desc": "Confirm sai", "u": "user910", "e": "new910@gmail.com", "p": "Abc@12345", "c": "Abc@1234", "exp": "khớp"},
    {"id": "TC12", "desc": "Confirm bỏ trống", "u": "user911", "e": "new911@gmail.com", "p": "Abc@12345", "c": "", "exp": "trống"}
]

def run():
    print(f">>> ĐANG CHẠY TEST CASE LỚP TƯƠNG ĐƯƠNG...")
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-search-engine-choice-screen")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    wrapper = textwrap.TextWrapper(width=40) # Giảm width text xuống xíu để vừa bảng

    # Header bảng (Đã thêm Confirm)
    header = f"{'ID':<5} | {'User':<10} | {'Email':<18} | {'Pass':<10} | {'Confirm':<10} | {'Trạng thái (Chi tiết lỗi)':<42} | {'Kết quả'}"
    print("\n" + header)
    print("="*len(header))

    for tc in test_cases:
        try:
            driver.get(URL)
            driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
            
            # --- LOGIC ĐẶC BIỆT CHO TC03 VÀ TC06 (Inject Data) ---
            if tc['id'] in ['TC03', 'TC06']:
                fake_user = {
                    "id": 99999,
                    "username": "user123" if tc['id'] == 'TC03' else "user_khac",
                    "email": tc['e'],
                    "password": "hashed_password",
                    "createdAt": "2024-01-01"
                }
                if tc['id'] == 'TC03':
                    fake_user['username'] = tc['u']
                    fake_user['email'] = "email_khac@gmail.com"

                script = f"const users = [{json.dumps(fake_user)}]; localStorage.setItem('users', JSON.stringify(users));"
                driver.execute_script(script)
            # -----------------------------------------------------
            
            driver.refresh()
            time.sleep(1)

            # Mở form & Nhập liệu
            try:
                try: driver.find_element(By.XPATH, "//button[descendant::*[local-name()='svg']]").click()
                except: driver.find_element(By.XPATH, "//button[contains(text(), 'Đăng nhập')]").click()
                wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Đăng ký ngay')]"))).click()
            except:
                print(f"{tc['id']:<5} | Lỗi: Không mở được form.")
                continue

            driver.find_element(By.XPATH, "//input[@placeholder='Nhập tên người dùng']").send_keys(tc['u'])
            driver.find_element(By.XPATH, "//input[@placeholder='example@gmail.com']").send_keys(tc['e'])
            driver.find_element(By.XPATH, "//input[@placeholder='Nhập mật khẩu (VD: Pass@123)']").send_keys(tc['p'])
            driver.find_element(By.XPATH, "//input[@placeholder='Nhập lại mật khẩu']").send_keys(tc['c'])
            driver.find_element(By.XPATH, "//button[text()='Đăng ký']").click()
            time.sleep(1)

            # Kiểm tra kết quả
            is_success_web = False
            status_text = "Không xác định"
            
            # Check Alert
            alert_msg = ""
            try:
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert_msg = alert.text
                alert.accept()
            except: pass

            # Check Giao diện
            if tc['u'] == "":
                 if len(driver.find_elements(By.XPATH, "//button[text()='Đăng ký']")) == 0: is_success_web = True
            else:
                if len(driver.find_elements(By.XPATH, f"//span[contains(text(), '{tc['u']}')]")) > 0: is_success_web = True
            
            if is_success_web:
                status_text = "Đăng ký thành công (OK)"
            else:
                if alert_msg: status_text = f"FAIL (Popup): {alert_msg}"
                else:
                    try:
                        errors = driver.find_elements(By.XPATH, "//*[contains(@class, 'text-red')]")
                        found_msgs = [e.text.strip() for e in errors if e.text.strip() != "" and e.text.strip() != "*"]
                        status_text = f"FAIL: {', '.join(found_msgs) if found_msgs else 'Lỗi'}"
                    except: status_text = "FAIL: Lỗi hệ thống"

            # Đánh giá
            final_result = "FAIL"
            if tc['exp'] == "Success":
                if is_success_web: final_result = "PASS"
            else: 
                if not is_success_web: final_result = "PASS"

            # Print kết quả ra bảng
            icon = "✅" if final_result == "PASS" else "❌"
            u_pr = (tc['u'][:8] + '..') if len(tc['u']) > 8 else tc['u']
            p_pr = (tc['p'][:8] + '..') if len(tc['p']) > 8 else tc['p']
            c_pr = (tc['c'][:8] + '..') if len(tc['c']) > 8 else tc['c'] # Cắt ngắn nếu confirm pass quá dài

            lines = wrapper.wrap(status_text)
            if not lines: lines = [""]
            
            # Dòng đầu tiên
            print(f"{tc['id']:<5} | {u_pr:<10} | {tc['e']:<18} | {p_pr:<10} | {c_pr:<10} | {lines[0]:<42} | {icon} {final_result}")
            
            # Các dòng tiếp theo nếu lỗi dài quá
            for line in lines[1:]: 
                print(f"{'':<5} | {'':<10} | {'':<18} | {'':<10} | {'':<10} | {line:<42} |")
            print("-" * len(header))

        except Exception as e: print(f"{tc['id']:<5} | Error: {str(e)[:30]}")

    driver.quit()

if __name__ == "__main__":
    run()