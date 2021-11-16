GET_CASH_SCHEDULE_LIST = "select DISTINCT schedule_group from po_data.rd_account_transactions " \
                         "where rd_date=%s and is_cash=True and schedule_number is NULL and schedule_group is NOT NULL " \
                         "ORDER BY schedule_group;"

GET_CASH_ACCOUNT_TRANSACTION_INFO = "select t.account_no,t.no_of_installments,t.rd_date  " \
                                    "from po_data.rd_account_transactions t " \
                                    "where t.rd_date=%s and t.schedule_group=%s and " \
                                    "t.is_cash=True and t.schedule_number IS NULL ORDER BY t.account_no;"

GET_CASH_ACCOUNT_TRANSACTION_DETAILS = "select t.account_no,m.investor_name,t.no_of_installments," \
                                       "t.no_of_installments * m.denomination as amount, t.rd_date, " \
                                       "m.total_months_paid, m.last_deposit_date,m.next_installment_date " \
                                       "from po_data.rd_account_transactions t, po_data.rd_master m " \
                                       "where t.account_no = m.account_no and t.rd_date=%s and t.schedule_group=%s " \
                                       "and t.is_cash=True and t.schedule_number IS NULL ORDER BY t.account_no;"

GET_CHEQUE_SCHEDULE_LIST = "select DISTINCT schedule_group from po_data.rd_account_transactions" \
                           " where rd_date=%s and is_cash=False and schedule_number is NULL and " \
                           "schedule_group is NOT NULL ORDER BY schedule_group;"

GET_CHEQUE_ACCOUNT_TRANSACTION_INFO = "select t.account_no,t.no_of_installments,t.rd_date, t.cheque_number, " \
                                      "m.bank_account_no from po_data.rd_account_transactions t," \
                                      "po_data.rd_master m where t.rd_date=%s and t.schedule_group=%s and " \
                                      "t.is_cash=False and t.schedule_number IS NULL and m.account_no = t.account_no" \
                                      " ORDER BY t.account_no;"

GET_CHEQUE_ACCOUNT_TRANSACTION_DETAILS = "select t.account_no,m.investor_name,t.no_of_installments, " \
                                         "t.no_of_installments * m.denomination as amount, t.rd_date,t.cheque_number," \
                                         "m.bank_account_no,m.total_months_paid, m.last_deposit_date," \
                                         "m.next_installment_date from po_data.rd_account_transactions t, " \
                                         "po_data.rd_master m where t.account_no = m.account_no and t.rd_date=%s and " \
                                         "t.schedule_group=%s and t.is_cash=False and t.schedule_number IS NULL " \
                                         "ORDER BY t.account_no;"

GET_ACCOUNT_ASLAAS = "select m.account_no, case  when (m.is_updated = false and m.is_extended = true) " \
                     "then m.new_card_number when(m.is_updated = false and m.is_extended = false) then " \
                     f"m.card_number else m.card_number end as card_number from po_data.rd_master m " \
                     "where(m.card_number is not null and m.card_number != '') limit 1;"

UPDATE_ACCOUNT_ASLAAS = "UPDATE po_data.rd_master SET is_updated=%s where account_no=%s;"

UPDATE_ACCOUNT_TRANSACTIONS = "UPDATE po_data.rd_account_transactions SET schedule_date=%s, schedule_number=%s " \
                              "WHERE rd_date=%s and account_no=%s and is_cash=%s and schedule_group=%s and " \
                              "no_of_installments=%s"

UPSERT_MASTER = "INSERT INTO po_data.rd_master " \
                "(account_no, investor_name, account_opening_date, denomination, total_deposit_amount, " \
                "total_months_paid, next_installment_date, last_deposit_date, rebate_paid, default_fee, " \
                "default_installments, pending_installments) " \
                "VALUES ('{account_no}','{investor_name}','{account_opening_date}',{denomination}," \
                "{total_deposit_amount}, {total_months_paid}, '{next_installment_date}', '{last_deposit_date}'," \
                "{rebate_paid},{default_fee},{default_installments},{pending_installments}"

UPSERT_RD_MASTER = "INSERT INTO po_data.rd_master " \
                   "(account_no, investor_name, account_opening_date, denomination, total_deposit_amount, " \
                   "total_months_paid, next_installment_date, last_deposit_date, rebate_paid, default_fee, " \
                   "default_installments, pending_installments) " \
                   "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT(account_no) DO UPDATE SET " \
                   "investor_name=%s, account_opening_date=%s, denomination=%s, total_deposit_amount=%s," \
                   "total_months_paid=%s,next_installment_date=%s,last_deposit_date=%s,rebate_paid=%s," \
                   "default_fee=%s,default_installments=%s,pending_installments=%s where rd_master.account_no = %s"

UPDATE_REBATE_DEFAULT = "UPDATE po_data.rd_account_transactions SET rebate=%s ,default_fee=%s where account_no=%s " \
                        "and rd_date=%s and is_cash=%s and schedule_group=%s ;"

GET_SCHEDULE_NUMBERS = "select distinct schedule_number from po_data.rd_account_transactions where schedule_date=%s;"
