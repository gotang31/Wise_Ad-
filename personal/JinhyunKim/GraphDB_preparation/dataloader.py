import pandas as pd
import config
from decimal import Decimal

def load_data_from_excel(file_path):
    """
    엑셀파일을 읽어들입니다.
    """
    return pd.read_excel(file_path)

def fetch_data_from_db(query):
    """
    DB에서 query에 따라 결과를 줍니다.
    """
    with config.get_conn() as conn, conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]
        rows = [[float(val) if isinstance(val, Decimal) else val for val in row] for row in rows]
        return pd.DataFrame(rows, columns=colnames)

def main():
    # Load data from Excel
    df = load_data_from_excel('./categories.xlsx')

    # Fetch data from the database
    items = fetch_data_from_db("select * from iteminfo;")
    users = fetch_data_from_db("select * from userinfo;")
    ratings = fetch_data_from_db("select * from transactioninfo")

    # Load data to graph DB
    gds = config.get_gds()
    # 모든 node, relation 삭제
    # 혹시 모를 중복 등을 방지하기 위해서 실행합니다.
    gds.run_cypher('''
        match (n)
        detach delete (n)
    ''')
    # 모든 node 생성
    # 1. Category 추천 관련 node 생성
    # Category nodes (이미 만들어져 있는 category nodes에 추가가 됩니다.) (categoryID)
    gds.run_cypher('create constraint if not exists for (c:Category) require (c.categoryID) is node key')
    create_category_res = gds.run_cypher('''
        unwind $data as row
        merge (c:Category{categoryID: row.categoryID})
        return count(*) as categories_created
    ''', params ={'data':df.to_dict('records')})
    
    # subcategory nodes 생성 (['강아지 사료'] ['강아지 간식'] 등등...)
    gds.run_cypher('create constraint if not exists for (s:Subcategory) require (s.subcategoryID) is node key')
    create_subcategory_res = gds.run_cypher('''
        unwind $data as row
        merge (s:Subcategory{subcategoryID: row.subcategory})
        return count(*) as subcategories_created
        ''', params ={'data': df.to_dict('records')})
    
    # supercategory nodes 생성 (0, 1, -1)
    gds.run_cypher('create constraint if not exists for (s:Supercategory) require (s.supercategoryID) is node key')
    create_supercategory_res = gds.run_cypher('''
        unwind $data as row
        merge (s:Supercategory{supercategoryID: row.supercategory})
        return count(*) as supercategories_created
        ''', params ={'data': df.to_dict('records')})
    
    # 2. Item 추천 관련 node 추가 생성
    # User nodes 생성
    gds.run_cypher('create constraint if not exists for (u:User) require (u.userID) is node key')
    create_user_res = gds.run_cypher('''
        unwind $data as row
        merge (u:User{userID: row.userid})
        set u.userName = row.username
        set u.Age = row.age
        set u.Gender = row.gender
        return count(*) as users_created
    ''', params ={'data':users.to_dict('records')})
    
    # Item nodes 생성
    gds.run_cypher('create constraint if not exists for (i:Item) require (i.itemID) is node key')
    create_item_res = gds.run_cypher('''
        unwind $data as row
        merge (i:Item{itemID: row.itemid})
        set i.itemName = row.itemname
        set i.Category = row.category
        set i.Price = row.price
        set i.Rating = row.rating
        set i.NumOfReviews = row.reviews
        set i.ImgFileName = row.imagefile
        return count(*) as items_created
    ''', params ={'data':items.to_dict('records')})
    
    ################################################
    # 모든 relationship 생성
    # 1. Category 관련 relationship 생성
    # (Category)-[:CATEGORY_BELONGS_TO]->(Subcategory) relation 생성
    create_category_belongs_to = gds.run_cypher('''
        unwind $data as row
        match (c:Category{categoryID: row.categoryID}), (s:Subcategory{subcategoryID: row.subcategory})
        merge (c)-[r:CATEGORY_BELONGS_TO]->(s)
        return count(*) as create_category_belongs_to
        ''', params = {'data':df.to_dict('records')})
    
    # (Subcategory)-[:SUBCATEGORY_BELONGS_TO]->(Supercategory) relation 생성
    create_subcat_belongs_to = gds.run_cypher('''
        unwind $data as row
        match (s:Subcategory{subcategoryID: row.subcategory}), (ss:Supercategory{supercategoryID: row.supercategory})
        merge (s)-[r:SUBCATEGORY_BELONGS_TO]->(ss)
        return count(*) as create_subcat_belongs_to
        ''', params = {'data':df.to_dict('records')})
    
    # 2. Item 추천 관련 relationship 생성
    # Rated relationship (User -[:RATED]-> Item relationship 생성)
    create_rated = gds.run_cypher('''
        unwind $data as row
        match (u:User{userID: row.userid}), (i:Item{itemID: row.itemid})
        merge (u)-[r:RATED]->(i)
        set r.Rating = row.rating
        return count(*) as create_rated
        ''', params = {'data': ratings.to_dict('records')})
    
    
    # Belongs_to relationship (Item -[:BELONGS_TO)-> Category relationship 생성)
    create_belongs_to = gds.run_cypher('''
        unwind $data as row
        match (i:Item{itemID: row.itemid}), (c:Category{categoryID: row.category})
        merge (i)-[b:BELONGS_TO]->(c)
        return count(*) as create_belongs_to
        ''', params = {'data': items.to_dict('records')})
    
    # subcategoryID = ['공통']인 것에 (119834, 119247)->239081, (119855, 119286)->239141, (157054, 118926)->275980
    # 이렇게 새로운 categoryID를 부여하여 item을 넣어줍니다.
    # 이는 영상에서 강아지, 고양이가 동수일 경우 (video_subject=-1)를 대비하는 것입니다.
    
    create_new_cat = gds.run_cypher('''
        //category mapping을 해줍니다.
        with [
            {newCategoryID: 238482, oldCategoryIDs: [119562, 118920]},
            {newCategoryID: 238486, oldCategoryIDs: [119564, 118922]},
            {newCategoryID: 275980, oldCategoryIDs: [157054, 118926]}
        ] as mappings
        
        unwind mappings as mapping
    
        //새로운 category node를 만듭니다.
        merge (newCategory:Category {categoryID: mapping.newCategoryID})
        //새 category가 들어갈 subcategory node
        merge (subCategory:Subcategory {subcategoryID: "['공통']"})
        merge (newCategory)-[:CATEGORY_BELONGS_TO]->(subCategory)
    
        //이전 category node에만 연결되어 있던 item들을 새로운 category node에도 연결을 해줍니다.
        with newCategory, mapping
        match (i:Item)-[:BELONGS_TO]->(c:Category)
        where c.categoryID IN mapping.oldCategoryIDs
        merge (i)-[:BELONGS_TO]->(newCategory)
    ''')
    
    # User-User similarity 생성
    # User-User similarity
    user_item_graph_existence = gds.run_cypher('''
        CALL gds.graph.exists('user_item_graph')
        YIELD exists
        RETURN exists
        ''')
    
    if not user_item_graph_existence.iat[0,0]:
        create_projection = gds.run_cypher('''
            call gds.graph.project(
            'user_item_graph',
            ['User', 'Item'],
            {
                RATED: {properties: 'Rating'}
                    }
        );
        ''')
    
    # User similarity 계산 (사용자 간의 유사도를 계산)
    # 이 함수에서는 모든 node 간의 similarity를 구합니다.
    # 저희는 이 중에서 user 간의 similarity score만 있으면 되기 때문에 이를 따로 추출합니다.
    # nodeSimilarity는 Jaccard Similarity를 사용합니다.
    # 참고: https://neo4j.com/docs/graph-data-science/current/algorithms/node-similarity/ 
    users_similarity = gds.run_cypher('''
        call gds.nodeSimilarity.stream('user_item_graph')
        yield node1, node2, similarity
        return gds.util.asNode(node1).userID AS userID1, gds.util.asNode(node2).userID AS userID2, similarity
        order by similarity descending, userID1, userID2
    ''')
    
    # Similarity relationship 생성 (사용자 간의 유사도를 바탕으로 사용자 간의 relationship edge를 생성)
    create_similarity = gds.run_cypher('''
        unwind $data as row
        match (u1: User{userID: row.userID1}), (u2: User{userID: row.userID2})
        merge (u1)-[s:SIMILAR]->(u2)
        set s.Similarity = row.similarity
        return count(*) as create_similarity
        ''', params = {'data': users_similarity.to_dict('records')})
    
    # Category 선호도 relationship 생성 (category 추천을 위해서 어떤 category를 user가 선호하는지 파악)
    create_preference = gds.run_cypher('''
            match (u:User)-[:RATED]->(i:Item)-[:BELONGS_TO]->(c:Category)
            with u, count(c) as total
            match (u)-[:RATED]->(i:Item)-[:BELONGS_TO]->(c:Category)
            with u, total, c, count(i)*1.0 as items
            merge (u)-[prefered:PREFERENCE]->(c)
            on create set prefered.preference = items/total
            on match set prefered.preference = items/total
            return count(*) as create_preference
        ''')


# Main execution
if __name__ == "__main__":
   main()
