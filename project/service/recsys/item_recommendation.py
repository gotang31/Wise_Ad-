# item_recommendation.py
import config
import pandas as pd


gds = config.get_gds()


def item_recommender(userID, categoryID):
    # Graph 구조를 활용한 collaborate filtering을 실시하여 추천을 진행합니다.
    recommendation = gds.run_cypher('''
    MATCH (u1:User)-[r1:SIMILAR]-(u2)-[r2:RATED]-(i:Item), (i)-[:BELONGS_TO]->(c:Category)
    WHERE id(u1) = $userID
    AND NOT ((u1)-[]-(i))
    AND c.categoryID = $categoryID
    WITH Sum(r1.Similarity*r2.Rating)/sum(r1.Similarity)+log(count(r2)) as score, i
    RETURN i.itemID
    ORDER BY score DESC
''', params = {'userID':userID, 'categoryID':categoryID})

    # 적절한 수의 아이템을 추천해주는지를 확인합니다.
    num_of_recommendations = recommendation[:4].shape[0]
    # 사용자의 정보 부족으로 인해서 적절한 수의 추천 아이템을 가져오지 못했는지 확인하기 위해서 더 필요한 추천 아이템의 수를 계산합니다.
    num_of_needed_recommendations = 4 - num_of_recommendations

    # Cold Start 문제를 해결하기 위해 자체적인 score를 도입하여, 사용자 정보와 관계 없이 상품을 추천해줍니다.
    # 여기에서 score에 아이템에 달린 리뷰 수와 평점을 반영합니다.
    if num_of_needed_recommendations > 0:
        additional_recommendations = gds.run_cypher('''
        MATCH (i:Item)-[:BELONGS_TO]->(c:Category)
        WHERE c.categoryID = $categoryID
        WITH i.NumOfReviews*i.Rating as score, i
        RETURN i.itemID
        ORDER BY score DESC
    ''', params = {'categoryID': categoryID})

        total_recommendations = [recommendation, additional_recommendations[:num_of_needed_recommendations]]
        result = pd.concat(total_recommendations)
    
    else:
        result = recommendation[:4]

    return result['i.itemID'].values.tolist()