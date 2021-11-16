import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import processor.app_config.ids as IDs
from processor.app_config import xpaths as XPATH
from processor.portal import driver


class RdDownloadSchedules:
    @staticmethod
    def search_schedule(schedule_number, starting_date, ending_date=None):
        start_date = starting_date.strftime("%d-%b-%Y")
        short_waits = WebDriverWait(driver.Instance, 10, poll_frequency=1)
        element = driver.Instance.find_elements_by_xpath(XPATH.list_download['block_ui'])
        if len(element) > 0:
            for i in range(5):
                if not element[0].is_displayed():
                    break
                time.sleep(1)
        start_date_element = short_waits.until(
            EC.visibility_of_element_located((By.ID, (IDs.reports_download['start_date']))))
        start_date_element.clear()
        start_date_element.send_keys(start_date)
        if ending_date:
            end_date_element = short_waits.until(
                EC.visibility_of_element_located((By.ID, IDs.reports_download['end_date'])))
            end_date_element.clear()
            end_date_element.send_keys(start_date)
        schedule_number_element = short_waits.until(
            EC.visibility_of_element_located((By.ID, IDs.reports_download['schedule_number'])))
        schedule_number_element.clear()
        schedule_number_element.send_keys(schedule_number)
        element = short_waits.until(EC.element_to_be_clickable((By.ID, IDs.reports_download['search_button'])))
        element.click()

    @staticmethod
    def download_schedule_excel():
        short_waits = WebDriverWait(driver.Instance, 10, poll_frequency=1)
        element = short_waits.until(EC.element_to_be_clickable((By.XPATH, XPATH.list_download['output_format'])))
        element.click()
        element = short_waits.until(EC.element_to_be_clickable((By.ID, IDs.schedule_download['download_file'])))
        driver.Instance.execute_script("arguments[0].click();", element)
