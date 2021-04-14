import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import driver
import element_ids as IDs
import xpaths
from common_scenarios import LoginPage
from database import update_query

with open('config/selenium_config.json', "r") as json_file:
    config_json = json.load(json_file)
    URL = config_json['dop_login_url']


def perform_login():
    driver.Initialize()
    LoginPage.GoToURL(URL)
    LoginPage.Login()


def navigate_to_account():
    LoginPage.navigate_to_accounts()


def fetch_accounts(account_nos, type):
    driver.Instance.find_element_by_xpath(xpaths.schedule_xpath[type]).click()
    account_no_search_element = driver.Instance.find_element_by_id(IDs.schedule_elements['search'])
    account_no_search_element.clear()
    account_no_search_element.send_keys(account_nos)
    driver.Instance.find_element_by_id(IDs.navigation_elements['fetch']).click()


def select_accounts(number_of_accounts):
    for i in range(1, number_of_accounts + 1):
        element_id = IDs.schedule_elements['account_no_check_box'] + f"[{i - 1}]"
        driver.Instance.find_element_by_id(element_id).click()
        if not i == 0 and i % 10 == 0:
            driver.Instance.find_element_by_id(IDs.navigation_elements['next_select_account']).click()

    driver.Instance.find_element_by_id(IDs.schedule_elements['save_accounts']).click()


def get_and_update_rebate_and_default_fee(account_no, number_of_installments):
    short_waits = WebDriverWait(driver.Instance, 10, poll_frequency=1)
    no_of_installment_element = driver.Instance.find_element_by_id(IDs.schedule_elements['no_of_installment'])
    no_of_installment_element.clear()
    no_of_installment_element.send_keys(number_of_installments)
    driver.Instance.find_element_by_id(IDs.schedule_elements['rebate_default_button']).click()
    rebate_element = short_waits.until(EC.presence_of_element_located((By.ID, IDs.schedule_elements['rebate'])))
    default_element = short_waits.until(EC.presence_of_element_located((By.ID, IDs.schedule_elements['default'])))
    rebate_default_dict = {'rebate': rebate_element.text.strip(), 'default_fee': default_element.text.strip()}
    account_no_dict = {'account_no': account_no}
    update_query("transaction", rebate_default_dict, account_no_dict)


def add_details_for_transaction(card_number, type, cheque_no=None, bank_account_no=None):
    card_number_element = driver.Instance.find_element_by_id(IDs.schedule_elements['card_number_input'])
    card_number_element.clear()
    card_number_element.send_keys(card_number)

    if type == 'cheque':
        cheque_no_element = driver.Instance.find_element_by_id(IDs.schedule_elements['cheque_no'])
        cheque_no_element.clear()
        cheque_no_element.send_keys(cheque_no)
        cheque_acc_no_element = driver.Instance.find_element_by_id(IDs.schedule_elements['cheque_acc_no'])
        cheque_acc_no_element.clear()
        cheque_acc_no_element.send_keys(bank_account_no)


def navigate_to_page(page_number):
    driver.Instance.find_element_by_id(IDs.navigation_elements['add_account_page_number']).send_keys(
        str(page_number))
    driver.Instance.find_element_by_id(IDs.navigation_elements['add_account_go']).click()


def submit_schedule():
    driver.Instance.find_element_by_id(IDs.schedule_elements['pay_schedule']).click()
    ref_no_text = driver.Instance.find_element_by_xpath(xpaths.schedule_xpath['reference_no']).text.strip()
    print(ref_no_text)
    reference_no = ref_no_text.split(".")[1]
    reference_no = reference_no[reference_no.rindex(" "):].strip()
    print(reference_no)
    return reference_no


def select_account_and_add_to_schedule(schedule_details, schedule_type):
    if not driver.Instance:
        perform_login()
        navigate_to_account()
    number_of_accounts = len(schedule_details)
    account_nos = ','.join(schedule_details.keys())

    fetch_accounts(account_nos, schedule_type)

    select_accounts(number_of_accounts)

    for i in range(number_of_accounts):

        short_waits = WebDriverWait(driver.Instance, 10, poll_frequency=1)

        element_id_string = IDs.schedule_update_elements['account_no'] + f"[{i}]"
        account_no = short_waits.until(EC.presence_of_element_located((By.ID, element_id_string))).text.strip()
        assert account_no in schedule_details.keys()
        radio_button_xpath = xpaths.account_details['radio_button'].replace("{value}", str(i))
        driver.Instance.find_element_by_xpath(radio_button_xpath).click()

        get_and_update_rebate_and_default_fee(account_no, schedule_details[account_no]['no_of_installment'])

        add_details_for_transaction(schedule_details[account_no]['card_number'], schedule_type,
                                    schedule_details[account_no]['cheque_no'],
                                    schedule_details[account_no]['cheque_acc_no'])

        driver.Instance.find_element_by_id(IDs.schedule_elements['save_modification']).click()

        page_to_go = int(((i + 1) / 10) + 1)
        if i <= 9:
            element_id_string = IDs.schedule_elements['modified_status'] + f"[{i}]"
            assert driver.Instance.find_element_by_id(element_id_string).text.strip().lower() == 'yes'
            if i == 9:
                navigate_to_page(page_to_go)
        else:
            navigate_to_page(page_to_go)
            element_id_string = IDs.schedule_elements['modified_status'] + f"[{i}]"
            assert driver.Instance.find_element_by_id(element_id_string).text.strip().lower() == 'yes'

        # if i == 9:
        #
        #     driver.Instance.find_element_by_id(IDs.navigation_elements['add_account_page_number']).send_keys(
        #         str(page_to_go))
        #     # short_waits.until(EC.element_to_be_clickable((By.ID, IDs.navigation_elements['add_account_go']))).click()
        #     driver.Instance.find_element_by_id(IDs.navigation_elements['add_account_go']).click()
        # elif i > 9:
        #     driver.Instance.find_element_by_id(IDs.navigation_elements['add_account_page_number']).send_keys(
        #         str(page_to_go))
        #     # short_waits.until(EC.element_to_be_clickable((By.ID, IDs.navigation_elements['add_account_go']))).click()
        #     driver.Instance.find_element_by_id(IDs.navigation_elements['add_account_go']).click()
        #
        # else:
        #     element_id_string = IDs.schedule_elements['modified_status'] + f"[{i}]"
        #     assert driver.Instance.find_element_by_id(element_id_string).text.strip().lower() == 'yes'

    input("Do You want to continue")
    # reference_no = submit_schedule()
    reference_no = input("Enter Reference Number : ")
    return reference_no
