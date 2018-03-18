import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


@pytest.fixture
def driver(request):
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    wd = webdriver.Chrome(chrome_options=chrome_options)
    #print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd

def clickn_check(driver):
    wait = WebDriverWait(driver, 5)
    el_list = driver.find_elements_by_xpath('//*[@id="app-"]/a')
    #print(len(el_list))
    for x in range(len(el_list)):
        el_list[x].click()
        el_list = driver.find_elements_by_xpath('//*[@id="app-"]/a')
        wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'h1')))
        internal = driver.find_elements_by_xpath('//*[@id="app-"]/ul/li')
        #print(len(internal))
        for y in range(1, len(internal)):
            internal[y].click()
            internal = driver.find_elements_by_xpath('//*[@id="app-"]/ul/li')
            el_list = driver.find_elements_by_xpath('//*[@id="app-"]/a')
            wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'h1')))


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
    clickn_check(driver)
    