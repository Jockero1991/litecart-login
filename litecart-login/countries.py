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
    sleep(1)
    aggregate(driver, 'country')
    aggregate(driver, 'geo')


    # нужна функция для проверки обоих сценариев.
def aggregate(driver, bead):
    bl = ['http://localhost/litecart/admin/?app=countries&doc=countries', 'http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones']
        
    if bead == 'country':
        driver.get(bl[0])
        table = driver.find_elements_by_xpath('//*[@class="dataTable"]//tr[@class="row"]')
        table_text = [x.text for x in table] # долго отрабатывает, почему непонятно
        countrys = []# Массив стран
        count_geo = [] # массив кол-ва геозон
        links = [] # ссылки на страны с кол-вом геозон больше 0
        for x in range(len(table_text)):
            countrys.append(table_text[x].split(' ')[2 : (len(table_text[x].split(' ')) - 1)])
            countrys[x] = ' '.join(countrys[x])
            count_geo.append(int(table_text[x].split(' ')[(len(table_text[x].split(' ')) - 1)]))
             
            if count_geo[x] > 0:
                links.append(driver.find_element_by_xpath('//*[@class="dataTable"]//tr[@class="row"][' + str(x+1) + ']//a').get_attribute('href'))
        sorting(driver, countrys)
        for y in range(len(links)):
            driver.get(links[y])
            list_for_chk=driver.find_elements_by_xpath('//*[@id="table-zones"]/tbody/tr//td[3]')
            list_for_chk = [x.text for x in list_for_chk]
            sorting(driver, list_for_chk)

    if bead == 'geo':
        driver.get(bl[1])
        table = driver.find_elements_by_xpath('//*[@class="dataTable"]//tr[@class="row"]')
        links = []
        for x in range(len(table)):
            links.append(driver.find_element_by_xpath('//*[@class="dataTable"]//tr[@class="row"][' + str(x+1) + ']//a').get_attribute('href'))
        for y in range(len(links)):
            driver.get(links[y])
            list_for_chk=driver.find_elements_by_xpath('//*[@id="table-zones"]/tbody/tr//td[3]')
            list_for_chk = [x.text for x in list_for_chk]
            sorting(driver, list_for_chk)

    
def sorting(driver, unordered_lst):
    ordered_list = []
    check_sum = 0
    errors = []
    ordered_list = sorted(unordered_lst)
    for i in range(len(unordered_lst)):
        if ordered_list[i] == unordered_lst[i]:
            check_sum += 1
        else:
            errors.append(unordered_lst[i])
    if check_sum == len(unordered_lst):
        print('Список отсортирован по алфавиту')
    else:
        print('Список не отсортирован!')

