import pandas as pd

# 새로운 데이터프레임을 생성하는 함수
def create_df():
    # 'Name', 'img_src', 'Price', 'Rating', '#ofReviews', 'Link' 열을 가진 빈 데이터프레임을 생성
    df_new = pd.DataFrame(columns=['Name', 'img_src', 'Price', 'Rating', '#ofReviews', 'Link'])
    
    return df_new

# [상품명, 썸네일url, 가격, 별점, 리뷰수, 상세페이지 url] 리스트를 받아 데이터프레임에 채워넣는 함수
def fill_df(namelist, imglist, pricelist, ratinglist, reviewlist, linklist):
    # 각 열에 해당하는 리스트 할당
    df_tmp = pd.DataFrame({'Name': namelist, 'img_src': imglist, 'Price': pricelist, 'Rating': ratinglist,
                           '#ofReviews': reviewlist, 'Link' : linklist})
    
    return df_tmp

# df_new와 df_tmp 데이터프레임을 합치는 함수
def concat_df(df_new, df_tmp):
    df = pd.concat([df_new, df_tmp])
    
    return df

# 데이터프레임을 엑셀 파일로 저장하는 함수
def to_excel(df):
    df.to_excel(f'.//data//sweatshirt//df.xlsx')