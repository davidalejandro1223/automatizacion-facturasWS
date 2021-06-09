import unittest
import json
import locale
import logging
import calendar
from datetime import datetime

from pyunitreport import HTMLTestRunner
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

locale.setlocale(locale.LC_TIME, 'es_CO.UTF-8')

class FacturasWS(unittest.TestCase):
    def setUp(self):
        self.set_invoice_values()
        self.driver = self.get_driver()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get("https://facturas.ws/")

    def set_invoice_values(self):
        with open("invoice_values.json", "r") as f:
            values = json.load(f)
        for key, value in values.items():
            setattr(self, key, value)
    
    def get_driver(self, browser_name=None):
        drivers = {
            "firefox": self.get_firefox_driver,
            "chrome": self.get_chrome_driver,
        }
        if browser_name:
            return drivers[browser_name]()
        
        for method in drivers.values():
            try:
                return method()
            except Exception as e:
                logging.warning(e)
        raise Exception("No existe ningún webdriver instalado")
    
    def get_firefox_driver(self):
        try:
            return webdriver.Firefox()
        except:
            raise Exception("No se encontró el webdriver para firefox (geckodriver)")

    def get_chrome_driver(self):
        try:
            return webdriver.Chrome()
        except WebDriverException: 
            raise Exception("No se encontró el webdriver para chrome (chromedriver)")

    def test_client_name(self):
        due_date_field = self.driver.find_element_by_xpath(
            '//div/input[@class="inv-due-date"]'
        )
        due_date_field.clear()
        due_date_field.send_keys(self.get_due_date())

        client_name_field = self.driver.find_element_by_xpath(
            '//input[@name="client-name"]'
        )
        client_name_field.click()
        client_name_field.clear()
        client_name_field.send_keys(self.client_name)

        client_address_field = self.driver.find_element_by_xpath(
            '//textarea[@name="client-address"]'
        )
        client_address_field.clear()
        client_address_field.send_keys(self.client_address)

        client_province_field = self.driver.find_element_by_xpath(
            '//input[@name="client-city"]'
        )
        client_province_field.clear()
        client_province_field.send_keys(self.client_province)

        client_city_field = self.driver.find_element_by_xpath(
            '//input[@name="client-state"]'
        )
        client_city_field.clear()
        client_city_field.send_keys(self.client_city)

        client_country_field = self.driver.find_element_by_xpath(
            f'//select[@name="client-country"]/option[@value="{self.client_country}"]'
        )
        client_country_field.click()

        my_name_field = self.driver.find_element_by_xpath(
            '//input[@name="company-name"]'
        )
        my_name_field.clear()
        my_name_field.send_keys(self.my_name)

        my_address_field = self.driver.find_element_by_xpath(
            '//textarea[@name="company-address"]'
        )
        my_address_field.clear()
        my_address_field.send_keys(self.my_address)

        my_city_field = self.driver.find_element_by_xpath(
            '//input[@name="company-city"]'
        )
        my_city_field.clear()
        my_city_field.send_keys(self.my_city)

        my_province_field = self.driver.find_element_by_xpath(
            '//input[@name="company-state"]'
        )
        my_province_field.clear()
        my_province_field.send_keys(self.my_province)

        my_country_field = self.driver.find_element_by_xpath(
            f'//select[@name="company-country"]/option[@value="{self.my_country}"]'
        )
        my_country_field.click()

        ads = self.driver.find_elements_by_xpath('//div[@class="google-auto-placed"]')
        for ad in ads:
            try:
                self.driver.execute_script("arguments[0].remove()", ad)
            except:
                pass
        
        invoice_items = self.driver.find_elements_by_xpath(
            '//div[@id="invoice-items"]/div'
        )
        
        for item in invoice_items:
            if item.get_attribute("data-divid") == "1":
                continue
                
            remove_item_button = item.find_element_by_xpath(
                f'//div[@id="invoice-items"]/div[2]/div[@class="remove-row"]'
            )
            self.driver.execute_script(
                "arguments[0].style='display: block;'", remove_item_button
            )
            remove_item_button.click()

        product_description_field = self.driver.find_element_by_xpath('//div[@class="item-cell"]/input')
        product_description_field.clear()
        product_description_field.send_keys(self.get_product_description())

        fee_field = self.driver.find_element_by_xpath('//div[@class="price-cell"]/input')
        fee_field.click()
        fee_field.send_keys(self.my_fees)

        taxes_field = self.driver.find_element_by_xpath('//div[@class="grand-vat"]/input')
        taxes_field.clear()
        taxes_field.send_keys(self.taxes)

        currency_field = self.driver.find_element_by_xpath(f'//*[@id="currency"]/option[@value="{self.currency}"]')
        currency_field.click()

        download_field = self.driver.find_element_by_xpath('//div[@class="submibtn"]/button')
        download_field.click()
    
    def get_product_description(self):
        separator = "-"
        month_year = datetime.now().strftime("%B %Y")
        return separator.join([self.my_position, self.my_area, month_year])
    
    def get_due_date(self):
        now = datetime.now()
        month_last_day = calendar.monthrange(now.year, now.month)[1]
        return now.replace(day=month_last_day).strftime("%m/%d/%Y")
    
    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main(
        verbosity=2,
        testRunner=HTMLTestRunner(output="reportes", report_name="FacturasWS-report"),
    )
