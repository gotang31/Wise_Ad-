import psycopg2 as pg
import pandas as pd


if __name__ == "__main__":
    conn = pg.connect(host="127.0.0.1", dbname="youreco", user="postgres", password="postgres", port=5432)
    cur = conn.cursor()

    cur.execute("select * from iteminfo")
    row = cur.fetchall()

    itemid = list(map(lambda x:x[0], row))
    category = list(map(lambda x:x[2], row))
    imagefile = list(map(lambda x:x[-1], row))

    item_table = pd.DataFrame({'itemid': itemid, 'category' : category, 'imagefile' : imagefile})
    item_table.to_csv('item_table.csv', index = False)
