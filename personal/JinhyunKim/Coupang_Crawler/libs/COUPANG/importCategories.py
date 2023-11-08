import pandas as pd


def excel_to_list():
    categories_list = pd.read_excel('/Users/jhk/PycharmProjects/Wise_Ad-/personal/JinhyunKim/Coupang_Crawler/coupang.xlsx', usecols='B')
    return categories_list
