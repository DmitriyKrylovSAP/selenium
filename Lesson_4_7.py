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
    #открытие главной
    driver.get("http://localhost/litecart")
    #список разделов с товарор
    product_list = {"box-most-popular",
                    "box-campaigns",
                    "box-latest-products"}
    # перебираем все разделы из списка
    for list in product_list:
        chapter = driver.find_element_by_id(list)
        # составляем список товаров в разделе
        product_list = chapter.find_elements_by_css_selector(".product.column")
        print(product_list)
        # для каждого товара проверяем стикер
        for product in product_list:
            assert product.find_element_by_class_name("sticker")
