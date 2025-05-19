import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import processor.app_config.ids as IDs
from processor.portal import driver


class LoginPage:
    @staticmethod
    def GoToURL(url):
        driver.Instance.get(url)

    @staticmethod
    def Login():
        with open('configuration/configuration.json', "r") as json_file:
            config = json.load(json_file)
            url = config['dop_login_url']
        driver.Initialize()
        driver.Instance.get(url)
        # print(os.getcwd())
        with open('configuration/credentials.json', "r") as json_file:
            config = json.load(json_file)
        username = config['username']
        password = config['password']
        driver.Instance.find_element_by_id(IDs.login_elements['username']).send_keys(username)
        driver.Instance.find_element_by_id(IDs.login_elements['password']).send_keys(password)
        long_waits = WebDriverWait(driver.Instance, 60, poll_frequency=2)
        long_waits.until(EC.element_to_be_clickable((By.ID, IDs.navigation_elements['accounts'])))

    @staticmethod
    def logout():
        driver.Instance.find_element_by_id(IDs.login_elements['HREF_Logout']).click()
        driver.Instance.find_element_by_id(IDs.login_elements['LOG_OUT']).click()
        driver.CloseDriver()
