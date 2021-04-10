import datetime
import json

import driver
from common_scenarios import LoginPage
from database import execute_select_query
from upload_schedules import select_account_and_add_to_schedule

with open('config/db_config.json', "r") as json_file:
    config_json = json.load(json_file)
    SCHEMA = config_json['schema']

CASH_SCHEDULE = f"select count(DISTINCT schedule_group) from {SCHEMA}.rd_account_transactions where rd_date = '(day)-(month-(year)' and is_cash = True"
CHEQUE_SCHEDULE = f"select count(DISTINCT schedule_group) from {SCHEMA}.rd_account_transactions where rd_date = '(day)-(month-(year)' and is_cash = False"

CASH_SCHEDULE_DETAILS = "select " \
                        "t.account_no," \
                        "t.investor_name," \
                        "t.no_of_installments," \
                        "t.rd_date," \
                        "case " \
                        "when m.is_extended = true then m.new_card_number else card_number end as card_number" \
                        " from " \
                        f"{SCHEMA}.rd_account_transactions t, {SCHEMA}.rd_master m " \
                        "where t.account_no = m.account_no and " \
                        "t.schedule_group = (scheduleGroup) and " \
                        "t.is_cash = True and t.schedule_number IS NULL;"

CHEQUE_SCHEDULE_DETAILS = "select " \
                          "t.account_no," \
                          "t.investor_name," \
                          "t.no_of_installments," \
                          "t.rd_date," \
                          "case " \
                          "when m.is_extended = true then m.new_card_number else card_number end as card_number," \
                          "t.cheque_number," \
                          "t.bank_account_no" \
                          " from " \
                          f"{SCHEMA}.rd_account_transactions t, {SCHEMA}.rd_master m " \
                          "where t.account_no = m.account_no and " \
                          "t.schedule_group = (scheduleGroup) and " \
                          "t.is_cash = False and t.schedule_number IS NULL;"


def create_account_dictionary(schedule_transactions, schedule):
    schedule_transactions[schedule[0]] = {}
    schedule_transactions[schedule[0]]['no_of_installment'] = schedule[2]
    schedule_transactions[schedule[0]]['card_number'] = schedule[4]
    if len(schedule) == 7:
        schedule_transactions[schedule[0]]['cheque_no'] = schedule[5]
        schedule_transactions[schedule[0]]['cheque_acc_no'] = schedule[6]
    return schedule_transactions


def create_cash_schedules(day, month, year):
    statement = CASH_SCHEDULE.replace("(day)-(month-(year)", f"{day}-{month}-{year}")
    total_schedules = execute_select_query(statement)[0][0]
    for i in range(1, total_schedules + 1):
        statement = CASH_SCHEDULE_DETAILS.replace("(scheduleGroup)", f"{i}")
        accounts_in_schedule = execute_select_query(statement)
        schedule_transactions = {}
        for schedule in accounts_in_schedule:
            schedule_transactions = create_account_dictionary(schedule_transactions, schedule)
        select_account_and_add_to_schedule(schedule_transactions, "cash")


def create_cheque_schedules(day, month, year):
    statement = CHEQUE_SCHEDULE.replace("(day)-(month-(year)", f"{day}-{month}-{year}")
    total_schedules = execute_select_query(statement)[0][0]
    print(total_schedules)
    for i in range(1, total_schedules + 1):
        statement = CHEQUE_SCHEDULE_DETAILS.replace("(scheduleGroup)", f"{i}")
        accounts_in_schedule = execute_select_query(statement)
        schedule_transactions = {}
        for schedule in accounts_in_schedule:
            schedule_transactions = create_account_dictionary(schedule_transactions, schedule)
        select_account_and_add_to_schedule(schedule_transactions, "cheque")


def perform_logout():
    if driver.Instance:
        LoginPage.logout()
        driver.CloseDriver()


if __name__ == '__main__':
    today_date = datetime.date.today()
    if today_date.day <= 15:
        create_cash_schedules(1, today_date.month, today_date.year)
        # create_cheque_schedules(1, today_date.month, today_date.year)
    else:
        create_cash_schedules(16, today_date.month, today_date.year)
        # create_cheque_schedules(16, today_date.month, today_date.year)
    # perform_logout()
