import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import MySQLdb
import random

@pytest.fixture
def driver(request):
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    wd = webdriver.Chrome(chrome_options=chrome_options)
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd

def db_conn(quer):
    conn = MySQLdb.connect('127.0.0.1', 'root', '', 'litecart')
    cursor = conn.cursor()
    cursor.execute(quer)
    # Получаем данные.
    row = cursor.fetchall()
    result = []
    for x in range(len(row)):
        result.append(row[x][0])
    #Разрываем подключение.
    conn.close()
    return result

db_conn("SELECT `email` FROM `lc_customers`")

def check_email(gen='test@t.ru', db_list=[]):
    for x in range(len(db_list)):
        if gen == db_list[x]:
            print(f'{gen} - такой email уже зарегистрирован')
            return False
        else:
            return True

def email_generator():
    abc = 'qwertyuiopasdfghjklzxcvbnm'
    domens = ['.ru', '.com', '.tst']
    return ''.join(random.choice(abc) for _ in range(6)) + '@' + ''.join(random.choice(abc) for _ in range(4)) + ''.join(random.choice(domens) for _ in range(len(domens)-2))

def test_registration(driver):
    mail_val = ''
    mail_val = email_generator()
    password = 'Qwerty123'
    while check_email(mail_val, db_conn("SELECT `email` FROM `lc_customers`")) is not True:
        mail_val = email_generator()
        
    driver.get('http://localhost/litecart/en/')
    driver.find_element_by_id('box-account-login').find_element_by_tag_name('a').click()
    driver.find_element_by_name('firstname').send_keys('Yuriy')
    driver.find_element_by_name('lastname').send_keys('Ivanov')
    driver.find_element_by_name('address1').send_keys('Moscow, Gagarin street, 10')
    driver.find_element_by_name('postcode').send_keys('12345')
    driver.find_element_by_name('city').send_keys('Moscow')
    driver.find_element_by_class_name('select2-selection__rendered').click()
    driver.find_element_by_class_name('select2-search__field').send_keys('United States\n')
    driver.find_element_by_name('email').send_keys(mail_val)
    driver.find_element_by_name('phone').send_keys('9991238900')
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_name('confirmed_password').send_keys(password)
    driver.find_element_by_name('create_account').click()
    driver.find_element_by_id('box-account').find_elements_by_css_selector('.list-vertical li a')[-1].click()
    print(mail_val, password)
    
    driver.find_element_by_name('email').send_keys(mail_val)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_name('login').click()
    sleep(3)
    driver.find_element_by_id('box-account').find_elements_by_css_selector('.list-vertical li a')[-1].click()
    sleep(2)