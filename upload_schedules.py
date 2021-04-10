import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import driver
import element_ids as IDs
import xpaths as xPaths
from common_scenarios import LoginPage

with open('config/selenium_config.json', "r") as json_file:
    config_json = json.load(json_file)
    URL = config_json['dop_login_url']


def perform_login():
    driver.Initialize()
    LoginPage.GoToURL(URL)
    LoginPage.Login()


def navigate_to_account():
    LoginPage.navigate_to_accounts()


def select_account_and_add_to_schedule(schedule_details, schedule_type):
    if not driver.Instance:
        perform_login()
        navigate_to_account()
    number_of_accounts = len(schedule_details)
    account_nos = ','.join(schedule_details.keys())
    driver.Instance.find_element_by_xpath(xPaths.schedule_xpath[schedule_type]).click()
    account_no_search_element = driver.Instance.find_element_by_id(IDs.schedule_elements['search'])
    account_no_search_element.clear()
    account_no_search_element.send_keys(account_nos)
    driver.Instance.find_element_by_id(IDs.navigation_elements['fetch']).click()
    for i in range(number_of_accounts):
        element_id = IDs.schedule_elements['account_no_check_box'] + f"[{i}]"
        driver.Instance.find_element_by_id(element_id).click()
    driver.Instance.find_element_by_id(IDs.schedule_elements['save_accounts']).click()

    for i in range(number_of_accounts):
        element_id_string = IDs.schedule_update_elements['account_no'] + f"[{i}]"
        account_no = driver.Instance.find_element_by_id(element_id_string).text.strip()
        assert account_no in schedule_details.keys()
        radio_button_xpath = xPaths.account_details['radio_button'].replace("{value}", str(i))
        driver.Instance.find_element_by_xpath(radio_button_xpath).click()
        # schedule details entering
        no_of_installment_element = driver.Instance.find_element_by_id(IDs.schedule_elements['no_of_installment'])
        no_of_installment_element.clear()
        no_of_installment_element.send_keys(
            schedule_details[account_no]['no_of_installment'])
        driver.Instance.find_element_by_id(IDs.schedule_elements['rebate_default_button']).click()
        short_waits = WebDriverWait(driver.Instance, 10, poll_frequency=1)

        rebate_element = short_waits.until(EC.presence_of_element_located((By.ID, IDs.schedule_elements['rebate'])))
        default_element = short_waits.until(EC.presence_of_element_located((By.ID, IDs.schedule_elements['default'])))
        rebate = rebate_element.text.strip()
        default_fee = default_element.text.strip()
        print("Rebate ", rebate)
        print("Default ", default_fee)
        card_number_element = driver.Instance.find_element_by_id(IDs.schedule_elements['card_number_input'])
        card_number_element.clear()
        card_number_element.send_keys(
            schedule_details[account_no]['card_number'])

        if schedule_type == 'cheque':
            cheque_no_element = driver.Instance.find_element_by_id(IDs.schedule_elements['cheque_no'])
            cheque_no_element.clear()
            cheque_no_element.send_keys(
                schedule_details[account_no]['cheque_no'])
            cheque_acc_no_element = driver.Instance.find_element_by_id(IDs.schedule_elements['cheque_acc_no'])
            cheque_acc_no_element.clear()
            cheque_acc_no_element.send_keys(
                schedule_details[account_no]['cheque_acc_no'])
        driver.Instance.find_element_by_id(IDs.schedule_elements['save_modification']).click()

    for i in range(number_of_accounts):
        element_id_string = IDs.schedule_elements['modified_status'] + f"[{i}]"
        assert driver.Instance.find_element_by_id(element_id_string).text.strip().lower() == 'yes'
