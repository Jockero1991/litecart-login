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

def test_ducks(driver):
    driver.get('http://localhost/litecart/en/')
    all_ducks = driver.find_elements_by_xpath('//*[@class="product column shadow hover-light"]/a')
    print(all_ducks[1].get_attribute('title')) # [0].get_attribute('alt')