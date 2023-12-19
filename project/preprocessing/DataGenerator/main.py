import pandas as pd

from create_user import create_insert_user_sql
from create_transaction import create_transaction_sql, execute_transaction_sql, initialize_db
from create_item import insert_item_from_excel_list, insert_item_from_excel
from create_statistics_table import create_statistics_table
import psycopg2 as pg

if __name__ == '__main__':
    # connect DB
    conn = pg.connect(host="127.0.0.1", dbname="youreco", user="postgres", password="postgres", port=5432)
    cur = conn.cursor()

    # # create data based on sql
    # create_insert_user_sql(1000)
    #
    # # initialize db & execute sql files
    initialize_db(cur)
    conn.commit()

    # import items from excel
    insert_item_from_excel_list(cur)
    conn.commit()

    # # create statistics table
    # create_statistics_table()

    # create data on database
    # create_transaction_sql(cur, 1000)
    execute_transaction_sql(cur)
    conn.commit()

    # disconnect DB
    cur.close()
    conn.close()

