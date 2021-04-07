do $$ declare
schema_name_variable constant varchar := 'test';
client_table_variable constant varchar := 'rd_account_transactions';
begin
Drop TYPE deposit_type;
create TYPE deposit_type as enum (
  'CHEQUE', 'CASH'
);
DROP DOMAIN cheque_numbers;
CREATE DOMAIN cheque_numbers AS INTEGER CHECK (
   VALUE > 0 AND VALUE <= 999999
);
execute format(
'CREATE TABLE IF NOT EXISTS %I.%I(
   rd_date date CONSTRAINT check_date CHECK((EXTRACT(DAY from rd_date) = 1) or EXTRACT(DAY from rd_date) = 16) ,
   account_no varchar(12),
   investor_name varchar,
   deposit_type deposit_type,
   receive_date date,
   deposit_amount numeric,
   cheque_number cheque_numbers,
   bank_name varchar,
   bank_account_no varchar,
   no_of_installments smallint,
   rebate numeric,
   default_fee numeric,
   schedule_date date,
   schedule_number varchar(10),
   PRIMARY KEY (rd_date, account_no),
   CONSTRAINT fk_account_no
      FOREIGN KEY(account_no)
	  REFERENCES rd_master(account_no)
)',
  schema_name_variable, client_table_variable
);
end $$ language plpgsql;