from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import processor.app_config.ids as IDs
from processor.portal import driver


class PortalNavigation:
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
    def navigate_to_aslaas():
        long_waits = WebDriverWait(driver.Instance, 30, poll_frequency=5)
        short_waits = WebDriverWait(driver.Instance, 10, poll_frequency=1)
        element = short_waits.until(EC.element_to_be_clickable((By.ID, IDs.navigation_elements['accounts'])))
        element.click()
        element = long_waits.until(EC.element_to_be_clickable((By.ID, IDs.navigation_elements['aslaas_update'])))
        element.click()
        long_waits.until(EC.visibility_of_element_located((By.ID, IDs.aslaas_update['account_no'])))
