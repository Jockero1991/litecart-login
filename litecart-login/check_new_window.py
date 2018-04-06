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
    # Открыть страницу создания страны
    driver.find_elements_by_id('app-')[2].click()
    driver.find_element_by_xpath('//*[@id="content"]//a[@class="button"]').click()
    sleep(1)

    # Получить элементы всех ссылок на внешние источники.
    ext_links = driver.find_elements_by_class_name('fa-external-link')
    for x in range(len(ext_links)):
        ext_links = driver.find_elements_by_class_name('fa-external-link')
        start_window = driver.current_window_handle
        all_windws = driver.window_handles
        ext_links.click()
        #newWindow = wait.until((existingWindows))
        sleep(4)

def find_new_win(arr1, arr2, driver):
    for t in range(len(arr1)):
        for z in range(len(arr2)):
            if arr1[t] <> arr2[z]:
                






