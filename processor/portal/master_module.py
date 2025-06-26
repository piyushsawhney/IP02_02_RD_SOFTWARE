from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from processor.app_config import ids as IDs
from processor.app_config import xpaths as XPATH
from processor.app_config.db_sql import UPSERT_RD_MASTER
from processor.db.database import execute_statement
from processor.portal import driver


class RdMaster:
    @staticmethod
    def update_account_details():
        values = ()
        long_waits = WebDriverWait(driver.Instance, 30, poll_frequency=5)
        element = long_waits.until(EC.element_to_be_clickable((By.ID, IDs.account_details['account_no'])))
        values += (driver.Instance.find_element_by_id(IDs.account_details['account_no']).text.strip(),)
        values += (driver.Instance.find_element_by_id(IDs.account_details['account_name']).text.strip(),)
        values += (str(
            datetime.strptime(
                driver.Instance.find_element_by_id(IDs.account_details['account_opening_date']).text.strip(),
                '%d-%b-%Y').date()),)
        values += (float(
            driver.Instance.find_element_by_id(IDs.account_details['denomination']).text.replace(',', '').strip()),)
        values += (float(
            driver.Instance.find_element_by_id(IDs.account_details['total_deposit_amount']).text.replace(',',
                                                                                                         '').strip()),)
        values += (int(
            driver.Instance.find_element_by_id(IDs.account_details['month_paid_upto']).text.strip()),)
        next_installment_date = driver.Instance.find_element_by_id(
            IDs.account_details['next_installment_date']).text.strip()
        if next_installment_date is not None and next_installment_date != '':
            values += (str(
                datetime.strptime(
                    driver.Instance.find_element_by_id(IDs.account_details['next_installment_date']).text.strip(),
                    '%d-%b-%Y').date()),)
        else:
            values += (None,)

        values += (str(
            datetime.strptime(
                driver.Instance.find_element_by_id(IDs.account_details['last_date_of_deposit']).text.strip(),
                '%d-%b-%Y').date()),)
        values += (
            float(driver.Instance.find_element_by_id(IDs.account_details['rebate']).text.replace(',', '').strip()),)
        values += (
            float(
                driver.Instance.find_element_by_id(IDs.account_details['default_fee']).text.replace(',', '').strip()),)
        values += (
            float(driver.Instance.find_element_by_id(IDs.account_details['default_installments']).text.strip()),)
        values += (
            float(driver.Instance.find_element_by_id(IDs.account_details['pending_installment']).text.strip()),)
        values += values[1:] + values[0:1]
        print(values)
        execute_statement(UPSERT_RD_MASTER, values)

    @staticmethod
    def process_accounts():
        long_waits = WebDriverWait(driver.Instance, 60, poll_frequency=5)
        start = 0
        counter = 0
        while True:
            rows = driver.Instance.find_elements_by_xpath(XPATH.account_details['table_rows'])
            for i in range(start, (counter + len(rows) - 3)):
                id_of_account = IDs.account_details['account_no_summary'] + "[" + str(i) + "]"
                element = long_waits.until(EC.element_to_be_clickable((By.ID, id_of_account)))
                # driver.Instance.find_element_by_id(id_of_account).click()
                element.click()
                RdMaster.update_account_details()
                driver.Instance.find_element_by_id(IDs.navigation_elements['back_button']).click()
                start = start + 1
            counter = start
            next_button = long_waits.until(EC.visibility_of_element_located((By.ID, IDs.navigation_elements['page_next'])))
            if next_button.is_enabled():
                next_button.click()
            else:
                break
