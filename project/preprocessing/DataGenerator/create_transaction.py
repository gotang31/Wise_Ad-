import random
import pandas as pd
from modules.create_dummydata import create_rating, weighted_create
from modules.importCategories import get_naver_category_code_list, naver_code_to_coupang_code


def execute_initialize_sqls(cursor, path: str):
    cursor.execute("select count(*) from pg_stat_user_tables;")
    if cursor.fetchone()[0] == 3:
        cursor.execute(open("{0}/youreco_clear.sql".format(path), "r").read())
    cursor.execute(open("{0}/youreco_init.sql".format(path), "r").read())
    cursor.execute(open("{0}/youreco_create_shopping_table.sql".format(path), "r").read())
    cursor.execute(open("{0}/insert_user.sql".format(path), "r", encoding='utf-8').read())


def initialize_db(cur):
    sql_directory_path = 'C:/Users/knuyh/Desktop/민지/고려대학교 교육/프로젝트/project/preprocessing/DataGenerator/sql'
    execute_initialize_sqls(cur, sql_directory_path)


def get_random_user_from_db(cursor):
    cursor.execute("SELECT COUNT(*) FROM userinfo;")
    userNum = cursor.fetchone()[0]
    random_id = random.randint(0,userNum - 1)
    cursor.execute("SELECT * FROM userinfo WHERE userid = {0}".format(random_id))
    random_user = cursor.fetchone()

    return random_user


def get_user_statistics_idx(user):
    random_user_age = user[2]
    random_user_gender = user[3]
    random_user_gen = (int(random_user_age/10)*10)
    statistics_idx = "{0}_{1}s".format(random_user_gender,random_user_gen)

    return statistics_idx


def get_statistics_weights(stat_idx: str):
    map_idx = {"male_10s": 0, "female_10s": 1, "male_20s": 2, "female_20s": 3, "male_30s": 4, "female_30s": 5, "male_40s": 6, "female_40s": 7, "male_50s": 8, "female_50s": 9, "male_60s": 10, "female_60s": 11 }
    idx = map_idx[stat_idx]
    stat = pd.read_excel('./statistics.xlsx')
    weights = stat.loc[stat['Unnamed: 0'] == idx].iloc[:, 1:].to_dict('records')[0]

    return weights


# return bought item and rated score for evaluation(unnecessary)
def create_review_by_category(userid, category_id, cursor, file):

    cursor.execute("SELECT * FROM iteminfo WHERE category = {0}".format(category_id))
    itemlist = cursor.fetchall()
    listSize = len(itemlist)
    random_idx = random.randint(0, listSize - 1)
    random_item = itemlist[random_idx]
    rating = create_rating()
    # iterate n time : assume multiple purchase at onetime
    n = weighted_create([1, 2, 3, 4, 5, 6],[0.6, 0.2, 0.1, 0.05, 0.03, 0.02])
    for i in range(n):
        file.write("INSERT INTO transactioninfo(userid, itemid, rating) VALUES({0},{1},{2});\n".format(userid, random_item[0], rating))
        file.write("UPDATE iteminfo set youreco_reviews = youreco_reviews + 1 where itemid = {0};\n".format(random_item[0]))

    return [random_item, rating]


def create_transaction(cur, file):
    rand_user = get_random_user_from_db(cur)
    rand_stat_idx = get_user_statistics_idx(rand_user)
    # print("this user group :", rand_stat_idx)
    weights = get_statistics_weights(rand_stat_idx)
    # print("purchase probability for each category :", weights)

    naver_category_code_list = get_naver_category_code_list()
    for category in naver_category_code_list:
        probability_idx = int(category)
        buy = random.choices([0, 1],[1 - weights[probability_idx], weights[probability_idx]])[0]
        if buy == 0:
            pass
        elif buy == 1:
            coupang_category = naver_code_to_coupang_code(category)
            bought = create_review_by_category(rand_user[0], coupang_category, cur, file)
            # print("User", rand_user[1], "bought", bought[0][1], "and rated", bought[1])


def create_transaction_sql(cur, iter_num: int):
    flag = 0
    f = open('./sql/insert_transaction.sql', 'w', encoding="utf-8")
    for i in range(iter_num):
        create_transaction(cur, f)
        flag += 1
        if flag % 100 == 0:
            print("100 transactions added")
    f.close()


def execute_transaction_sql(cur):
    path = 'C:/Users/knuyh/Desktop/민지/고려대학교 교육/프로젝트/project/preprocessing/DataGenerator/sql'
    cur.execute(open("{0}/insert_transaction.sql".format(path), "r", encoding='utf-8').read())
