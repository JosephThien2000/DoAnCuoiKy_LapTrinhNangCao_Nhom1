from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidSessionIdException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from tkinter.filedialog import askopenfilename, asksaveasfilename
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
import requests
import os


path = "C:/Users/Public/Documents/"
images = []

# Run driver with Chromedriver
def get_wb_i(url):
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

    # change directory to current path
    os.chdir(path)

    # create new directory
    new_dir = os.path.join(path, 'image')

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


# Download_image function
def download_image(url):
    """
        Dowload ảnh về thư mục đã được tạo
    """

    global path

    # creat a new directory, change, and save image
    change_dir(path)

    # variables
    file_extension = url.split("/")[-1].split(".")[1]
    url_name = url.split("/")[-1].split(".")[0]
    
    # download image
    if ".jpg_low_res" not in url:
    #     # Save image function
    #     filepath = asksaveasfilename(
    #         title="Save image"
    #         , filetypes=(("JPG files", "*.jpg"), ("PNG files", "*.png"))
    #         , defaultextension=".jpg"
    #         , initialfile=url_name
    # )
    #     if not filepath:
    #         return

        with open(f'{url_name}.{file_extension}', 'wb') as handle:
            response = requests.get(url, stream=True)

            if not response.ok:
                print(response)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)

def crawl_images():
    """
        Cào dữ liệu ảnh của trang web nasa.gov
    """
    global driver

    gallery_container = driver.find_element(By.CLASS_NAME, "is-gallery")

    gallery_list = gallery_container.find_element(By.ID, "gallery-list")

    count = 1

    # Show more images in 10 times
    while count <= 10:
        next_page = gallery_list.find_element(By.XPATH, '//*[@id="trending"]')
        next_page.click()
        sleep(1) 
        count += 1
    
    gallery_items = gallery_list.find_elements(By.TAG_NAME, "img")

    for item in gallery_items:
        image = item.get_attribute("src")
        images.append(image)
        # download_image(image)
        # print(image)

    print("Successfully download image!")


# if __name__ == "__main__":
    
#     # Run driver with Chromedriver
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

#     # open link
#     driver.get(url)
#     driver.maximize_window()
#     driver.minimize_window()

#     sleep(5)

#     # crawl data
#     crawl_images()

#     sleep(5)

#     driver.close()