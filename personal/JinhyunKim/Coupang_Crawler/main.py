from libs.COUPANG.getUrl import *
from libs.COUPANG.getInfo import *
from libs.COUPANG.createDF import *


def main():
    text = getres(init_url)
    page = get_total_page(text)
    url_list = get_url_list(page)
    df_new = create_df()
    namelist,imglist,pricelist,ratinglist,reviewlist = loop_url_getinfo(url_list)
    df_tmp = fill_df(namelist, imglist, pricelist, ratinglist, reviewlist)
    df = concat_df(df_new,df_tmp)
    to_excel(df)


if __name__== "__main__":
    main()