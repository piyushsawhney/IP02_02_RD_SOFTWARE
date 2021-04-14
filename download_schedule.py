import json
import time
import datetime

import win32com.client as win32
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import driver
from common_scenarios import LoginPage
from database import execute_select_distinct_query
from element_ids import reports_download, schedule_download
from xpaths import list_download

with open('config/selenium_config.json', "r") as json_file:
    config_json = json.load(json_file)
    URL = config_json['dop_login_url']


def perform_login():
    driver.Initialize()
    LoginPage.GoToURL(URL)
    LoginPage.Login()


def wait_for_banner_to_go():
    element = driver.Instance.find_elements_by_xpath(list_download['block_ui'])
    if len(element) > 0:
        for i in range(5):
            if not element[0].is_displayed():
                break
            time.sleep(1)


def perform_logout():
    wait_for_banner_to_go()
    LoginPage.logout()
    driver.CloseDriver()


def navigate_to_reports():
    LoginPage.navigate_to_reports()


def get_schedule_details_from_db(schedule_number):
    return execute_select_distinct_query("transaction", ["schedule_date"], {"schedule_number": schedule_number})[0]


def search_schedule(schedule_number, start_date, end_date=None):
    short_waits = WebDriverWait(driver.Instance, 10, poll_frequency=1)
    wait_for_banner_to_go()
    start_date_element = short_waits.until(EC.visibility_of_element_located((By.ID, (reports_download['start_date']))))
    start_date_element.clear()
    start_date_element.send_keys(start_date)
    if end_date:
        end_date_element = short_waits.until(EC.visibility_of_element_located((By.ID, reports_download['end_date'])))
        end_date_element.clear()
        end_date_element.send_keys(start_date)
    schedule_number_element = short_waits.until(
        EC.visibility_of_element_located((By.ID, reports_download['schedule_number'])))
    schedule_number_element.clear()
    schedule_number_element.send_keys(schedule_number)
    element = short_waits.until(EC.element_to_be_clickable((By.ID, reports_download['search_button'])))
    element.click()


def download_excel():
    short_waits = WebDriverWait(driver.Instance, 10, poll_frequency=1)
    element = short_waits.until(EC.element_to_be_clickable((By.XPATH, list_download['output_format'])))
    element.click()
    element = short_waits.until(EC.element_to_be_clickable((By.ID, schedule_download['download_file'])))
    driver.Instance.execute_script("arguments[0].click();", element)


if __name__ == '__main__':
    schedule_list = []
    today_date = datetime.date.today()
    date = datetime.date(today_date.year, today_date.month, 1).strftime("%d-%b-%Y")
    perform_login()
    navigate_to_reports()
    for schedule_number in schedule_list:
        search_schedule(schedule_number, "01-Mar-2021")
        download_excel()
    perform_logout()
