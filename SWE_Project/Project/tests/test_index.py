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

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)

def test_home_load(client):
    response = requests.get("http://localhost")
    print(response)
    assert response.status_code == 200
    assert b"<title>Zil Sepeti</title>" in response.content
    
def test_home_filter_minmax_value(client):

    driver.get("http://localhost")
    
    driver.find_element("id",'inputMax').send_keys("134")
    driver.find_element("id",'inputMin').send_keys("25")
    driver.find_element("id",'inputMin').send_keys(Keys.RETURN)
    
    
    assert '<h5 class="card-title">Rain</h5>' not in driver.page_source
    assert '<h5 class="card-title">Birds In Nature</h5>' in driver.page_source

def test_home_filter_category_value(client):
    driver.get("http://localhost")
    driver.find_element("id",'Nature').click()
    
    assert '<h5 class="card-title">Rain</h5>' in driver.page_source
    assert '<h5 class="card-title">Birds In Nature</h5>' in driver.page_source
    assert '<h5 class="card-title">Sponge Bob</h5>' not in driver.page_source

def test_home_filter_search_value(client):
    driver.get("http://localhost")
    driver.find_element("id",'search').send_keys("Birds")
    
    assert '<h5 class="card-title">Rain</h5>' not in driver.page_source
    assert '<h5 class="card-title">Birds In Nature</h5>' in driver.page_source
    assert '<h5 class="card-title">Sponge Bob</h5>' not in driver.page_source


def test_home_signin_button(client):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),)
    driver.get("http://localhost")
    driver.find_element("id",'dropsign').click()
    driver.find_element("id",'signinn').click()
    
    assert '<title>Signin</title>' in driver.page_source

def test_home_order_button_fail(client):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),)
    driver.get("http://localhost")
    driver.find_element("id",'cart').click()

    assert '<title>Signin</title>' in driver.page_source
    

def test_home_home_button_success(client):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),)
    driver.get("http://localhost")
    driver.find_element("id",'home').click()

    assert '<title>Signin</title>' not in driver.page_source
    assert '<title>Zil Sepeti</title>' in driver.page_source
    # check selenium driver http status code
    
def test_sigin_pageload(client):
    response = requests.get("http://localhost/signin")
    print(response.content)
    assert response.status_code == 200

def test_sigin(client):
    response = requests.post("http://localhost/signin",data={"email":"q@q","password":"6060"})
    user = DB().find_user_with_email("q@q","6060")
    print(response.content)
    assert response.status_code == 200
    assert b"<title>Zil Sepeti</title>" in response.content
    assert bytes(user["Name"], 'utf-8') in response.content
    assert b"Sign In" not in response.content

def test_sigout(client):
    response = requests.get("http://localhost/signout")
    print(response.content)
    assert response.status_code == 200
    assert b"<title>Zil Sepeti</title>" in response.content