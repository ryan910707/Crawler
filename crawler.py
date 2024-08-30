from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from io import BytesIO
import time
import numpy as np


# Define the URL with the stock_id
stock_id = input("Please enter the stock ID: ")
days = input("Please enter the number of days (1, 5, 10, 30, 72): ")
if days == "30":
    url = f"https://stockchannelnew.sinotrade.com.tw/z/zc/zcw/zcwg/zcwg_{stock_id}.djhtm"
else:
    url = f"https://stockchannelnew.sinotrade.com.tw/z/zc/zcw/zcwg/zcwg_{stock_id}_{days}.djhtm"


def crop_white_border(img):
    # Convert image to numpy array
    img_array = np.array(img)

    # Find the boundaries of the non-white area
    def find_edges(arr):
        return np.argwhere((arr != 255).any(axis=1))

    top = find_edges(img_array[:, :, 0]).min()
    bottom = find_edges(img_array[:, :, 0]).max()
    left = find_edges(img_array[:, :, 0].T).min()
    right = find_edges(img_array[:, :, 0].T).max()

    # Crop the image
    cropped_img = img.crop((left, top, right, bottom))
    return cropped_img


# Configure Selenium webdriver (ensure chromedriver is installed)
driver = webdriver.Chrome()

try:
    # Open the URL
    driver.get(url)

    # Wait for the iframe to load (adjust the locator to match your iframe)
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe")))

    # Wait a few seconds to ensure the content is fully loaded
    time.sleep(1)

    # Take a screenshot and load it directly with Pillow
    screenshot = driver.get_screenshot_as_png()
    img = Image.open(BytesIO(screenshot))

    # Crop and save the image
    cropped_img = crop_white_border(img)
    cropped_img.show()


finally:
    # Close the webdriver
    driver.quit()
