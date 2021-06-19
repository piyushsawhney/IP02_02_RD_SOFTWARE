import datetime
import json
from configparser import ConfigParser

import psycopg2
from psycopg2._psycopg import AsIs

with open('config/db_config.json', "r") as json_file:
    config_json = json.load(json_file)
    SCHEMA = config_json['schema']


def config(filename='config/desktop.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


try:
    # read connection parameters
    params = config()
    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)


def execute_select_query(query):
    cur.execute(query)
    return cur.fetchall()


def execute_select_distinct_query(table_type, attribute_list, condition=None):
    attributes = ','.join(attribute_list)
    if condition:
        condition_str = ','.join("{!s}={!r}".format(k, v) for (k, v) in condition.items())
    statement = f"select DISTINCT {attributes} from {SCHEMA}.{config_json[table_type]}" + (
        f" where {condition_str}" if condition is not None else "") + ";"
    cur.execute(statement)
    return cur.fetchall()


def update_query(table_type, update_dict, condition=None):
    statement = "update " + SCHEMA + "." + config_json[table_type] + f" set "
    update_values_str = ','.join("{!s}={!r}".format(k, v) for (k, v) in update_dict.items())
    statement = statement + update_values_str
    if condition:
        statement = statement + " where " + condition + " ;"
    cur.execute(statement)
    conn.commit()


def execute_upsert_query(dict, table, conflict_column_name):
    statement = 'insert into ' + SCHEMA + '.' + table + ' (%s) values %s  ON CONFLICT' + f'({conflict_column_name}) DO UPDATE SET '
    columns = dict.keys()
    values = [dict[column] for column in columns]
    for column in columns:
        if dict[column] is None:
            pass
        elif column.lower() == conflict_column_name:
            pass
        elif isinstance(dict[column], datetime.date) or isinstance(dict[column], str):
            statement = statement + f"{column}='{dict[column]}',"
        else:
            statement = statement + f"{column}={dict[column]},"
    statement = statement[:-1] + ";"
    cur.execute(statement, (AsIs(','.join(columns)), tuple(values)))
    conn.commit()


def update_null(table_type, column_list, condition):
    statement = "update " + SCHEMA + "." + config_json[table_type] + f" set "
    for column in column_list:
        statement = statement + column + "=NULL,"
    statement = statement[:-1]
    if condition:
        condition_str = ','.join("{!s}={!r}".format(k, v) for (k, v) in condition.items())
        statement = statement + " where " + condition_str
    statement = statement + ";"
    cur.execute(statement)
    conn.commit()


def  execute_insert_query(table_type, insert_dict):
    statement = 'insert into ' + SCHEMA + '.' + config_json[table_type] + ' (%s) values %s  ON CONFLICT DO NOTHING;'
    columns = insert_dict.keys()
    values = [insert_dict[column] for column in columns]
    cur.execute(statement, (AsIs(','.join(columns)), tuple(values)))
    # print(cur.mogrify(statement, (AsIs(','.join(columns)), tuple(values))))
    conn.commit()
