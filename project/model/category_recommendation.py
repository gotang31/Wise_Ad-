# category_recommendation.py
#userID와 key_category를 받으면, tab2, tab3에 대한 카테고리를 추천해줍니다.

import config
import pandas as pd


gds = config.get_gds()


def category_recommender(userID, key_category):
    recommend_category = gds.run_cypher('''
        // key_category에 대해서 subcategory를 찾기
        MATCH (keyCategory:Category {categoryID: $key_categoryID})-[:CATEGORY_BELONGS_TO]->(keySubcategory:Subcategory)
        
        // Find similar users
        MATCH (targetUser:User {userID: $userID})-[:SIMILAR]->(similarUser:User)
        
        // Find categories liked by similar users
        MATCH (similarUser)-[:PREFERENCE]->(category:Category)-[:CATEGORY_BELONGS_TO]->(subcategory:Subcategory)
        WHERE category.categoryID <> $key_categoryID AND subcategory.subcategoryID = keySubcategory.subcategoryID
        WITH category.categoryID AS categoryID, COUNT(*) AS recommendationScore
        RETURN categoryID
        ORDER BY recommendationScore DESC
        LIMIT 2
        ''', params={'userID':userID, 'key_categoryID': key_category})
    
    # 카테고리 추천 수를 확인한다
    cat_rec_num = recommend_category.shape[0]
    cat_rec_num
    
    # 만약에 카테고리 추천 수가 2보다 적을 경우, 랜덤으로 더해줘야 한다.
    # 추천해준 카테고리 수가 1개인 경우
    if cat_rec_num == 1:
        category_id = int(recommend_category['category.categoryID'].iloc[0])
            
        additional_rec_cat = gds.run_cypher('''
        MATCH (keyCategory:Category {categoryID: $key_categoryID})-[:CATEGORY_BELONGS_TO]->(keySubcategory:Subcategory)
        MATCH (category:Category)-[:CATEGORY_BELONGS_TO]->(subcategory:Subcategory)
        WHERE NOT category.categoryID = $categoryID AND NOT category.categoryID = $key_categoryID AND subcategory.subcategoryID = keySubcategory.subcategoryID
        WITH category.categoryID AS categoryID 
        return categoryID
        ORDER BY rand()
        LIMIT 1
        ''', params={'categoryID':category_id, 'userID':userID, 'key_categoryID': key_category})
    
        recommend_category = pd.concat([recommend_category, additional_rec_cat], ignore_index = True)

    # 추천해준 카테고리 수가 0개인 경우
    elif cat_rec_num == 0:
        additional_rec_cat = gds.run_cypher('''
        MATCH (keyCategory:Category {categoryID: $key_categoryID})-[:CATEGORY_BELONGS_TO]->(keySubcategory:Subcategory)
        MATCH (category:Category)-[:CATEGORY_BELONGS_TO]->(subcategory:Subcategory)
        WHERE NOT category.categoryID = $key_categoryID AND subcategory.subcategoryID = keySubcategory.subcategoryID
        WITH category.categoryID AS categoryID
        RETURN categoryID
        ORDER BY rand()
        LIMIT 2
        ''', params={'userID':userID, 'key_categoryID': key_category})
    
        recommend_category = pd.concat([recommend_category, additional_rec_cat], ignore_index = True)

    tab2_cat = recommend_category.to_dict('index')[0]['categoryID']
    tab3_cat = recommend_category.to_dict('index')[1]['categoryID']

    return tab2_cat, tab3_cat