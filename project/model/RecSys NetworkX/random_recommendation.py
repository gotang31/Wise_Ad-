# random_recommendation.py
import networkx as nx
import random
import pandas as pd

from config import get_graph, find_node_by_attribute

G = get_graph()

def random_recommender(tab2_cat, tab3_cat, video_subject):
    # Find all supercategories belonging to the given metacategory
    # Find the metacategory node
    metacategory_node = None
    for node, data in G.nodes(data=True):
        if data.get('metacategoryID') == str(video_subject):
            metacategory_node = node
    
    # Find all supercategories under this metacategory
    supercategories = [u for u, v, d in G.edges(data=True) if d.get('label') == 'SUPERCATEGORY_BELONGS_TO' and v == metacategory_node]

    # Find all categories within these supercategories, excluding tab2_cat and tab3_cat
    potential_categories = []
    for sc in supercategories:
        categories = [u for u, v, d in G.edges(data=True) if d.get('label') == 'CATEGORY_BELONGS_TO' and v == sc]
        potential_categories.extend(categories)

    # Filter categories and randomly select one
    potential_categories = [cat for cat in potential_categories if G.nodes[cat].get('categoryID') not in [tab2_cat, tab3_cat]]
    tab4_cat = random.choice(potential_categories) if potential_categories else None
    
    # Randomly recommend items from the selected category
    tab4_items = []
    if tab4_cat:
        items_in_category = [u for u, v, d in G.edges(data=True) if d.get('label') == 'BELONGS_TO' and v == str(tab4_cat)]
        tab4_items = random.sample(items_in_category, min(len(items_in_category), 4))

    # Convert node IDs to itemIDs
    tab4_item_ids = [int(G.nodes[item].get('itemID')) for item in tab4_items]

    return int(G.nodes[tab4_cat].get('categoryID')), tab4_item_ids


