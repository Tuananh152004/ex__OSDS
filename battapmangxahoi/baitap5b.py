
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
import time
import pandas as pd
import getpass

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
url = 'https://www.reddit.com/login/'

# Truy cập
driver.get(url)
time.sleep(7)

# Nhap thong tin nguoi dung
my_email = input('Please provide your email:')
my_password = getpass.getpass('Please provide your password:')

actionChains = ActionChains(driver)
time.sleep(1)
for i in range(5):
    actionChains.key_down(Keys.TAB).perform()

actionChains.send_keys(my_email).perform()
actionChains.key_down(Keys.TAB).perform()

actionChains.send_keys(my_password + Keys.ENTER).perform()

time.sleep(5)
# Truy cap trang post bai
url2 = 'https://www.reddit.com/user/phuongtex15/submit/?type=TEXT'
driver.get(url2);
time.sleep(2)

for i in range(17):
    actionChains.key_down(Keys.TAB).perform()

actionChains.send_keys('Vi du post').perform()

actionChains.key_down(Keys.TAB)
actionChains.key_down(Keys.TAB).perform()

actionChains.send_keys('NGUYEN TUAN ANH').perform()

for i in range(2):
    actionChains.key_down(Keys.TAB).perform()
    time.sleep(3)

actionChains.send_keys(Keys.ENTER).perform()

time.sleep(120)
driver.quit()