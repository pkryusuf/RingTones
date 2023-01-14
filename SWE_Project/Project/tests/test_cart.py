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

def test_add_cart(client):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),)
    driver.get("http://localhost/signin")
    driver.find_element("id",'floatingInput').send_keys("q@q")
    driver.find_element("id",'floatingPassword').send_keys("6060")
    driver.find_element("id",'signin_button').click()
    
    user = DB().find_user_with_email("q@q", "6060")
    DB().add_to_cart(user["Id"], 1)
    driver.get("http://localhost/cart")
    
    assert '<p style="padding-left: 30%;">Rain</p>' in driver.page_source

def test_remove_cart(client):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),)
    driver.get("http://localhost/signin")
    driver.find_element("id",'floatingInput').send_keys("q@q")
    driver.find_element("id",'floatingPassword').send_keys("6060")
    driver.find_element("id",'signin_button').click()
    
    user = DB().find_user_with_email("q@q", "6060")
    
    driver.get("http://localhost/cart")
    
    driver.find_element("id",'trashcan').click()
    
    assert '<p style="padding-left: 30%;">Rain</p>' not in driver.page_source

def test_checkout_cart(client):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),)
    driver.get("http://localhost/signin")
    driver.find_element("id",'floatingInput').send_keys("q@q")
    driver.find_element("id",'floatingPassword').send_keys("6060")
    driver.find_element("id",'signin_button').click()
    
    user = DB().find_user_with_email("q@q", "6060")
    
    driver.get("http://localhost/cart")
    
    driver.find_element("id",'complete_cart').click()
    
    assert '<title>Thank You</title>' in driver.page_source
    



    

    




