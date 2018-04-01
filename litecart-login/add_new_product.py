import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os

@pytest.fixture
def driver(request):
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    wd = webdriver.Chrome(chrome_options=chrome_options)
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd

def test_main(driver):
    wait = WebDriverWait(driver, 4)
    print('Открываем страницу админки')
    driver.get('http://localhost/litecart/admin/')
    sleep(2)
    print('Вводим логин')
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@name="username"]'))).send_keys('admin')
    print('Вводим пароль')
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@name="password"]'))).send_keys('admin')
    print('Жмем кнопку login')
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@name="login"]'))).click()
    sleep(2)
    add_new_product(driver)

def add_new_product(driver):
    wait = WebDriverWait(driver, 4)
    # General
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="box-apps-menu"]/li[2]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div/a[2]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-general"]/table/tbody/tr[2]/td/span/input'))).send_keys('Punk Duck')
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-general"]/table/tbody/tr[3]/td/input'))).send_keys('123432')
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-general"]/table/tbody/tr[4]/td/div/table/tbody/tr[2]/td[1]/input'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-general"]/table/tbody/tr[7]/td/div/table/tbody/tr[4]/td[1]/input'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-general"]/table/tbody/tr[8]/td/table/tbody/tr/td[1]/input'))).send_keys('432')
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-general"]/table/tbody/tr[9]/td/table/tbody/tr[1]/td/input'))).send_keys(os.path.abspath('utochka_rockstar-1b.jpg'))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-general"]/table/tbody/tr[10]/td/input'))).send_keys('14032018')
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-general"]/table/tbody/tr[11]/td/input'))).send_keys('28052018')
    # Information
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/form/div/ul/li[2]/a'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-information"]/table/tbody/tr[1]/td/select'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-information"]/table/tbody/tr[1]/td/select/option[2]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-information"]/table/tbody/tr[2]/td/select'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-information"]/table/tbody/tr[3]/td/input'))).send_keys('rock_duck')
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-information"]/table/tbody/tr[4]/td/span/input'))).send_keys('duck that rock!')
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-information"]/table/tbody/tr[5]/td/span/div/div[2]'))).send_keys('Test')
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-information"]/table/tbody/tr[6]/td/span/input'))).send_keys('Rock Duck')
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-information"]/table/tbody/tr[7]/td/span/input'))).send_keys('Test')
    # Prices
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/form/div/ul/li[4]/a'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-prices"]/table[1]/tbody/tr/td/input'))).send_keys('900')
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-prices"]/table[1]/tbody/tr/td/select'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tab-prices"]/table[1]/tbody/tr/td/select/option[2]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/form/p/span/button[1]'))).click()