from configparser import ConfigParser
import datetime

import psycopg2
from psycopg2._psycopg import AsIs


def config(filename='', section='postgresql'):
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


def execute_insert_query(dict, schema, table, conflict_column_name):
    statement = 'insert into ' + schema + '.' + table + ' (%s) values %s  ON CONFLICT' + f'({conflict_column_name}) DO UPDATE SET '
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
    print(statement)
    cur.execute(statement, (AsIs(','.join(columns)), tuple(values)))
    conn.commit()