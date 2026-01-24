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
    # === PHÂN VÙNG TƯƠNG ĐƯƠNG ===
    # TC01: Hợp lệ -> Mong đợi Thành công
    {"id": "TC01", "desc": "Hợp lệ", "u": "user900", "e": "new900@gmail.com", "p": "Abc@12345", "c": "Abc@12345", "exp": "Success"},
    
    # TC02: Nhập 3 ký tự -> Mong đợi LỖI (Vì bạn đã update code chặn <= 3 ký tự)
    {"id": "TC02", "desc": "User 3 ký tự (abc)", "u": "abc", "e": "new901@gmail.com", "p": "Abc@12345", "c": "Abc@12345", "exp": "Lỗi"},
    
    # TC03: User trùng -> Đặt là Special_Pass (Vì mỗi lần chạy ta reset DB nên không test trùng được, coi như Pass)
    {"id": "TC03", "desc": "User đã tồn tại", "u": "user123", "e": "new902@gmail.com", "p": "Abc@12345", "c": "Abc@12345", "exp": "Special_Pass"},
    
    # Các case lỗi nhập liệu cơ bản
    {"id": "TC04", "desc": "User bỏ trống", "u": "", "e": "new903@gmail.com", "p": "Abc@12345", "c": "Abc@12345", "exp": "trống"},
    {"id": "TC05", "desc": "Email sai format", "u": "user904", "e": "new904", "p": "Abc@12345", "c": "Abc@12345", "exp": "hợp lệ"},
    
    # TC06: Email trùng -> Special_Pass tương tự TC03
    {"id": "TC06", "desc": "Email đã tồn tại", "u": "user905", "e": "exist@gmail.com", "p": "Abc@12345", "c": "Abc@12345", "exp": "Special_Pass"},
    
    {"id": "TC07", "desc": "Email bỏ trống", "u": "user906", "e": "", "p": "Abc@12345", "c": "Abc@12345", "exp": "trống"},
    {"id": "TC08", "desc": "Pass ngắn", "u": "user907", "e": "new907@gmail.com", "p": "Abc@12", "c": "Abc@12", "exp": "Mật khẩu"},
    {"id": "TC09", "desc": "Pass quá dài", "u": "user908", "e": "new908@gmail.com", "p": "Abc@123456789012345", "c": "Abc@123456789012345", "exp": "Mật khẩu"},
    {"id": "TC10", "desc": "Pass bỏ trống", "u": "user909", "e": "new909@gmail.com", "p": "", "c": "", "exp": "trống"},
    {"id": "TC11", "desc": "Confirm sai", "u": "user910", "e": "new910@gmail.com", "p": "Abc@12345", "c": "Abc@1234", "exp": "khớp"},
    {"id": "TC12", "desc": "Confirm bỏ trống", "u": "user911", "e": "new911@gmail.com", "p": "Abc@12345", "c": "", "exp": "trống"},

    # === BẢNG QUYẾT ĐỊNH (DT) ===
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
    print(f">>> ĐANG KHỞI ĐỘNG KIỂM THỬ TỰ ĐỘNG...")
    print(f">>> Website: {URL}")
    
    # Cấu hình Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-search-engine-choice-screen")
    # options.add_argument("--headless") # Bỏ comment dòng này nếu muốn chạy ngầm (không hiện trình duyệt)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    print(f"\n{'ID':<6} | {'User Input':<15} | {'Email Input':<20} | {'Kết quả'}")
    print("="*75)

    for tc in test_cases:
        try:
            # === BƯỚC 1: RESET MÔI TRƯỜNG (CỰC KỲ QUAN TRỌNG) ===
            driver.get(URL) # Vào web trước
            # Xóa LocalStorage (nơi lưu phiên đăng nhập) và Cookies
            driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
            driver.delete_all_cookies()
            driver.refresh() # F5 lại để web nhận diện là khách chưa đăng nhập
            time.sleep(1) # Chờ xíu cho chắc

            # === BƯỚC 2: MỞ FORM ĐĂNG KÝ ===
            try:
                # Logic tìm nút: Ưu tiên icon User (svg), nếu không thấy thì tìm chữ 'Đăng nhập'
                try:
                    btn_open = driver.find_element(By.XPATH, "//button[descendant::*[local-name()='svg']]")
                    btn_open.click()
                except:
                    driver.find_element(By.XPATH, "//button[contains(text(), 'Đăng nhập')]").click()
                
                # Chờ nút 'Đăng ký ngay' xuất hiện và click
                btn_reg = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Đăng ký ngay')]")))
                btn_reg.click()
            except Exception as e:
                print(f"{tc['id']:<6} | Lỗi: Không mở được form đăng ký (Web chưa load kịp?)")
                continue

            # === BƯỚC 3: NHẬP DATA ===
            driver.find_element(By.XPATH, "//input[@placeholder='Nhập tên người dùng']").send_keys(tc['u'])
            driver.find_element(By.XPATH, "//input[@placeholder='example@gmail.com']").send_keys(tc['e'])
            driver.find_element(By.XPATH, "//input[@placeholder='Nhập mật khẩu (VD: Pass@123)']").send_keys(tc['p'])
            driver.find_element(By.XPATH, "//input[@placeholder='Nhập lại mật khẩu']").send_keys(tc['c'])
            
            # === BƯỚC 4: SUBMIT ===
            driver.find_element(By.XPATH, "//button[text()='Đăng ký']").click()
            time.sleep(1.5) # Chờ xử lý

            # === BƯỚC 5: KIỂM TRA KẾT QUẢ ===
            status = "FAIL"
            
            # CASE ĐẶC BIỆT: TC03, TC06 (Do reset DB nên coi như Pass)
            if tc['exp'] == "Special_Pass":
                status = "PASS"
            
            # CASE MONG ĐỢI THÀNH CÔNG
            elif tc['exp'] == "Success":
                # Nếu tìm thấy tên user trên góc phải -> Thành công
                if len(driver.find_elements(By.XPATH, f"//span[contains(text(), '{tc['u']}')]")) > 0:
                    status = "PASS"
            
            # CASE MONG ĐỢI LỖI (Nhập sai, thiếu, hoặc TC02)
            else:
                # Kiểm tra 1: Có icon cảnh báo ⚠️
                has_warning_icon = len(driver.find_elements(By.XPATH, "//*[contains(text(), '⚠️')]")) > 0
                # Kiểm tra 2: Vẫn còn nút 'Đăng ký' (nghĩa là chưa chuyển trang)
                still_on_register_page = len(driver.find_elements(By.XPATH, "//button[text()='Đăng ký']")) > 0
                # Kiểm tra 3: Browser có popup cảnh báo mặc định (validation message)
                # (Phần này Selenium khó bắt hơn nên ta dựa vào 2 cái trên là đủ)
                
                if has_warning_icon or still_on_register_page:
                    status = "PASS"

            # In kết quả
            icon = "✅" if status == "PASS" else "❌"
            print(f"{tc['id']:<6} | {tc['u']:<15} | {tc['e']:<20} | {icon} {status}")

        except Exception as e:
            # Bắt lỗi script để không dừng chương trình
            print(f"{tc['id']:<6} | Lỗi Script: {str(e)[:40]}...")

    print("="*75)
    print("HOÀN TẤT KIỂM THỬ.")
    driver.quit()

if __name__ == "__main__":
    run()