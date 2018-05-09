import datetime as dt
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener

class MyListener(AbstractEventListener):
    def before_find(self, by, value, driver):
        print(by, value)
    def after_find(self, by, value, driver):
        print(by, value, "found")
    def on_exception(self, exception, driver):
        print(exception)
        tod=str(dt.datetime.today().timestamp())
        tod = f"Screen-{tod}.png"
        #print(tod)
        driver.get_screenshot_as_file(tod)
        

@pytest.fixture
def driver(request):
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    caps=DesiredCapabilities.CHROME
    #caps['loggingPrefs']={'browser': 'ALL'}
    caps['loggingPrefs'] = {'performance': 'ALL'}
    wd = EventFiringWebDriver(webdriver.Chrome(
        chrome_options=chrome_options, desired_capabilities = caps
    ), MyListener())

    print(caps)
    
    request.addfinalizer(wd.quit)
    return wd

def get_browser_logs(driver, typ):
    for l in driver.get_log(typ):
        print(l)
def test_openpage(driver):
    driver.get("http://www.lostfilm.tv/series/Colony/season_3/episode_1")
    get_browser_logs(driver, 'performance')

def test_login_success(driver):
    wait = WebDriverWait(driver, 1)
    #get_browser_logs(driver)
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