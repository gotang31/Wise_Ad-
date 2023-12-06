import pandas as pd


def excel_to_list():
    categories_list = pd.read_excel('./coupang.xlsx', usecols='B')
    return categories_list
