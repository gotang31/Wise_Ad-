# category_recommendation.py
#userID와 key_category를 받으면, tab2, tab3에 대한 카테고리를 추천해줍니다.
import networkx as nx
import random
import pandas as pd

from config import get_graph, find_node_by_attribute

G = get_graph()

def category_recommender(user_id, key_category_id):
    # Step 1: Find the keySupercategory of the keyCategory
    key_category_node = find_node_by_attribute(G, 'categoryID', key_category_id)
    key_supercategory_node = None
    for u, v, d in G.edges(key_category_node, data=True):
        if d.get('label') == 'CATEGORY_BELONGS_TO':
            key_supercategory_node = v
            break

    if not key_supercategory_node:
        raise ValueError("Key supercategory not found")
    
    # Step 2: Find similar users
    target_user_node = find_node_by_attribute(G, 'userID', str(user_id))
    # Similar user가 없는 경우에는 이를 빈 list로 해줘야 한다. 
    # 이렇게 하지 않으면 모든 edges를 다 가져오기 때문에 문제가 생긴다.
    if target_user_node:
        similar_users = [v for u, v in G.edges(target_user_node) if G[u][v].get('label') == 'SIMILAR']
    else:
        similar_users = []
    
    # Initialize recommended_categories
    recommended_categories = {}

    # If there are similar users, proceed with collaborative filtering
    if similar_users:
        for su in similar_users:
            for u, v, d in G.edges(su, data=True):
                if d.get('label') == 'PREFERENCE':
                    if any(d.get('label') == 'CATEGORY_BELONGS_TO' for _, _, d in G.edges(v, data=True)):
                        category_id = G.nodes[v].get('categoryID')
                        recommended_categories[category_id] = recommended_categories.get(category_id, 0) + 1

        # Sort and get top 2 categories
        sorted_categories = sorted(recommended_categories, key=recommended_categories.get, reverse=True)[:2]

    else:
        # If no similar users, pick 2 random categories from the same supercategory
        potential_categories = [u for u, v, d in G.edges(key_category_node, data=True) 
                                if d.get('label') == 'CATEGORY_BELONGS_TO' and G.nodes[u].get('categoryID') != key_category_id]
        # no duplicates
        potential_categories = list(set(potential_categories))

        # Randomly select up to 2 categories
        selected_nodes = random.sample(potential_categories, 2) 
        sorted_categories = [G.nodes[v].get('categoryID') for v in selected_nodes]

    return [int(x) for x in sorted_categories[:2]]

