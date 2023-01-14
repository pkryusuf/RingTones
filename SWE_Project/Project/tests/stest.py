from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path=r"./chromedriver.exe",)
driver.get("http://localhost")
time.sleep(5)
driver.find_element("id",'inputMax').send_keys("134")
time.sleep(5)

