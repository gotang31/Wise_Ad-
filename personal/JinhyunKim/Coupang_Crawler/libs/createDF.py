import pandas as pd

def create_df():
    df_new = pd.DataFrame(columns=['Name', 'img_src', 'Price', 'Rating', '#ofReviews', 'Link'])
    return df_new


def fill_df(namelist, imglist, pricelist, ratinglist, reviewlist, linklist):
    df_tmp = pd.DataFrame({'Name': namelist, 'img_src': imglist, 'Price': pricelist, 'Rating': ratinglist,
                           '#ofReviews': reviewlist, 'Link' : linklist})
    return df_tmp


def concat_df(df_new, df_tmp):
    df = pd.concat([df_new, df_tmp])
    return df


def to_excel(df):
    df.to_excel(f'.//data//sweatshirt//df.xlsx')