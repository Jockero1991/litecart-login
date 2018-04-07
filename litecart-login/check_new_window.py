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
    all_windws = driver.window_handles

    # Получить элементы всех ссылок на внешние источники.
    ext_links = driver.find_elements_by_class_name('fa-external-link')
    for x in range(len(ext_links)):
        start_window = driver.current_window_handle
        
        #print(start_window)
        ext_links[x].click()
        sleep(5)
        all_windws = driver.window_handles
        
        newWindow = all_windws[1]
        driver.switch_to.window(newWindow)
        
        sleep(1)
        driver.close()
        
        driver.switch_to.window(start_window)
        
        sleep(2)






