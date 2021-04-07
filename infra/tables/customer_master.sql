do $$ declare
schema_name_variable constant varchar := 'test';
client_table_variable constant varchar := 'rd_master';
begin
execute format(
'CREATE TABLE IF NOT EXISTS %I.%I(
   account_no varchar(12) PRIMARY KEY,
   investor_name varchar,
   account_opening_date date,
   denomination numeric,
   total_deposit_amount numeric,
   total_months_paid smallint,
   next_installment_date date,
   last_deposit_date date,
   rebate_paid numeric,
   default_fee numeric,
   default_installments smallint,
   pending_installments smallint,
   card_number varchar(9),
   new_card_number varchar(9),
   is_extended boolean
)',
  schema_name_variable, client_table_variable
);
end $$ language plpgsql;