import time

import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver(request):
    browser = webdriver.Chrome()
    yield browser
    browser.quit()


def test_all_chapter(driver):
    # авторизация в админке
    driver.get("http://localhost/litecart/admin")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    # открытие страницы с геозонами
    driver.get("http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones")
    countries = driver.find_elements_by_xpath("//*[@name='geo_zones_form']//tr[@class='row']")
    countrie_list = []
    # составляем список стран
    for countrie in countries:
        countrie_list.append(countrie.find_element_by_xpath(".//a").get_attribute("text"))
    # по составленному списку ищем каждый раз следующую страну
    for contrie_find in countrie_list:
        driver.find_element_by_xpath("//a[text()='" + contrie_find + "']").click()
        # составляем список зон в стране
        zones = driver.find_elements_by_xpath("//*[@class='dataTable']//*[contains(@name, '[zone_code]')]")
        zone_sample = "A"
        # для кажой зоны делаем проверку
        for zone in zones:
            # получаем название геозоны
            opt = zone.find_element_by_xpath("./option[@selected]").get_attribute("innerHTML")
            if len(opt) > 0:
                assert zone_sample <= opt
                zone_sample = opt
        driver.back()