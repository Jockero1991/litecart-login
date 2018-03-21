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

def test_ducks(driver):
    driver.get('http://localhost/litecart/en/')
    try:
        all_ducks = driver.find_elements_by_xpath('//*[@class="product"]/a[1]/div[1]/img')
        all_stickers = driver.find_elements_by_xpath('//*[@class="product"]/a[1]/div[1]/div[1]')
    except:
        print('Ошибка при получении списков уток и стикеров')
    pairs = {}
    err_count = 0
    for x in range(len(all_ducks)):
        if all_ducks[x].get_attribute('alt') not in pairs.keys():
            if all_stickers[x].get_attribute('class') != None:
                pairs.update({all_ducks[x].get_attribute('alt') : all_stickers[x].get_attribute('class')})
            else:
                print('у утки ' + str(all_ducks[x].get_attribute('alt')) + ' нет стикера.')
        else:
            if pairs[all_ducks[x].get_attribute('alt')] != all_stickers[x].get_attribute('class'):
                err_count += 1
                print(all_ducks[x].get_attribute('alt'), str('already exists: ' + pairs[all_ducks[x].get_attribute('alt')]), str('trying to add: ' + all_stickers[x].get_attribute('class')))
    if err_count==0:
        print('У всех уток уникальные стикеры')
    else:
        print('Кол-во разных стикеров для одинаковых уток: ' + str(err_count))