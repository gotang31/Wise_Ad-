import pandas as pd
from modules.importCategories import get_coupang_category_code_list


def insert_item_from_excel(cursor, category_code : str):
    filename = category_code + ".xlsx"
    print(filename)
    # open category excel
    df = pd.read_excel("./data/" + filename)
    newdf = df[["Name", "Category", "Price", "Rating", "#ofReviews", "img_name"]]
    newdf = newdf.dropna()

    # insert each row
    row_num = len(newdf)
    for i in range(row_num):
        print(newdf.iloc[i,:][4])
        item_name = newdf.iloc[i,:][0].replace("'", "")[:60]
        category_name = newdf.iloc[i,:][1]
        price = newdf.iloc[i,:][2].replace(",", "")
        rating = newdf.iloc[i,:][3]
        reviews = newdf.iloc[i,:][4].replace("(", "").replace(")", "")
        imagefile = newdf.iloc[i,:][5]
        print(item_name, category_name, price, rating, reviews, imagefile)
        cursor.execute(
            "INSERT INTO iteminfo(itemname, category, price, rating, reviews, youreco_reviews, imagefile) VALUES(\'{0}\',{1},{2},{3},{4}, 0,\'{5}\');".format(
                item_name, category_name, price, rating, reviews, imagefile))

def insert_item_from_excel_list(cur):
    category_list = get_coupang_category_code_list()
    for category in category_list:
        insert_item_from_excel(cur, str(category))
