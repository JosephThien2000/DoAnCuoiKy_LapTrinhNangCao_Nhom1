from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidSessionIdException
from tkinter.filedialog import askopenfilename, asksaveasfilename
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
import requests
import os
from main import *


path = "C:/Users/Public/Documents/"

# Run driver with Chromedriver
def get_wb_t(url):
    global driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    # driver.maximize_window()
    driver.minimize_window()
    sleep(5)

# Change directory function
def change_dir(path):
    """
        Tạo thư mục mới và thay đổi thư mục path hiện tại thành thư mục mới
    """
    global driver
    # change directory to current path
    os.chdir(path)

    # create new directory
    new_dir = os.path.join(path, 'text')

    # check if directory exists
    try:
        os.mkdir(new_dir)
    except:
        for retry in range(100):
            try:
                os.rename(new_dir,new_dir)
                break
            except:
                print("rename failed, retrying...")

    return os.chdir(new_dir)

topics = []
def crawl_texts():
    """
        Cào dữ liệu video của trang web nasa.gov
    """
    global driver
    main = driver.find_element(By.ID, "main")
    tag_list = main.find_element(By.XPATH, '//*[@id="tag-list"]')
    hrefs = tag_list.find_elements(By.TAG_NAME, "a")

    for href in hrefs:
        topics.append(href.get_attribute("href"))

    print("Crawl texts successfully!")

def download_texts(url):
    """
        Download text về máy tính
    """
    global path, count

    change_dir(path)

#     filepath = asksaveasfilename(
#     defaultextension=".txt",
#     filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
# )
#     if not filepath:
#         return

#     with open(filepath, mode="w", encoding="utf-8") as output_file:
#         output_file.write(f"{url}")

    with open(f"{url.split('/')[-1]}.txt", 'w') as f:
        f.writelines(f"{url}")

    print("Download text successfully!")


# if __name__ == "__main__":
    
#     # Run driver with Chromedriver
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

#     # open link
#     driver.get(url)
#     # driver.maximize_window()
#     driver.minimize_window()

#     sleep(5)

#     # crawl data
#     crawl_texts()

#     # # show href of topics
#     for topic in topics:
#         print(topic)

#     sleep(5)

#     driver.close()