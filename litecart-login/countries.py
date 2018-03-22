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

    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd

def test_login_success(driver):
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
    sorting_countr(driver)

def sorting_countr(driver):
    driver.get('http://localhost/litecart/admin/?app=countries&doc=countries')
    table_text = driver.find_elements_by_xpath('//*[@class="dataTable"]//tr[@class="row"]')
    table_text = [x.text for x in table_text] # долго отрабатывает, причем неважно какой цикл ни ставь.
    countrys = []# Массив стран
    count_geo = [] # массив кол-ва геозон
    for x in range(len(table_text)):
        countrys.append(table_text[x].split(' ')[2 : (len(table_text[x].split(' ')) - 1)])
        countrys[x] = ' '.join(countrys[x])
        count_geo.append(table_text[x].split(' ')[(len(table_text[x].split(' ')) - 1)])
        print(countrys[x], count_geo[x])

    