import json
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import driver
import element_ids as IDs
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    @staticmethod
    def GoToURL(url):
        driver.Instance.get(url)

    @staticmethod
    def Login():
        with open('config/credentials.json', "r") as json_file:
            config = json.load(json_file)
        username = config['username']
        password = config['password']
        driver.Instance.find_element_by_id(IDs.login_elements['username']).send_keys(username)
        driver.Instance.find_element_by_id(IDs.login_elements['password']).send_keys(password)
        for i in range(10):
            # text = driver.Instance.find_element_by_id(IDs.login_elements['captcha_box']).text
            time.sleep(1)
        driver.Instance.find_element_by_id(IDs.login_elements['login']).click()

    @staticmethod
    def navigate_to_accounts():
        long_waits = WebDriverWait(driver.Instance, 30, poll_frequency=5)
        short_waits = WebDriverWait(driver.Instance, 10, poll_frequency=1)
        element = short_waits.until(EC.element_to_be_clickable((By.ID, IDs.navigation_elements['accounts'])))
        element.click()
        element = long_waits.until(EC.element_to_be_clickable((By.ID, IDs.navigation_elements['deposit_accounts'])))
        element.click()
        long_waits.until(EC.element_to_be_clickable((By.ID, IDs.navigation_elements['fetch'])))

    @staticmethod
    def navigate_to_reports():
        long_waits = WebDriverWait(driver.Instance, 30, poll_frequency=5)
        short_waits = WebDriverWait(driver.Instance, 10, poll_frequency=1)
        element = short_waits.until(EC.element_to_be_clickable((By.ID, IDs.navigation_elements['accounts'])))
        element.click()
        element = long_waits.until(EC.element_to_be_clickable((By.ID, IDs.navigation_elements['reports'])))
        element.click()
        long_waits.until(EC.visibility_of_element_located((By.ID, IDs.navigation_elements['agent_id'])))

    @staticmethod
    def logout():
        driver.Instance.find_element_by_id(IDs.login_elements['logout_1']).click()
        driver.Instance.find_element_by_id(IDs.login_elements['logout_2']).click()
