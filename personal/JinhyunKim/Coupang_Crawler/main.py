from libs.getUrl import *
from libs.getInfo import *
from libs.createDF import *
from libs.importCategories import *
from libs.downloadimg import *
from libs.changeExtension import *

def main():
    # categories_list = excel_to_list()
    # 엑셀 파일에서 카테고리 목록을 가져오는 함수 (현재 주석 처리됨)

    text = getres(url)
    # 주어진 URL에서 HTML 내용을 가져오는 함수

    page = get_total_page(text)
    # 가져온 HTML 내용에서 총 페이지 수를 계산하는 함수

    print(page)
    # 계산된 페이지 수 출력

    url_list = get_url_list(page)
    # 각 페이지에 대한 URL 목록을 생성하는 함수

    print(url_list)
    # 생성된 URL 목록 출력

    df_new = create_df()
    # 새로운 데이터프레임을 생성하는 함수

    namelist, imglist, pricelist, ratinglist, reviewlist, linklist = loop_url_getinfo(url_list)
    # URL 목록을 순회하면서 각 상품의 정보를 수집하는 함수

    df_tmp = fill_df(namelist, imglist, pricelist, ratinglist, reviewlist, linklist)
    # 수집된 정보를 바탕으로 임시 데이터프레임을 채우는 함수

    df = concat_df(df_new, df_tmp)
    # 새로운 데이터프레임과 임시 데이터프레임을 합치는 함수

    to_excel(df)
    # 최종 데이터프레임을 엑셀 파일로 저장하는 함수

    downloadimg(df)
    # 데이터프레임에 있는 각 상품의 이미지를 다운로드하는 함수

    changeextension()
    #폴더 내의 다른 확장자를 .jpg로 변경하는 함수



if __name__== "__main__":
    main()