schedule_xpath = {}

schedule_xpath['cash'] = f"//input[@title='Cash' and @id='CustomAgentRDAccountFG.PAY_MODE_SELECTED_FOR_TRN']"
schedule_xpath['cheque'] = f"//input[@title='DOP Cheque' and @id='CustomAgentRDAccountFG.PAY_MODE_SELECTED_FOR_TRN']"

account_details = {}
account_details['table_rows'] = "//table[@id='SummaryList']/tbody/tr"
account_details['listing_table_rows'] = "//table[@id='CustomAgentRDAccountFG.RD_ACCOUNT_NUMBER_FOR_PAYMENT']/tbody/tr"
account_details['radio_button'] = "//input[@id='CustomAgentRDAccountFG.SELECTED_INDEX' and @value='{value}']"
