from libs.getUrl import *
from libs.getInfo import *
from libs.createDF import *
from libs.downloadimg import *
from libs.changeExtension import *

def main():
    text = getres(url)  # 크롤링하고자 하는 상품 카테고리 url 로부터 html 반환
    page = get_total_page(text) # 해당 카테고리의 최대 상품 페이지 수 반환
    url_list = get_url_list(page)   # 각 페이지에 대한 url 저장
    df_new = create_df()    # 상품 정보를 저장할 데이터프레임 생성
    namelist,imglist,pricelist,ratinglist,reviewlist, linklist = loop_url_getinfo(url_list) # 각 페이지에서 상품 정보 수집
    df_tmp = fill_df(namelist, imglist, pricelist, ratinglist, reviewlist, linklist)    # 수집된 정보 임시 데이터프레임에 저장
    df = concat_df(df_new,df_tmp)   # 임시 데이터프레임과 상품 정보 데이터프레임 병합
    to_excel(df)    # 상품 정보 데이터프레임 엑셀 파일로 저장
    downloadimg(df) # 수집된 상품에 대한 고해상도 이미지 저장
    changeextension()   # 이미지파일 확장자 .jpg로 통일 (라벨링 사이트에 .jpg 외의 파일 업로드 불가능)

if __name__== "__main__":
    main()