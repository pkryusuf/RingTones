import responses 
import requests
from Project import DataBase as DB
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_loadOwned(client):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),)
    driver.get("http://localhost/signin")
    driver.find_element("id",'floatingInput').send_keys("q@q")
    driver.find_element("id",'floatingPassword').send_keys("6060")
    driver.find_element("id",'signin_button').click()
    
    driver.find_element("id",'dropsign').click()
    driver.find_element("id",'myringtones').click()

    assert '<h5 class="card-title">Rain</h5>' in driver.page_source
    