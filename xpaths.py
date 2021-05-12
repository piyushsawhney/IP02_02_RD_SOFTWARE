schedule_xpath = {}

schedule_xpath['cash'] = f"//input[@title='Cash' and @id='CustomAgentRDAccountFG.PAY_MODE_SELECTED_FOR_TRN']"
schedule_xpath['cheque'] = f"//input[@title='DOP Cheque' and @id='CustomAgentRDAccountFG.PAY_MODE_SELECTED_FOR_TRN']"
schedule_xpath['reference_no'] = f"//div[@id='MessageDisplay_TABLE']//div[@class='greenbg' and @role='alert']"
# schedule_xpath['reference_no'] = f"//div[@id='MessageDisplay_TABLE']//div[1]"

account_details = {}
account_details['table_rows'] = "//table[@id='SummaryList']/tbody/tr"
account_details['listing_table_rows'] = "//table[@id='CustomAgentRDAccountFG.RD_ACCOUNT_NUMBER_FOR_PAYMENT']/tbody/tr"
account_details['radio_button'] = "//input[@id='CustomAgentRDAccountFG.SELECTED_INDEX' and @value='{value}']"

list_download = {}
list_download[
    'output_format'] = "//select[@id='CustomAgentRDAccountFG.OUTFORMAT']/option[@value='4' or text()='XLS file']"
list_download['block_ui'] = "//div[@class='blockUI blockOverlay']"
