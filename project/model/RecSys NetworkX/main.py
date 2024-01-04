# main.py
# input = {'detection_category':detection_category, 'userID':userID, 'video_subject':video_subject}
# output = [[tab2_cat, tab3_cat, tab4_cat], tab2_item, tab3_item, tab4_item]
# tab2_item = item_recommender(userID, tab2_cat)
# tab3_item = item_recommender(userID, tab3_cat)
# tab4_item = random_recommender(tab2_cat, tab3_cat, video_subject)


import numpy as np
import pandas as pd
from category_conversion import convert_category
from category_recommendation import category_recommender
from item_recommendation import item_recommender
from random_recommendation import random_recommender


def main(input_data):

    #추천을 위한 변수들을 준비합니다.
    detection_category = int(input_data["detection_category"])
    userID = int(input_data["userID"])
    video_subject = int(input_data["video_subject"])
    key_category = convert_category(detection_category, video_subject)
    
    #tab2, 3 카테고리 추천
    tab2_cat, tab3_cat = category_recommender(userID, key_category)

    #tab2, 3 item 추천
    tab2_item = item_recommender(userID, tab2_cat)
    tab3_item = item_recommender(userID, tab3_cat)

    #tab4 카테고리, item 추천
    tab4_cat, tab4_item = random_recommender(tab2_cat, tab3_cat, video_subject)

    #최종 결과: list 형태
    # [[tab2_cat, tab3_cat, tab4_cat], tab2_item, tab3_item, tab4_item]
    category_list = [tab2_cat, tab3_cat, tab4_cat]
    item_list = [tab2_item, tab3_item, tab4_item]
    result = [category_list] + item_list

    print(result)
    return result


# Main execution
if __name__ == "__main__":
   main()
    
