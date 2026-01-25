import time
import textwrap  # <--- Thư viện để xử lý xuống dòng
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- CẤU HÌNH ---
URL = "https://saori-hara-create.github.io/fan-shop/"

# --- DỮ LIỆU KIỂM THỬ ---
test_cases = [
    {"id": "TC01", "desc": "Hợp lệ", "u": "user900", "e": "new900@gmail.com", "p": "Abc@12345", "c": "Abc@12345", "exp": "Success"},
    {"id": "TC02", "desc": "User 3 ký tự", "u": "abc", "e": "new901@gmail.com", "p": "Abc@12345", "c": "Abc@12345", "exp": "Lỗi"},
    {"id": "TC03", "desc": "User đã tồn tại", "u": "user123", "e": "new902@gmail.com", "p": "Abc@12345", "c": "Abc@12345", "exp": "Lỗi"},
    {"id": "TC04", "desc": "User bỏ trống", "u": "", "e": "new903@gmail.com", "p": "Abc@12345", "c": "Abc@12345", "exp": "trống"},
    {"id": "TC05", "desc": "Email sai format", "u": "user904", "e": "new904", "p": "Abc@12345", "c": "Abc@12345", "exp": "hợp lệ"},
    {"id": "TC06", "desc": "Email đã tồn tại", "u": "user905", "e": "exist@gmail.com", "p": "Abc@12345", "c": "Abc@12345", "exp": "Lỗi"},
    {"id": "TC07", "desc": "Email bỏ trống", "u": "user906", "e": "", "p": "Abc@12345", "c": "Abc@12345", "exp": "trống"},
    {"id": "TC08", "desc": "Pass ngắn", "u": "user907", "e": "new907@gmail.com", "p": "Abc@12", "c": "Abc@12", "exp": "Mật khẩu"},
    {"id": "TC09", "desc": "Pass quá dài", "u": "user908", "e": "new908@gmail.com", "p": "Abc@123456789012345", "c": "Abc@123456789012345", "exp": "Mật khẩu"},
    {"id": "TC10", "desc": "Pass bỏ trống", "u": "user909", "e": "new909@gmail.com", "p": "", "c": "", "exp": "trống"},
    {"id": "TC11", "desc": "Confirm sai", "u": "user910", "e": "new910@gmail.com", "p": "Abc@12345", "c": "Abc@1234", "exp": "khớp"},
    {"id": "TC12", "desc": "Confirm bỏ trống", "u": "user911", "e": "new911@gmail.com", "p": "Abc@12345", "c": "", "exp": "trống"},
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
    print(f">>> ĐANG CHẠY KIỂM THỬ (WORD WRAP - XUỐNG DÒNG)...")
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-search-engine-choice-screen")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    # Header bảng
    # Tăng độ rộng cột trạng thái lên 45
    print(f"\n{'ID':<5} | {'User':<10} | {'Email':<20} | {'Pass':<10} | {'Trạng thái (Chi tiết lỗi)':<45} | {'Kết quả'}")
    print("="*120)

    # Khởi tạo công cụ ngắt dòng (chiều rộng tối đa 45 ký tự)
    wrapper = textwrap.TextWrapper(width=45)

    for tc in test_cases:
        try:
            # 1. Reset môi trường
            driver.get(URL)
            driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
            driver.delete_all_cookies()
            driver.refresh()
            time.sleep(1)

            # 2. Mở form
            try:
                try:
                    driver.find_element(By.XPATH, "//button[descendant::*[local-name()='svg']]").click()
                except:
                    driver.find_element(By.XPATH, "//button[contains(text(), 'Đăng nhập')]").click()
                
                wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Đăng ký ngay')]"))).click()
            except:
                print(f"{tc['id']:<5} | Lỗi: Không mở được form.")
                continue

            # 3. Nhập liệu
            driver.find_element(By.XPATH, "//input[@placeholder='Nhập tên người dùng']").send_keys(tc['u'])
            driver.find_element(By.XPATH, "//input[@placeholder='example@gmail.com']").send_keys(tc['e'])
            driver.find_element(By.XPATH, "//input[@placeholder='Nhập mật khẩu (VD: Pass@123)']").send_keys(tc['p'])
            driver.find_element(By.XPATH, "//input[@placeholder='Nhập lại mật khẩu']").send_keys(tc['c'])
            
            # 4. Submit
            driver.find_element(By.XPATH, "//button[text()='Đăng ký']").click()
            time.sleep(1.5) 

            # 5. Xử lý kết quả & Lấy Text
            is_success_web = False
            status_text = "Không xác định"
            
            if tc['u'] == "":
                 if len(driver.find_elements(By.XPATH, "//button[text()='Đăng ký']")) == 0:
                     is_success_web = True
            else:
                if len(driver.find_elements(By.XPATH, f"//span[contains(text(), '{tc['u']}')]")) > 0:
                    is_success_web = True
            
            if is_success_web:
                status_text = "Đăng ký thành công (OK)"
            else:
                # Lọc lỗi và bỏ dấu *
                error_msg = ""
                try:
                    errors = driver.find_elements(By.XPATH, "//*[contains(@class, 'text-red')]")
                    found_msgs = [e.text.strip() for e in errors if e.text.strip() != "" and e.text.strip() != "*"]
                    
                    if found_msgs:
                        error_msg = ", ".join(found_msgs)
                    else:
                        error_msg = "Lỗi (Không tìm thấy text)"
                except:
                    error_msg = "Lỗi hệ thống"
                
                status_text = f"FAIL: {error_msg}"

            # 6. Đánh giá PASS/FAIL
            final_result = "FAIL"
            if tc['exp'] == "Success":
                if is_success_web: final_result = "PASS"
            else: 
                if not is_success_web: final_result = "PASS"

            # 7. IN RA MÀN HÌNH (CÓ XUỐNG DÒNG)
            icon = "✅" if final_result == "PASS" else "❌"
            u_pr = (tc['u'][:8] + '..') if len(tc['u']) > 8 else tc['u']
            p_pr = (tc['p'][:8] + '..') if len(tc['p']) > 8 else tc['p']
            
            # Cắt status_text thành các dòng nhỏ
            lines = wrapper.wrap(status_text)
            
            # Nếu không có nội dung thì gán mảng rỗng để tránh lỗi
            if not lines: lines = [""]

            # In dòng đầu tiên chứa đầy đủ thông tin
            print(f"{tc['id']:<5} | {u_pr:<10} | {tc['e']:<20} | {p_pr:<10} | {lines[0]:<45} | {icon} {final_result}")

            # In các dòng tiếp theo (nếu thông báo lỗi quá dài)
            for line in lines[1:]:
                # Các cột khác để trống, chỉ in cột Trạng thái
                print(f"{'':<5} | {'':<10} | {'':<20} | {'':<10} | {line:<45} |")

            # In đường gạch ngang mờ để phân cách các test case cho dễ nhìn
            print("-" * 120)

        except Exception as e:
            print(f"{tc['id']:<5} | Error: {str(e)[:30]}")

    print("="*120)
    driver.quit()

if __name__ == "__main__":
    run()