from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def search_amazon(product_name):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    options.add_argument(r"user-data-dir=C:\selenium-amazon-profile")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get("https://www.amazon.in/")

    wait = WebDriverWait(driver, 15)
    
    search_bar = wait.until(
        EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
    )

    search_bar.send_keys(product_name)
    search_bar.send_keys(Keys.ENTER)

    time.sleep(3)
    url = driver.current_url
    driver.quit()

    return url