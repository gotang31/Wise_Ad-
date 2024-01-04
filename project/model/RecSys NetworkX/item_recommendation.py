# item_recommendation.py
import networkx as nx
import random
import pandas as pd

from config import get_graph, find_node_by_attribute

G = get_graph()

def item_recommender(user_id, category_id):
    # Step 1: Find similar users and their rated items
    target_user_node = find_node_by_attribute(G, 'userID', str(user_id))
    if target_user_node:
        similar_users = [v for u, v in G.edges(target_user_node) if G[u][v].get('label') == 'SIMILAR']
    else:
        similar_users = []
    item_scores = {}

    print(similar_users)
    # items that target_user already bought
    target_user_items = [v for u, v, d in G.edges(target_user_node, data=True) if d.get('label') == 'RATED']
    for su in similar_users:
        print(type(su))
        for u, item, data in G.edges(data=True):
            if data.get('label') == 'RATED' and item not in target_user_items and u == su:
                item_data = G.nodes[item]
                # 하나의 item이 동시에 여러 category에 속할 수 있으므로 (['공통']의 경우), 그것을 반영합니다
                category_ids = [G.nodes[v].get('categoryID') for u, v, d in G.edges(item, data=True) if d.get('label') == 'BELONGS_TO']
                if str(category_id) in category_ids:
                    # item 평점을 가져옵니다. 이로 우선순위를 부여합니다.
                    rating = data.get('Rating', 0)
                    item_scores[item] = item_scores.get(item, 0) + float(rating)
        print(item_scores)
        print('category_ids:')
        print(category_ids)
    # Step 2: item을 rating을 기준으로 높은 것을 추천해줍니다.
    top_items = sorted(item_scores, key=item_scores.get, reverse=True)[:4]
    print(top_items)
    # Step 3: Cold Start Problem
    # similar user가 없는 경우, 또는 추천하는 item이 부족한 경우, 자체적인 score를 계산하여 추천을 합니다.
    # 동일 category 내에서 추천을 해줍니다.
    # Calculate the number of recommendations already found
    num_of_recommendations = len(top_items)
    num_of_needed_recommendations = 4 - num_of_recommendations
    print(num_of_needed_recommendations)

    # Cold Start Problem Handling
    if num_of_needed_recommendations > 0:
         # Find the node that represents the specified category
        category_node = find_node_by_attribute(G, 'categoryID', str(category_id))
    
        # Find all item nodes connected to this category node and not in top_items
        all_items_in_category = []
        if category_node:
            for u, v, d in G.edges(data=True):
                #print("Edge from", u, "to", v, "with data:", d)
                if d.get('label') == 'BELONGS_TO' and v == category_node and u not in top_items:
                    all_items_in_category.append(u)
    
        # Calculate a score for each additional item based on NumOfReviews and Rating
        cold_start_scores = {item: float(G.nodes[item].get('NumOfReviews', 0)) * float(G.nodes[item].get('Rating', 0)) for item in all_items_in_category}
        # Select additional items based on the score
        additional_items = sorted(cold_start_scores, key=cold_start_scores.get, reverse=True)[:num_of_needed_recommendations]
        top_items.extend(additional_items)
    
    # Convert node IDs to itemIDs
    recommended_itemIDs = [int(G.nodes[item].get('itemID')) for item in top_items]

    return recommended_itemIDs
