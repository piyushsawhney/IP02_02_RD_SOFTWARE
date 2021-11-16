from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import processor.app_config.ids as IDs
from processor.app_config.db_sql import GET_ACCOUNT_ASLAAS, UPDATE_ACCOUNT_ASLAAS
from processor.db.database import execute_select_query, execute_statement
from processor.portal import driver
from processor.portal.navigation_module import PortalNavigation


class AslaasProcessor:
    @staticmethod
    def get_non_updated_cards():
        return execute_select_query(GET_ACCOUNT_ASLAAS)

    @staticmethod
    def update_card_on_portal(account_no, card_no):
        short_waits = WebDriverWait(driver.Instance, 10, poll_frequency=1)
        driver.Instance.find_element_by_id(IDs.aslaas_update['account_no']).send_keys(
            account_no.strip())
        driver.Instance.find_element_by_id(IDs.aslaas_update['aslaas_number']).send_keys(
            card_no.strip())
        element = short_waits.until(EC.element_to_be_clickable((By.ID, IDs.aslaas_update['continue'])))
        element.click()
        element = short_waits.until(EC.element_to_be_clickable((By.ID, IDs.aslaas_update['add'])))
        element.click()

    @staticmethod
    def update_card_update_status(account_no):
        execute_statement(UPDATE_ACCOUNT_ASLAAS, (True, account_no,))

    @staticmethod
    def process_aslaas_numbers():
        account_aslaas_no_list = AslaasProcessor.get_non_updated_cards()
        if len(account_aslaas_no_list) > 0:
            PortalNavigation.navigate_to_aslaas()
            for aslaas_account_no in account_aslaas_no_list:
                AslaasProcessor.update_card_on_portal(aslaas_account_no[0], aslaas_account_no[1])
                AslaasProcessor.update_card_update_status(aslaas_account_no[0])
