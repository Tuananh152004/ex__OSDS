from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import pandas as pd

# Đường dẫn đến file thực thi geckodriver
gecko_path = r"D:/code/geckodriver.exe"

# Khởi tởi đối tượng dịch vụ với đường geckodriver
ser = Service(gecko_path)

# Tạo tùy chọn
options = webdriver.firefox.options.Options();
options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
# Thiết lập firefox chỉ hiện thị giao diện
options.headless = False

# Khởi tạo driver
driver = webdriver.Firefox(options=options, service=ser)

# Tạo url
url = 'https://gochek.vn/collections/all'

# Truy cập
driver.get(url)

# Tạm dừng khoảng 2 giây
time.sleep(1)

# Tìm phần tử body của trang để gửi phím mũi tên xuống
body = driver.find_element(By.TAG_NAME, "body")
time.sleep(3)

# Nhấn phím mũi tên xuống nhiều lần để cuộn xuống từ từ
for i in range(50):  # Lặp 30 lần, mỗi lần cuộn xuống một ít
    body.send_keys(Keys.ARROW_DOWN)
    time.sleep(0.01)  # Tạm dừng 0.2 giây giữa mỗi lần cuộn để trang tải nội dung

# Tạm dừng thêm vài giây để trang tải hết nội dung ở cuối trang
time.sleep(1)

# Tao cac list
stt = []
ten_san_pham = []
gia_ban = []
hinh_anh = []

# Tìm tất cả sp trên trang
spgo =  driver.find_elements(By.XPATH, "//div[contains(@class,'product-block')]")
for i, goc in enumerate(spgo, 1):

    parent_div = goc
    sp = parent_div

    # Lat ten sp
    try:
        tsp = sp.find_element(By.TAG_NAME, 'h3').text
    except:
        tsp = ''

    # Lat gia sp
    try:
        gsp = sp.find_element(By.CLASS_NAME, "pro-price.highlight").text
        gsp1 = [el.text for el in gia_ban.find_elements(By.XPATH, ".//*[not(contains(@class, 'pro-price-del'))]")]
        gsp = " ".join(gsp1)
    except:
        gsp = sp.find_element(By.CLASS_NAME, "box-pro-prices").text

    # Lat hinh anh
    try:
        ha = sp.find_element(By.TAG_NAME, 'img').get_attribute('src')
    except:
        ha = ''

    # Chi them vao ds neu co ten sp
    if (len(tsp) > 0):
        stt.append(i)
        ten_san_pham.append(tsp)
        gia_ban.append(gsp)
        hinh_anh.append(ha)

# Tạo df
df = pd.DataFrame({
    "STT": stt,
    "Tên sản phẩm": ten_san_pham,
    "Giá bán": gia_ban,
    "Hình ảnh": hinh_anh

})

df.to_excel('danh_sach_sp_gochek.xlsx', index=False)