import datetime
import json

import driver
from common_scenarios import LoginPage
from database import execute_select_query, update_query
from upload_schedules import select_account_and_add_to_schedule

with open('config/db_config.json', "r") as json_file:
    config_json = json.load(json_file)
    SCHEMA = config_json['schema']

CASH_SCHEDULE = f"select DISTINCT schedule_group from {SCHEMA}.rd_account_transactions where rd_date = '(date)' and is_cash = True and schedule_number is NULL and schedule_group is NOT NULL;"
CHEQUE_SCHEDULE = f"select DISTINCT schedule_group from {SCHEMA}.rd_account_transactions where rd_date = '(date)' and is_cash = False and schedule_number is NULL and schedule_group is NOT NULL;"

CASH_SCHEDULE_DETAILS = "select " \
                        "t.account_no," \
                        "m.investor_name," \
                        "t.no_of_installments," \
                        "t.rd_date," \
                        "case " \
                        "when m.is_extended = true then m.new_card_number else card_number end as card_number" \
                        " from " \
                        f"{SCHEMA}.rd_account_transactions t, {SCHEMA}.rd_master m " \
                        "where t.account_no = m.account_no and " \
                        "t.schedule_group = (scheduleGroup) and " \
                        "t.is_cash = True and t.schedule_number IS NULL " \
                        "ORDER BY t.account_no;"

CHEQUE_SCHEDULE_DETAILS = "select " \
                          "t.account_no," \
                          "m.investor_name," \
                          "t.no_of_installments," \
                          "t.rd_date," \
                          "case " \
                          "when m.is_extended = true then m.new_card_number else card_number end as card_number," \
                          "t.cheque_number," \
                          "m.bank_account_no" \
                          " from " \
                          f"{SCHEMA}.rd_account_transactions t, {SCHEMA}.rd_master m " \
                          "where t.account_no = m.account_no and " \
                          "t.schedule_group = (scheduleGroup) and " \
                          "t.is_cash = False and t.schedule_number IS NULL " \
                          "ORDER BY t.cheque_number;"


def create_account_dictionary(schedule_transactions, schedule):
    schedule_transactions[schedule[0]] = {}
    schedule_transactions[schedule[0]]['no_of_installment'] = schedule[2]
    schedule_transactions[schedule[0]]['card_number'] = schedule[4]
    if len(schedule) == 7:
        schedule_transactions[schedule[0]]['cheque_no'] = schedule[5]
        schedule_transactions[schedule[0]]['cheque_acc_no'] = schedule[6]
    return schedule_transactions


def create_cash_schedules(date):
    statement = CASH_SCHEDULE.replace("(date)", str(date))
    total_schedules = execute_select_query(statement)
    output = [item for t in total_schedules for item in t]
    output.sort()
    for i in output:
        statement = CASH_SCHEDULE_DETAILS.replace("(scheduleGroup)", f"{i}")
        accounts_in_schedule = execute_select_query(statement)
        schedule_transactions = {}
        for schedule in accounts_in_schedule:
            schedule_transactions = create_account_dictionary(schedule_transactions, schedule)
        schedule_reference = select_account_and_add_to_schedule(schedule_transactions, "cash")
        schedule_reference_dict = {"schedule_number": schedule_reference, "schedule_date": str(datetime.date.today())}
        for schedule in accounts_in_schedule:
            update_query("transaction", schedule_reference_dict, {"account_no": schedule[0]})


def create_cheque_schedules(date):
    statement = CHEQUE_SCHEDULE.replace("(date)", str(date))
    total_schedules = execute_select_query(statement)
    output = [item for t in total_schedules for item in t]
    output.sort()
    for i in output:
        statement = CHEQUE_SCHEDULE_DETAILS.replace("(scheduleGroup)", f"{i}")
        accounts_in_schedule = execute_select_query(statement)
        schedule_transactions = {}
        for schedule in accounts_in_schedule:
            schedule_transactions = create_account_dictionary(schedule_transactions, schedule)
        schedule_reference = select_account_and_add_to_schedule(schedule_transactions, "cheque")
        schedule_reference_dict = {"schedule_number": schedule_reference, "schedule_date": str(datetime.date.today())}
        for schedule in accounts_in_schedule:
            update_query("transaction", schedule_reference_dict, {"account_no": schedule[0]})


def perform_logout():
    if driver.Instance:
        LoginPage.logout()
        driver.CloseDriver()


if __name__ == '__main__':
    today_date = datetime.date.today()
    choice = input("Enter Choice \n1. Only Cash\n2. Only Cheque\n3. Both Cash and Cheque\n")
    if today_date.day <= 15:
        date = datetime.date(today_date.year, today_date.month, 1)
        if choice == '1' or choice == '3':
            create_cash_schedules(date)
        if choice == '2' or choice == '3':
            create_cheque_schedules(date)
    else:
        date = datetime.date(today_date.year, today_date.month, 16)
        if choice == '1' or choice == '3':
            create_cash_schedules(date)
        if choice == '2' or choice == '3':
            create_cheque_schedules(date)
    perform_logout()
