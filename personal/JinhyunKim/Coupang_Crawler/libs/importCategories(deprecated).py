import pandas as pd


#   쿠팡 전체 카테고리 url을 저장한 excel 파일로부터 카테고리 url 가져오는 함수
def excel_to_list():
    categories_list = pd.read_excel('../coupang.xlsx', usecols='B')
    return categories_list
