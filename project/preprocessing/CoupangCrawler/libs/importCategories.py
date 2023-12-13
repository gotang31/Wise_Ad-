import pandas as pd


def excel_to_list():
    categories_list = pd.read_excel('./category_code.xlsx')
    return categories_list


def category_name_list():
    categories_list = pd.read_excel('./category_code.xlsx')
    name_list = categories_list.name.to_list()
    return name_list


def category_name_to_naver_code(name : str):
    categories_list = pd.read_excel('./category_code.xlsx')
    result = categories_list.loc[categories_list.name == name, ['naver']]
    if result.shape == (1,1):
        naver_code = str(result.iloc[0, 0])
        return naver_code
    else:
        return "Error"



def category_name_to_coupang_code(name : str):
    categories_list = pd.read_excel('./category_code.xlsx')
    result = categories_list.loc[categories_list.name == name, ['coupang']]
    if result.shape == (1,1):
        coupang_code = str(result.iloc[0, 0])
        return coupang_code
    else:
        return "Error"
