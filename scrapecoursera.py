from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = r"C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://www.edx.org/")



search = driver.find_elements_by_id("home-search")
search.send_keys("Artificial Intelligence")
search.send_keys(Keys.RETURN)

time.sleep(3)
