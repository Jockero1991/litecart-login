import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
#import assert


@pytest.fixture
def driver(request):
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    wd = webdriver.Chrome(chrome_options=chrome_options)
    #print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd

def test_ducks_v2(driver):
    driver.get('http://localhost/litecart/en/')
    sleep(1)
    products = driver.find_elements_by_class_name('product')
    #print(products)
    counter=0
    for x in range(len(products)):
        
        if len(driver.find_elements_by_class_name('product')[x].find_elements_by_class_name('sticker')) == 1:
            counter += 1
    if len(products) == counter:
        print(f' Кол-во стикеров {counter} равно кол-ву продуктов: {len(products)} \n У каждого продукта 1 стикер.')
    else:
        print('Кол-во стикеров не равно кол-ву продуктов или у какого-то продукта больше 1 стикера')