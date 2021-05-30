import unittest
import json
from pyunitreport import HTMLTestRunner
from selenium import webdriver


class FacturasWS(unittest.TestCase):
    def setUp(self):
        self.set_invoice_values()
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get("https://facturas.ws/")

    def set_invoice_values(self):
        with open("invoice_values.json", "r") as f:
            values = json.load(f)
        for key, value in values.items():
            setattr(self, key, value)

    def test_client_name(self):
        client_name_field = self.driver.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div[1]/div/ul/li[1]/input"
        )
        client_name_field.clear()
        client_name_field.send_keys(self.client_name)

        client_address_field = self.driver.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div[1]/div/ul/li[2]/textarea"
        )
        client_address_field.clear()
        client_address_field.send_keys(self.client_address)

        client_province_field = self.driver.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div[1]/div/ul/li[3]/input[1]"
        )
        client_province_field.clear()
        client_province_field.send_keys(self.client_province)

        client_city_field = self.driver.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div[1]/div/ul/li[3]/input[2]"
        )
        client_city_field.clear()
        client_city_field.send_keys(self.client_city)

        client_country_field = self.driver.find_element_by_xpath(
            f'/html/body/div[2]/div[2]/div[1]/div/ul/li[5]/select/option[@value="{self.client_country}"]'
        )
        client_country_field.click()

        my_name_field = self.driver.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div[2]/div[2]/ul/li[1]/input"
        )
        my_name_field.clear()
        my_name_field.send_keys(self.my_name)

        my_address_field = self.driver.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div[2]/div[2]/ul/li[2]/textarea"
        )
        my_address_field.clear()
        my_address_field.send_keys(self.my_address)

        my_city_field = self.driver.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div[2]/div[2]/ul/li[3]/input[1]"
        )
        my_city_field.clear()
        my_city_field.send_keys(self.my_city)

        my_province_field = self.driver.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div[2]/div[2]/ul/li[3]/input[2]"
        )
        my_province_field.clear()
        my_province_field.send_keys(self.my_province)

        my_country_field = self.driver.find_element_by_xpath(
            f'/html/body/div[2]/div[2]/div[2]/div[2]/ul/li[4]/select/option[@value="{self.my_country}"]'
        )
        my_country_field.click()

        invoice_items = self.driver.find_elements_by_xpath(
            '//div[@id="invoice-items"]/div'
        )
        for item in invoice_items:
            if item.get_attribute("data-divid") == "1":
                continue
            
            remove_item_button = item.find_element_by_xpath(
                f'//*[@id="invoice-items"]/div[2]/div[@class="remove-row"]'
            )
            self.driver.execute_script(
                "arguments[0].style='display: block;'", remove_item_button
            )
            remove_item_button.click()

        breakpoint()

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main(
        verbosity=2,
        testRunner=HTMLTestRunner(output="reportes", report_name="FacturasWS-report"),
    )