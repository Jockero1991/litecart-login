import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener

@pytest.fixture
def driver(request):
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    caps=DesiredCapabilities.CHROME
    caps['loggingPrefs']={'browser': 'ALL'}
    #caps['loggingPrefs'] = {'performance': 'ALL'}
    wd = webdriver.Chrome(
        chrome_options=chrome_options, desired_capabilities = caps
    )

    print(caps)
    
    request.addfinalizer(wd.quit)
    return wd

def get_browser_logs(driver, typ):
    logs=[]
    for l in driver.get_log(typ):
        logs.append(l)
        #print(l)
    return logs

def test_login(driver):
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
    check_console_errors(driver)

def check_console_errors(driver):
    print("Переходим в каталог")
    cataloges = driver.find_elements_by_xpath('//*[@id="app-"]/a')[1].get_attribute("href")
    driver.find_elements_by_xpath('//*[@id="app-"]')[1].click()
    sleep(0.5)
    print("Разворачиваем каталог с товарами")
    driver.find_element_by_link_text("Rubber Ducks").click()
    sleep(1)
    ducks = driver.find_elements_by_xpath('//*[@class="row"]/td[3]/a')
    
    for i in range(1, len(ducks)):
        logs = []
        ducks[i].click()
        sleep(2)
        current_duck = driver.find_element_by_xpath('//*[@id="tab-general"]/table/tbody/tr[2]/td/span/input').get_attribute('value')
        print("Переходим в каталог")
        driver.get(cataloges)
        sleep(2)
        print("Разворачиваем каталог с товарами")
        driver.find_element_by_link_text("Rubber Ducks").click()
        ducks = driver.find_elements_by_xpath('//*[@class="row"]/td[3]/a')
        logs = get_browser_logs(driver, 'browser')
        if logs:
            print('This duck: ' + current_duck + ' has log!')
            print(logs)
    


