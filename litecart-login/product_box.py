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

def test_main(driver):
    #check_the_box(driver)
    add_to_box(driver, check_the_box(driver))

def add_to_box(driver, count):
    wait = WebDriverWait(driver, 3)
    # При условии что элементов в корзине меньше 3х выполнить поиск первого продукта и добавление его в корзину.
    if count < 3:
        driver.find_element_by_xpath('//*[@name="add_cart_product"]').click()
        sleep(2)
        add_to_box(driver, check_the_box(driver))
    # когда товаров в корзине будет 3, удалить товары 1 за другим.
    if count == 3:
        print('В корзине 3 товара')
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Checkout »'))).click()
        #sleep(1)
        while(count is not 0):
            try:
                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@name="remove_cart_item"]'))).click()
                sleep(1)
                count -= 1
                #print(count)
            except:
                count -= 1
                #print(count)
                print('end of the test')

# Открыть страницу найденного товара, получить и вернуть кол-во товаров в корзине
def check_the_box(driver):
    wait = WebDriverWait(driver, 3)
    driver.get('http://localhost/litecart/en/')
    driver.find_element_by_class_name('product').click()
    count = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'quantity'))).text
    
    return int(count)