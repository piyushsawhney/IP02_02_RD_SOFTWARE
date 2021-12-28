import datetime
import operator

from processor.app_config.db_sql import GET_CASH_SCHEDULE_LIST, GET_CHEQUE_SCHEDULE_LIST, \
    GET_CASH_ACCOUNT_TRANSACTION_INFO, \
    GET_CHEQUE_ACCOUNT_TRANSACTION_INFO, GET_CASH_ACCOUNT_TRANSACTION_DETAILS, GET_CHEQUE_ACCOUNT_TRANSACTION_DETAILS, \
    UPDATE_ACCOUNT_TRANSACTIONS
from processor.db.database import execute_select_query, execute_statement
from processor.portal.card_module import AslaasProcessor
from processor.portal.create_schedule_module import RdSchedules
from processor.portal.login_module import LoginPage
from processor.portal.navigation_module import PortalNavigation


class ScheduleProcessor:
    @staticmethod
    def get_schedule_list(is_cash, rd_date):
        if is_cash:
            return execute_select_query(GET_CASH_SCHEDULE_LIST, (rd_date,))
        else:
            return execute_select_query(GET_CHEQUE_SCHEDULE_LIST, (rd_date,))

    @staticmethod
    def get_transaction_info(is_cash, rd_date, schedule_group):
        if is_cash:
            return execute_select_query(GET_CASH_ACCOUNT_TRANSACTION_INFO, (rd_date, schedule_group))
        else:
            return execute_select_query(GET_CHEQUE_ACCOUNT_TRANSACTION_INFO, (rd_date, schedule_group))

    @staticmethod
    def get_schedule_details(is_cash, rd_date, schedule_group):
        if is_cash:
            return execute_select_query(GET_CASH_ACCOUNT_TRANSACTION_DETAILS, (rd_date, schedule_group))
        else:
            return execute_select_query(GET_CHEQUE_ACCOUNT_TRANSACTION_DETAILS, (rd_date, schedule_group))

    @staticmethod
    def update_db_after_completion(schedule_date, schedule_number, account_no, rd_date, is_cash, schedule_group,
                                   number_of_instalments):
        execute_statement(UPDATE_ACCOUNT_TRANSACTIONS, (
            schedule_date, schedule_number, account_no, rd_date, is_cash, schedule_group, number_of_instalments,))


def process_schedule_creation(today_date, rd_date, is_cash):
    logged_in = False
    for schedule_group in ScheduleProcessor.get_schedule_list(is_cash, rd_date):
        if not logged_in:
            LoginPage.Login()
            AslaasProcessor.process_aslaas_numbers()
            PortalNavigation.navigate_to_accounts()
            logged_in = True
        transaction_list = ScheduleProcessor.get_transaction_info(is_cash, str(rd_date), schedule_group[0])
        RdSchedules.fetch_accounts(transaction_list, is_cash)
        RdSchedules.select_accounts(transaction_list)
        RdSchedules.update_account(transaction_list, is_cash, schedule_group[0])
        schedule_number = RdSchedules.submit_schedule()
        for transaction in transaction_list:
            ScheduleProcessor.update_db_after_completion(str(today_date), schedule_number, str(rd_date), transaction[0],
                                                         is_cash, schedule_group[0], transaction[1])
    if logged_in:
        LoginPage.logout()


if __name__ == '__main__':
    choice = input("Enter Choice \n1. Only Cash\n2. Only Cheque\n3. Both Cash and Cheque\n")
    today_date = datetime.date.today()
    if today_date.day <= 15:
        if choice == '1' or choice == '3':
            process_schedule_creation(today_date, datetime.date(today_date.year, today_date.month, 1), True)
        if choice == '2' or choice == '3':
            process_schedule_creation(today_date, datetime.date(today_date.year, today_date.month, 1), False)
    else:
        if choice == '1' or choice == '3':
            process_schedule_creation(today_date, datetime.date(today_date.year, today_date.month, 16), True)
        if choice == '2' or choice == '3':
            process_schedule_creation(today_date, datetime.date(today_date.year, today_date.month, 16), False)
