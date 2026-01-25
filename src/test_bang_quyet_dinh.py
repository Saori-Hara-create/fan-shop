import time
import textwrap
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- CẤU HÌNH ---
URL = "https://saori-hara-create.github.io/fan-shop/"

# --- DỮ LIỆU KIỂM THỬ: BẢNG QUYẾT ĐỊNH (TC13 - TC21) ---
test_cases = [
    {"id": "TC13", "desc": "DT: Hợp lệ", "u": "user900", "e": "new900@gmail.com", "p": "Ab@12345", "c": "Ab@12345", "exp": "Success"},
    {"id": "TC14", "desc": "DT: Confirm sai", "u": "user901", "e": "new901@gmail.com", "p": "Ab@12345", "c": "Ab@1234", "exp": "khớp"},
    {"id": "TC15", "desc": "DT: Thiếu Confirm", "u": "user902", "e": "new902@gmail.com", "p": "Ab@12345", "c": "", "exp": "trống"},
    {"id": "TC16", "desc": "DT: Pass sai", "u": "user903", "e": "new903@gmail.com", "p": "adadaad", "c": "adadaad", "exp": "Mật khẩu"},
    {"id": "TC17", "desc": "DT: Thiếu Pass", "u": "user904", "e": "new904@gmail.com", "p": "", "c": "", "exp": "trống"},
    {"id": "TC18", "desc": "DT: Email sai", "u": "user905", "e": "new905", "p": "Ab@12345", "c": "Ab@12345", "exp": "hợp lệ"},
    {"id": "TC19", "desc": "DT: Thiếu Email", "u": "user906", "e": "", "p": "Ab@12345", "c": "Ab@12345", "exp": "trống"},
    {"id": "TC20", "desc": "DT: User sai", "u": "ab", "e": "new908@gmail.com", "p": "Ab@12345", "c": "Ab@12345", "exp": "Lỗi"},
    {"id": "TC21", "desc": "DT: Rỗng hết", "u": "", "e": "", "p": "", "c": "", "exp": "trống"}
]

def run():
    print(f">>> ĐANG CHẠY TEST CASE BẢNG QUYẾT ĐỊNH...")
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-search-engine-choice-screen")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    wrapper = textwrap.TextWrapper(width=45)

    print(f"\n{'ID':<5} | {'User':<10} | {'Email':<20} | {'Pass':<10} | {'Trạng thái (Chi tiết lỗi)':<45} | {'Kết quả'}")
    print("="*120)

    for tc in test_cases:
        try:
            driver.get(URL)
            driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
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
                        status_text = f"FAIL: {', '.join(found_msgs) if found_msgs else 'Lỗi (Không tìm thấy text)'}"
                    except: status_text = "FAIL: Lỗi hệ thống"

            # Đánh giá
            final_result = "FAIL"
            if tc['exp'] == "Success":
                if is_success_web: final_result = "PASS"
            else: 
                if not is_success_web: final_result = "PASS"

            # Print
            icon = "✅" if final_result == "PASS" else "❌"
            u_pr = (tc['u'][:8] + '..') if len(tc['u']) > 8 else tc['u']
            p_pr = (tc['p'][:8] + '..') if len(tc['p']) > 8 else tc['p']
            lines = wrapper.wrap(status_text)
            if not lines: lines = [""]
            print(f"{tc['id']:<5} | {u_pr:<10} | {tc['e']:<20} | {p_pr:<10} | {lines[0]:<45} | {icon} {final_result}")
            for line in lines[1:]: print(f"{'':<5} | {'':<10} | {'':<20} | {'':<10} | {line:<45} |")
            print("-" * 120)

        except Exception as e: print(f"{tc['id']:<5} | Error: {str(e)[:30]}")

    driver.quit()

if __name__ == "__main__":
    run()