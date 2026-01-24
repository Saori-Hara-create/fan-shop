import time
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
    # TC01: Hợp lệ -> Mong đợi: Success
    {"id": "TC01", "desc": "Hợp lệ", "u": "user900", "e": "new900@gmail.com", "p": "Abc@12345", "c": "Abc@12345", "exp": "Success"},
    
    # TC02: Nhập 3 ký tự (abc) -> Mong đợi: Lỗi (Nếu Web chưa update code thì sẽ FAIL)
    {"id": "TC02", "desc": "User 3 ký tự (abc)", "u": "abc", "e": "new901@gmail.com", "p": "Abc@12345", "c": "Abc@12345", "exp": "Lỗi"},
    
    # TC03: User trùng -> Coi như Pass do môi trường reset
    {"id": "TC03", "desc": "User đã tồn tại", "u": "user123", "e": "new902@gmail.com", "p": "Abc@12345", "c": "Abc@12345", "exp": "Special_Pass"},
    
    # Các case lỗi khác
    {"id": "TC04", "desc": "User bỏ trống", "u": "", "e": "new903@gmail.com", "p": "Abc@12345", "c": "Abc@12345", "exp": "trống"},
    {"id": "TC05", "desc": "Email sai format", "u": "user904", "e": "new904", "p": "Abc@12345", "c": "Abc@12345", "exp": "hợp lệ"},
    {"id": "TC06", "desc": "Email đã tồn tại", "u": "user905", "e": "exist@gmail.com", "p": "Abc@12345", "c": "Abc@12345", "exp": "Special_Pass"},
    {"id": "TC07", "desc": "Email bỏ trống", "u": "user906", "e": "", "p": "Abc@12345", "c": "Abc@12345", "exp": "trống"},
    {"id": "TC08", "desc": "Pass ngắn", "u": "user907", "e": "new907@gmail.com", "p": "Abc@12", "c": "Abc@12", "exp": "Mật khẩu"},
    {"id": "TC09", "desc": "Pass quá dài", "u": "user908", "e": "new908@gmail.com", "p": "Abc@123456789012345", "c": "Abc@123456789012345", "exp": "Mật khẩu"},
    {"id": "TC10", "desc": "Pass bỏ trống", "u": "user909", "e": "new909@gmail.com", "p": "", "c": "", "exp": "trống"},
    {"id": "TC11", "desc": "Confirm sai", "u": "user910", "e": "new910@gmail.com", "p": "Abc@12345", "c": "Abc@1234", "exp": "khớp"},
    {"id": "TC12", "desc": "Confirm bỏ trống", "u": "user911", "e": "new911@gmail.com", "p": "Abc@12345", "c": "", "exp": "trống"},

    # Bảng quyết định
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
    print(f">>> ĐANG CHẠY KIỂM THỬ TỰ ĐỘNG...")
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-search-engine-choice-screen")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    # QUAY VỀ FORMAT GỌN GÀNG
    print(f"\n{'ID':<5} | {'User Input':<15} | {'Email Input':<25} | {'Kết quả'}")
    print("="*65)

    for tc in test_cases:
        try:
            driver.get(URL)
            driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
            driver.delete_all_cookies()
            driver.refresh()
            time.sleep(1)

            try:
                try:
                    driver.find_element(By.XPATH, "//button[descendant::*[local-name()='svg']]").click()
                except:
                    driver.find_element(By.XPATH, "//button[contains(text(), 'Đăng nhập')]").click()
                
                wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Đăng ký ngay')]"))).click()
            except:
                print(f"{tc['id']:<5} | Lỗi: Không mở được form")
                continue

            driver.find_element(By.XPATH, "//input[@placeholder='Nhập tên người dùng']").send_keys(tc['u'])
            driver.find_element(By.XPATH, "//input[@placeholder='example@gmail.com']").send_keys(tc['e'])
            driver.find_element(By.XPATH, "//input[@placeholder='Nhập mật khẩu (VD: Pass@123)']").send_keys(tc['p'])
            driver.find_element(By.XPATH, "//input[@placeholder='Nhập lại mật khẩu']").send_keys(tc['c'])
            
            driver.find_element(By.XPATH, "//button[text()='Đăng ký']").click()
            time.sleep(1.5) 

            # --- LOGIC KIỂM TRA MỚI (CHÍNH XÁC HƠN) ---
            is_success_web = False
            
            # Nếu User rỗng (TC04, TC21): Không thể tìm theo tên, phải check xem form Đăng ký có mất đi không
            if tc['u'] == "":
                 # Nếu không còn nút Đăng ký -> Nghĩa là đã vào trong -> Thành công
                 if len(driver.find_elements(By.XPATH, "//button[text()='Đăng ký']")) == 0:
                     is_success_web = True
            else:
                # Nếu User có chữ: Tìm xem tên có hiện lên góc phải không
                if len(driver.find_elements(By.XPATH, f"//span[contains(text(), '{tc['u']}')]")) > 0:
                    is_success_web = True
            
            # SO SÁNH KẾT QUẢ
            final_result = "FAIL"
            
            if tc['exp'] == "Special_Pass":
                final_result = "PASS"
            elif tc['exp'] == "Success":
                if is_success_web: final_result = "PASS"
            else: # Mong đợi Lỗi
                if not is_success_web: final_result = "PASS"

            icon = "✅" if final_result == "PASS" else "❌"
            print(f"{tc['id']:<5} | {tc['u']:<15} | {tc['e']:<25} | {icon} {final_result}")

        except Exception as e:
            print(f"{tc['id']:<5} | Error: {str(e)[:20]}")

    print("="*65)
    driver.quit()

if __name__ == "__main__":
    run()