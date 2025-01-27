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
conn = sqlite3.connect('painters_data.db')
c = conn.cursor()
try:
    c.execute('''
        CREATE TABLE painters (
            name TEXT,
            birth TEXT,
            death TEXT,
            nationality TEXT
        )
    ''')
except Exception as e:
    print(e)

def insert_data(name, birth, death, nationality):
    conn = sqlite3.connect('painters_data.db')
    c = conn.cursor()
    # Insert into the database
    c.execute('''
        INSERT INTO painters(name, birth, death, nationality)
        VALUES (:name, :birth, :death, :nationality)
    ''',
      {
          'name': name,
          'birth': birth,
          'death': death,
          'nationality': nationality
      })
    conn.commit()
    conn.close()
# I. Tai noi chua links
all_links = []
# II. Lay ra tat ca duong dan de truy cap den painters
# Khởi tạo Webdriver
for i in range(65,66):
    driver = webdriver.Chrome()
    url = "https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22"+chr(i)+"%22"
    try:
        # Mở trang
        driver.get(url)

        # Đợi một chút để trang tải
        time.sleep(3)

        # Lay ra tat cac ca the ul
        ul_tags = driver.find_elements(By.TAG_NAME, "ul")
        print(len(ul_tags))

        # Chon the ul thu 21
        ul_painters = ul_tags[20]  # list start with index=0

        # Lay ra tat ca the <li> thuoc ul_painters
        li_tags = ul_painters.find_elements(By.TAG_NAME, "li")

        # Tao danh sach cac url
        links = [tag.find_element(By.TAG_NAME, "a").get_attribute("href") for tag in li_tags]
        for x in links:
            all_links.append(x)
    except:
        print("Error!")

    # Dong webdrive
    driver.quit()
######################################################
# III. Lay thong tin cua tung hoa si
        # Khoi tao webdriver
for link in all_links:
    try:
        driver = webdriver.Chrome()
        # Mo trang
        url = link
        driver.get(url)

        # Doi 2 giay
        time.sleep(2)

        # Lay ten hoa si
        try:
            name = driver.find_element(By.TAG_NAME, "h1").text
        except:
            name = ""
        # Lay ngay sinh
        try:
            birth_element = driver.find_element(By.XPATH, "//th[text()='Born']/following-sibling::td")
            birth = birth_element.text
            birth = re.findall(r'[0-9]{1,2}+\s+[A-Za-z]+\s+[0-9]{4}', birth)[0] # regex
        except:
            birth = ""
# Lay ngay mat
        try:
            death_element = driver.find_element(By.XPATH, "//th[text()='Died']/following-sibling::td")
            death = death_element.text
            death = re.findall(r'[0-9]{1,2}+\s+[A-Za-z]+\s+[0-9]{4}', death)[0]
        except:
            death = ""
        # Lay ngay mat
        try:
            nationality_element = driver.find_element(By.XPATH, "//th[text()='Nationality']/following-sibling::td")
            nationality = nationality_element.text
        except:
            nationality = ""

        #Insert data into the database
        insert_data(name, birth, death, nationality)
        # Dong web driver
        driver.quit()
    except :
        pass
