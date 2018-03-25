import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from PIL import ImageColor as pl

@pytest.fixture
def driver(request):
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    wd = webdriver.Chrome(chrome_options=chrome_options)
    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd

    # Постановка:
    # 1) Получить данные о продукте: Наименование, цену, зачеркнутую цену, цвет и жирность акционной цены, размер шрифта акционной цены.
    # 2) Получить ссылку на страницу продукта и перейти по ней.
    # 3) Передать массив с данными в функцию для проверки  
    # 4) проверить совпадение имен и цен,
    #    - что обычная цена зачеркнута, 
    #    - что обычная цена серого цвета, 
    #    - что у акционной цены красный цвет шрифта (можно считать, что "красный" цвет это такой, у которого в RGBa представлении каналы G и B имеют нулевые значения) и более крупный и жирный шрифт

classes = ['regular-price', 'campaign-price']
prop = ['text', 'color', 'font-size', 'nodeName']

def test_main(driver):
    driver.get('http://localhost/litecart/en/')
    products = driver.find_element_by_xpath('//*[@id="box-campaigns"]').find_elements_by_class_name('product')
    t = aggr_products(driver, products)
    #print(t)
    for i in range(len(t)):
        #print(t[i][-1])
        driver.get(t[i][-1])
        check_product(driver, t[i])




def aggr_products(driver, pr):
    result_list = [[]]
    links =[]
    #products = driver.find_element_by_xpath('//*[@id="box-campaigns"]').find_elements_by_class_name('product')
    for x in range(len(pr)):
        for y in range(len(pr)):
            result_list[y].append(pr[x].find_element_by_class_name('name').text)
            prod_attr = ness_elem_attrs(driver, classes, prop)
            result_list[y] = list(result_list[y] + prod_attr)
            result_list[y].append(pr[x].find_element_by_class_name('link').get_attribute('href'))
    #print(result_list)
    return result_list

def check_product(driver, attrs):
    #driver.get(link)
    check_list = []
    
    check_list.append(driver.find_element_by_css_selector('h1.title').text)
    res = ness_elem_attrs(driver, classes, prop)
    check_list = list(check_list + res)
    # Проверка имени товара
    assert attrs[0] == check_list[0]
    # Проверка обычной цены товара на 2 экранах
    assert attrs[1] == check_list[1]
    # Проверка серого цвета обычной цены на обоих экранах независимо
    assert pl.getcolor(attrs[2], 'RGBa')[0]==pl.getcolor(attrs[2], 'RGBa')[1]==pl.getcolor(attrs[2], 'RGBa')[2]
    assert pl.getcolor(check_list[2], 'RGBa')[0]==pl.getcolor(check_list[2], 'RGBa')[1]==pl.getcolor(check_list[2], 'RGBa')[2]
    # Проверка что размер шрифта акционной цены больше шрифта обычной
    assert float(attrs[3].split('px')[0]) < float(attrs[-3].split('px')[0])
    assert float(check_list[3].split('px')[0]) < float(check_list[-2].split('px')[0])
    # проверка что обычная цена зачеркнута, тег S
    assert attrs[4]==check_list[4]=='S'
    # Проверка, что акционные цены совпадают и на главном и на странице товара.
    assert attrs[5]==check_list[5]
    # Проверка, что цвет акционной цены красный
    assert pl.getcolor(attrs[6], 'RGBa')[1]==pl.getcolor(attrs[6], 'RGBa')[2]==0
    assert pl.getcolor(check_list[6], 'RGBa')[1]==pl.getcolor(check_list[6], 'RGBa')[2]==0
    # Проверка, что шрифт акционной цены жирный на обоих экранах
    assert attrs[-2]==check_list[-1]=='STRONG'
    
    return check_list


def ness_elem_attrs(driver, cl_name, pr):
    ch_l = []
    for x in range(len(cl_name)):
        for f in range(len(pr)):
            if pr[f] == 'text':
                ch_l.append(driver.find_element_by_class_name(cl_name[x]).text)
            if pr[f] == 'color' or pr[f] == 'font-size':
                ch_l.append(driver.find_element_by_class_name(cl_name[x]).value_of_css_property(pr[f]))
            if pr[f] == 'nodeName':
                ch_l.append(driver.find_element_by_class_name(cl_name[x]).get_attribute(pr[f]))  
    return ch_l