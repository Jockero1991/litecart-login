import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import MySQLdb

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
    for x in range(len(row)):
        result.append(row[x][0])
    # Разрываем подключение.
    conn.close()
    return result
db_conn("SELECT `email` FROM `lc_customers`")

def check_email():
    pass

def email_generator():
    pass

def test_registration(driver):
    pass