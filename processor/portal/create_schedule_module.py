import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from processor.app_config import ids as IDs
from processor.app_config import xpaths as XPATH
from processor.app_config.db_sql import UPDATE_REBATE_DEFAULT
from processor.db.database import execute_statement
from processor.portal import driver


class RdSchedules:
    @staticmethod
    def fetch_accounts(account_list, is_cash):
        type = 'cash' if is_cash else 'cheque'
        account_nos = ','.join([item[0] for item in account_list])
        driver.Instance.find_element_by_xpath(XPATH.schedule_xpath[type]).click()
        account_no_search_element = driver.Instance.find_element_by_id(IDs.schedule_elements['search'])
        account_no_search_element.clear()
        account_no_search_element.send_keys(account_nos)
        driver.Instance.find_element_by_id(IDs.navigation_elements['fetch']).click()

    @staticmethod
    def select_accounts(account_list):
        number_of_accounts = len(account_list)
        for i in range(1, number_of_accounts + 1):
            element_id = IDs.schedule_elements['account_no_check_box'] + f"[{i - 1}]"
            driver.Instance.find_element_by_id(element_id).click()
            if not i == 0 and i % 10 == 0 and number_of_accounts != 10:
                driver.Instance.find_element_by_id(IDs.navigation_elements['next_select_account']).click()

        driver.Instance.find_element_by_id(IDs.schedule_elements['save_accounts']).click()

    @staticmethod
    def update_account(account_list, is_cash, schedule_group):
        for i in range(len(account_list)):
            short_waits = WebDriverWait(driver.Instance, 45, poll_frequency=2)

            element_id_string = IDs.schedule_update_elements['account_no'] + f"[{i}]"
            account_no = short_waits.until(EC.visibility_of_element_located((By.ID, element_id_string))).text.strip()
            assert account_no == account_list[i][0]
            radio_button_xpath = XPATH.account_details['radio_button'].replace("{value}", str(i))
            driver.Instance.find_element_by_xpath(radio_button_xpath).click()
            # Rebate and Default Calculation
            no_of_installment_element = driver.Instance.find_element_by_id(IDs.schedule_elements['no_of_installment'])
            no_of_installment_element.clear()
            no_of_installment_element.send_keys(account_list[i][1])
            driver.Instance.find_element_by_id(IDs.schedule_elements['rebate_default_button']).click()
            time.sleep(1)
            rebate_element = short_waits.until(
                EC.presence_of_element_located((By.ID, IDs.schedule_elements['rebate'])))
            default_element = short_waits.until(
                EC.presence_of_element_located((By.ID, IDs.schedule_elements['default'])))
            values = (
                float(rebate_element.text.replace(",", "").strip()),
                float(default_element.text.replace(",", "").strip()),
                account_list[i][0], account_list[i][2], is_cash, schedule_group,)
            execute_statement(UPDATE_REBATE_DEFAULT, values)

            # Update cheque details
            if not is_cash:
                cheque_no_element = driver.Instance.find_element_by_id(IDs.schedule_elements['cheque_no'])
                cheque_no_element.clear()
                cheque_no_element.send_keys(account_list[i][3])
                cheque_acc_no_element = driver.Instance.find_element_by_id(IDs.schedule_elements['cheque_acc_no'])
                cheque_acc_no_element.clear()
                cheque_acc_no_element.send_keys(account_list[i][4])
            driver.Instance.find_element_by_id(IDs.schedule_elements['save_modification']).click()
            time.sleep(1)
            RdSchedules.verify_account(i, len(account_list))

    @staticmethod
    def navigate_to_page(page_number):
        short_waits = WebDriverWait(driver.Instance, 30, poll_frequency=5)
        short_waits.until(
            EC.visibility_of_element_located((By.ID, IDs.navigation_elements['add_account_page_number'])))
        driver.Instance.find_element_by_id(IDs.navigation_elements['add_account_page_number']).send_keys(
            str(page_number))
        driver.Instance.find_element_by_id(IDs.navigation_elements['add_account_go']).click()

    @staticmethod
    def verify_account(i, number_of_accounts):
        short_waits = WebDriverWait(driver.Instance, 30, poll_frequency=5)
        page_to_go = int(((i + 1) / 10) + 1)

        element_id_string = IDs.schedule_elements['modified_status'] + f"[{i}]"
        if i <= 9:
            assert short_waits.until(
                EC.visibility_of_element_located((By.ID, element_id_string))).text.strip().lower() == 'yes'
            if i == 9 and number_of_accounts != 10:
                RdSchedules.navigate_to_page(page_to_go)
        elif i % 10 == 9:
            RdSchedules.navigate_to_page(page_to_go - 1)
            assert short_waits.until(
                EC.visibility_of_element_located((By.ID, element_id_string))).text.strip().lower() == 'yes'
            RdSchedules.navigate_to_page(page_to_go)
        else:
            RdSchedules.navigate_to_page(page_to_go)
            assert short_waits.until(
                EC.visibility_of_element_located((By.ID, element_id_string))).text.strip().lower() == 'yes'

    @staticmethod
    def submit_schedule():
        short_waits = WebDriverWait(driver.Instance, 15, poll_frequency=2)
        driver.Instance.find_element_by_id(IDs.schedule_elements['pay_schedule']).click()
        ref_no_text = short_waits.until(
            EC.visibility_of_element_located((By.XPATH, XPATH.schedule_xpath['reference_no']))).text.strip()
        print(ref_no_text)
        reference_no = ref_no_text.split(".")[1]
        reference_no = reference_no[reference_no.rindex(" "):].strip()
        print(reference_no)
        return reference_no
