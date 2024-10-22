from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import sqlite3
import time
import re
import pandas as pd
######################################################
# 0. Create SQLite Database
conn = sqlite3.connect('musician_data.db')
c = conn.cursor()
try:
    c.execute('''
        CREATE TABLE musicians (
            name_of_band TEXT,
            years_active TEXT
        )
    ''')
except Exception as e:
    print(e)

def insert_data(name_of_band, years_active):
    conn = sqlite3.connect('musician_data.db')
    c = conn.cursor()
    # Insert into the database
    c.execute('''
        INSERT INTO musicians(name_of_band, years_active)
        VALUES (:name_of_band, :years_active)
    ''',
      {
          'name_of_band': name_of_band,
          'years_active': years_active,
      })
    conn.commit()
    conn.close()

######################################################
# 1. Scraping Data
# Tạo op để chạy chế độ ẩn
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--window-size=1920x1080")
# Initialize driver
driver = webdriver.Chrome(chrome_options)
# Access the target website
driver.get("https://en.wikipedia.org/wiki/Lists_of_musicians#A")
#dừng khoảng 3s
time.sleep(3)
# Tạo danh sách rỗng để chứa các liên kết đến tất cả link và nghệ sĩ
musician_links = []
all_links= []
try:
    #lấy tất cả các thẻ ul trong web danh mục
    ul_tags = driver.find_elements(By.TAG_NAME, "ul")
    print(len(ul_tags))

    #chọn ul thứ 22
    ul_musican = ul_tags[21]
    #lấy tất cả link chứa thông tin nhạc sĩ bắt đầu bằng chữ A thuộc ul_musican
    li_tags = ul_musican.find_elements(By.TAG_NAME, "li")
    print(len(li_tags))

    # tạo danh sách các url
    links = [tag.find_element(By.TAG_NAME,"a").get_attribute("href") for tag in li_tags]
    for x in links:
        all_links.append(x)
except:
    print("Error!!!!")
#tat man hinh
driver.quit()
#kiểm tra all_links có dữ liệu chưa
print(all_links)
#truy cập vô đường link đầu tiên của all_links
artists_driver = webdriver.Chrome(chrome_options)
artists_driver.get(all_links[0])

#dừng khoảng 2s
time.sleep(2)

try:
     #lấy tất cả các the ul của list of acid rock artists
    ul_artists_tags = artists_driver.find_elements(By.TAG_NAME, "ul")
    print(len(ul_artists_tags))

    #chọn ul thứ 25
    ul_artist = ul_artists_tags[24]
    #lấy tất cả link chứa thông tin thuộc artists
    li_artist = ul_artist.find_elements(By.TAG_NAME, "li")
    print(len(li_artist))
    # tạo danh sách các url của artist
    links_artist = [artist_tag.find_element(By.TAG_NAME,"a").get_attribute("href") for artist_tag in li_artist]
    for x in links_artist:
        musician_links.append(x)
except:
    print("Error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
artists_driver.quit()
#kiểm tra musician có dữ liệu chưa
print(musician_links)
# ... (phần đầu của mã không thay đổi)
# lấy thông tin của các nhạc sĩ ca sĩ
count = 0
for link in musician_links:
    if count >= 100:  # Dừng lại sau khi đã lấy thông tin cho 100 nhạc sĩ để xem có lỗi không
        break
    count += 1
    print(link)
    try:
        # khởi tạo webdriver
        driver = webdriver.Chrome(chrome_options)
        # mở trang web
        url = link
        driver.get(url)
        # đợi khoảng 3s
        time.sleep(3)
        # lấy tên ban nhạc
        try:
            name_of_band = driver.find_element(By.TAG_NAME, "h1").text
        except:
            name_of_band = ""

        # lay năm hoat dong
        try:
            year_active_element = driver.find_element(By.XPATH, value='//span[contains(text(),"Years active")]/parent::*/following-sibling::td')
            years_active = year_active_element.text
        except:
            years_active = ""
    except:
        print("Loi !!!")

    # Insert data into the database
    insert_data(name_of_band, years_active)

driver.quit()