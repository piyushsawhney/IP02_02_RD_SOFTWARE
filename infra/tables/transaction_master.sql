do $$ declare
schema_name_variable constant varchar := 'test';
client_table_variable constant varchar := 'rd_account_transactions';
begin
execute format(
'CREATE TABLE IF NOT EXISTS %I.%I(
   rd_date date CONSTRAINT check_date CHECK((EXTRACT(DAY from rd_date) = 1) or EXTRACT(DAY from rd_date) = 16) ,
   account_no varchar(12),
   is_cash boolean,
   no_of_installments smallint,
   cheque_number varchar(6),
   loan_amount numeric,
   loan_interest numeric,
   schedule_group smallint,
   rebate numeric,
   default_fee numeric,
   schedule_date date,
   schedule_number varchar(12),
   CONSTRAINT cheque_schedule CHECK ((is_cash = False and cheque_number IS NOT NULL) OR is_cash = True),
   PRIMARY KEY (rd_date, account_no),
   CONSTRAINT fk_account_no
      FOREIGN KEY(account_no)
	  REFERENCES rd_master(account_no)
)',
  schema_name_variable, client_table_variable
);
end $$ language plpgsql;