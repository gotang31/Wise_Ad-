import pandas as pd

def create_df():
    # 새로운 데이터프레임 생성 함수
    # 'Name', 'img_src', 'Price', 'Rating', '#ofReviews', 'Link' 열을 가진 빈 데이터프레임을 생성
    df_new = pd.DataFrame(columns=['Name', 'Category', 'img_src', 'Price', 'Rating', '#ofReviews', 'img_name', 'Link'])
    return df_new

def fill_df(namelist, category, imglist, pricelist, ratinglist, reviewlist, imgnamelist, linklist):
    # 수집된 상품 정보를 데이터프레임에 채우는 함수
    # 각 리스트를 해당 열에 매핑하여 데이터프레임을 생성
    df_tmp = pd.DataFrame({
        'Name': namelist,
        'Category': category,
        'img_src': imglist,
        'Price': pricelist,
        'Rating': ratinglist,
        '#ofReviews': reviewlist,
        'img_name' : imgnamelist,
        'Link': linklist
    })
    return df_tmp

def concat_df(df_new, df_tmp):
    # 두 데이터프레임을 합치는 함수
    # df_new와 df_tmp를 합쳐서 하나의 데이터프레임으로 반환
    df = pd.concat([df_new, df_tmp])
    return df

def to_excel(df, filename):
    # 데이터프레임을 엑셀 파일로 저장하는 함수
    # 지정된 경로에 데이터프레임을 엑셀 파일로 저장
    df.to_excel('./data/{0}.xlsx'.format(filename))