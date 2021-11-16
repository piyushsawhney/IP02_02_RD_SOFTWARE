import datetime
import json

from openpyxl import load_workbook

from processor.app_config.db_sql import UPDATE_ACCOUNT_TRANSACTIONS
from processor.db.database import execute_statement


class TransactionEntry:
    @staticmethod
    def read_from_file(date):
        with open('configuration/configuration.json', "r") as json_file:
            config_json = json.load(json_file)
            file_name = config_json['file_name']
        wb = load_workbook(file_name)
        ws = wb['Sheet1']
        for row in ws.iter_rows(min_row=2):
            values = (row[0].value, str(date), int(row[4].value), bool(row[5].value), int(row[2].value),)
            TransactionEntry.update_to_db(values)

    @staticmethod
    def update_to_db(values):
        execute_statement(UPDATE_ACCOUNT_TRANSACTIONS, values)


if __name__ == '__main__':
    today_date = datetime.date.today()
    if today_date.day <= 15:
        date = datetime.date(today_date.year, today_date.month, 1)
    else:
        date = datetime.date(today_date.year, today_date.month, 16)
    TransactionEntry.read_from_file(date)
