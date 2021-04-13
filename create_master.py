import json
from datetime import datetime

import database
import driver
import element_ids as IDs
from common_scenarios import LoginPage
from xpaths import account_details

with open('config/selenium_config.json', "r") as json_file:
    config_json = json.load(json_file)
    URL = config_json['dop_login_url']
with open('config/db_config.json', "r") as json_file:
    config_json = json.load(json_file)
    table = config_json['master_table_name']


def update_to_db(my_dict):
    database.execute_upsert_query(my_dict, table, "account_no")


def perform_login():
    driver.Initialize()
    LoginPage.GoToURL(URL)
    LoginPage.Login()


def perform_logout():
    LoginPage.logout()
    driver.CloseDriver()


def navigate_to_account():
    LoginPage.navigate_to_accounts()


def create_row(driver):
    my_dict = {}
    my_dict['account_no'] = driver.Instance.find_element_by_id(IDs.account_details['account_no']).text
    my_dict['account_no'] = my_dict['account_no'].strip()
    my_dict['investor_name'] = driver.Instance.find_element_by_id(IDs.account_details['account_name']).text
    my_dict['account_opening_date'] = driver.Instance.find_element_by_id(
        IDs.account_details['account_opening_date']).text
    my_dict['account_opening_date'] = my_dict['account_opening_date'].strip()
    my_dict['denomination'] = driver.Instance.find_element_by_id(IDs.account_details['denomination']).text
    my_dict['total_deposit_amount'] = driver.Instance.find_element_by_id(
        IDs.account_details['total_deposit_amount']).text
    my_dict['total_months_paid'] = driver.Instance.find_element_by_id(
        IDs.account_details['month_paid_upto']).text
    my_dict['next_installment_date'] = driver.Instance.find_element_by_id(
        IDs.account_details['next_installment_date']).text
    my_dict['last_deposit_date'] = driver.Instance.find_element_by_id(
        IDs.account_details['last_date_of_deposit']).text
    my_dict['rebate_paid'] = driver.Instance.find_element_by_id(IDs.account_details['rebate']).text
    my_dict['default_fee'] = driver.Instance.find_element_by_id(IDs.account_details['default_fee']).text
    my_dict['default_installments'] = driver.Instance.find_element_by_id(
        IDs.account_details['default_installments']).text
    my_dict['pending_installments'] = driver.Instance.find_element_by_id(
        IDs.account_details['pending_installment']).text

    my_dict['account_opening_date'] = datetime.strptime(my_dict['account_opening_date'], '%d-%b-%Y').date()
    my_dict['next_installment_date'] = datetime.strptime(my_dict['next_installment_date'], '%d-%b-%Y').date() if \
        my_dict['next_installment_date'] is not None and my_dict['next_installment_date'].strip() else None
    my_dict['last_deposit_date'] = datetime.strptime(my_dict['last_deposit_date'], '%d-%b-%Y').date()

    denomination = my_dict['denomination'].replace(',', '').strip()
    my_dict['denomination'] = float(denomination)

    total_deposit_amount = my_dict['total_deposit_amount'].replace(',', '').strip()
    my_dict['total_deposit_amount'] = float(total_deposit_amount)

    rebate_paid = my_dict['rebate_paid'].replace(',', '').strip()
    my_dict['rebate_paid'] = float(rebate_paid)

    default_fee = my_dict['default_fee'].replace(',', '').strip()
    my_dict['default_fee'] = float(default_fee)

    my_dict['total_months_paid'] = int(my_dict['total_months_paid'])
    my_dict['default_installments'] = int(my_dict['default_installments'])
    my_dict['pending_installments'] = int(my_dict['pending_installments'])
    return my_dict


def get_account_details():
    start = 0
    counter = 0
    while True:
        rows = driver.Instance.find_elements_by_xpath(account_details['table_rows'])
        for i in range(start, (counter + len(rows) - 3)):
            id_of_account = IDs.account_details['account_no_summary'] + "[" + str(i) + "]"

            driver.Instance.find_element_by_id(id_of_account).click()
            update_to_db(create_row(driver))
            driver.Instance.find_element_by_id(IDs.navigation_elements['back_button']).click()
            start = start + 1
        counter = start
        next_button = driver.Instance.find_element_by_id(IDs.navigation_elements['page_next'])
        if next_button.is_enabled():
            next_button.click()
        else:
            break


if __name__ == '__main__':
    perform_login()
    navigate_to_account()
    get_account_details()
    perform_logout()
