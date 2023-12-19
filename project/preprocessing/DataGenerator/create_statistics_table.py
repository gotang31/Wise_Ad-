from modules.get_statistics_naver import get_item_distribution
from modules.importCategories import get_naver_category_code_list
import pandas as pd


def create_statistics_table():

    statistics_table = {}

    naver_categories = get_naver_category_code_list()

    for value in naver_categories:
        statistics_table[value] = get_item_distribution(value)
        print("value", value, "completed")

    df = pd.DataFrame.from_dict(statistics_table)
    df.to_excel('./statistics.xlsx')