# random_recommendation.py
import config


gds = config.get_gds()


def random_recommender(tab2_cat, tab3_cat, video_subject):
    random_category = gds.run_cypher('''
        MATCH (c:Category)-[:CATEGORY_BELONGS_TO]->(s:Supercategory)-[:SUPERCATEGORY_BELONGS_TO]->(m:Metacategory)
        WHERE NOT c.categoryID = $categoryID1
        AND NOT c.categoryID = $categoryID2
        AND m.metacategoryID = $metacategoryID
        WITH c.categoryID AS categoryID
        RETURN categoryID
        ORDER BY rand()
        LIMIT 1
    ''', params = {'categoryID1':tab2_cat, 'categoryID2':tab3_cat, 'metacategoryID':video_subject})

    tab4_cat = int(random_category.iat[0,0])

    random_item_recommender = gds.run_cypher('''
        MATCH (i:Item)-[:BELONGS_TO]->(c:Category)
        WHERE c.categoryID = $categoryID
        WITH i.itemID AS itemID
        RETURN itemID
        ORDER BY rand()
        LIMIT 4
''', params = {'categoryID':int(tab4_cat)})

    tab4_item = random_item_recommender['itemID'].values.tolist()
    
    return tab4_cat, tab4_item
