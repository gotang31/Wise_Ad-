import pandas as pd
import config
from decimal import Decimal


def load_data_from_excel(file_path):
    #엑셀 파일을 DataFrame으로 읽어들입니다.
    return pd.read_excel(file_path)


def fetch_data_from_db(query):
    #DB에서 query에 따라 결과를 줍니다.
    with config.get_conn() as conn, conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]
        rows = [[float(val) if isinstance(val, Decimal) else val for val in row] for row in rows]
        return pd.DataFrame(rows, columns=colnames)


def main():
    # Excel에서 데이터 가져오기
    df = load_data_from_excel('./categories.xlsx')

    # DB에서 데이터 가져오기
    items = fetch_data_from_db("select * from iteminfo;")
    users = fetch_data_from_db("select * from userinfo;")
    ratings = fetch_data_from_db("select * from transactioninfo")

    # 아래부터는 graphDB에 Excel, DB에서 가져온 데이터를 그래프로 제작하여 저장하는 단계입니다.
    # python에서 neo4j driver 사용을 위해 configuration
    gds = config.get_gds()
    
    # 혹시 모를 중복 등을 방지하기 위해서 이미 graphDB내에 존재하는 모든 node, relation 삭제를 진행합니다.
    gds.run_cypher('''
        MATCH (n)
        DETACH DELETE (n)
    ''')
    
    # 모든 node 생성
    # 1. Category 추천 관련 node 생성
    # Category nodes (categoryID1, categoryID2, 등등...)
    gds.run_cypher('CREATE CONSTRAINT IF NOT EXISTS FOR (c:Category) REQUIRE (c.categoryID) IS NODE KEY')
    create_category_res = gds.run_cypher('''
        UNWIND $data AS row
        MERGE (c:Category{categoryID: row.categoryID})
        RETURN count(*) AS categories_created
    ''', params ={'data':df.to_dict('records')})
    print('Category nodes 생성 완료')
    
    # supercategory nodes 생성 (['강아지 사료'] ['강아지 간식'] 등등...)
    gds.run_cypher('CREATE CONSTRAINT IF NOT EXISTS FOR (s:Supercategory) REQUIRE (s.supercategoryID) IS NODE KEY')
    create_supercategory_res = gds.run_cypher('''
        UNWIND $data AS row
        MERGE (s:Supercategory{supercategoryID: row.supercategory})
        RETURN count(*) AS supercategories_created
        ''', params ={'data': df.to_dict('records')})
    print('Supercategory nodes 생성 완료')
    
    # category nodes 생성 (0, 1, -1)
    gds.run_cypher('CREATE CONSTRAINT IF NOT EXISTS FOR (m:Metacategory) REQUIRE (m.metacategoryID) IS NODE KEY')
    create_metaacategory_res = gds.run_cypher('''
        UNWIND $data AS row
        MERGE (m:Metacategory{metacategoryID: row.metacategory})
        RETURN count(*) AS metacategories_created
        ''', params ={'data': df.to_dict('records')})
    print('Metacategory nodes 생성 완료')
    
    # 2. Item 추천 관련 node 추가 생성
    # User nodes 생성
    gds.run_cypher('CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE (u.userID) IS NODE KEY')
    create_user_res = gds.run_cypher('''
        UNWIND $data AS row
        MERGE (u:User{userID: row.userid})
        SET u.userName = row.username
        SET u.Age = row.age
        SET u.Gender = row.gender
        RETURN count(*) AS users_created
    ''', params ={'data':users.to_dict('records')})
    print('User nodes 생성 완료')
    
    # Item nodes 생성
    gds.run_cypher('CREATE CONSTRAINT IF NOT EXISTS FOR (i:Item) REQUIRE (i.itemID) IS NODE KEY')
    create_item_res = gds.run_cypher('''
        UNWIND $data AS row
        MERGE (i:Item{itemID: row.itemid})
        SET i.itemName = row.itemname
        SET i.Category = row.category
        SET i.Price = row.price
        SET i.Rating = row.rating
        SET i.NumOfReviews = row.reviews
        SET i.ImgFileName = row.imagefile
        RETURN count(*) AS items_created
    ''', params ={'data':items.to_dict('records')})
    print('Item nodes 생성 완료')
    
    # 모든 relationship 생성 (node와 node 사이 연결 관계를 생성합니다)
    # 1. Category 관련 relationship 생성
    # (Category)-[:CATEGORY_BELONGS_TO]->(Supercategory) relation 생성 (Category보다 Supercategory를 상위 개념으로 두었습니다)
    create_category_belongs_to = gds.run_cypher('''
        UNWIND $data AS row
        MATCH (c:Category{categoryID: row.categoryID}), (s:Supercategory{supercategoryID: row.supercategory})
        MERGE (c)-[r:CATEGORY_BELONGS_TO]->(s)
        RETURN count(*) AS create_category_belongs_to
        ''', params = {'data':df.to_dict('records')})
    print('CATEGORY_BELONGS_TO relationship 생성 완료')
    
    # (Supercategory)-[:SUPERCATEGORY_BELONGS_TO]->(Metacategory) relation 생성 (Supercategory보다 Metacategory를 상위 개념으로 두었습니다)
    create_supercat_belongs_to = gds.run_cypher('''
        UNWIND $data AS row
        MATCH (s:Supercategory{supercategoryID: row.supercategory}), (m:Metacategory{metacategoryID: row.metacategory})
        MERGE (s)-[r:SUPERCATEGORY_BELONGS_TO]->(m)
        RETURN count(*) AS create_supercat_belongs_to
        ''', params = {'data':df.to_dict('records')})
    print('SUPERCATEGORY_BELONGS_TO relationship 생성 완료')
    
    # 2. Item 추천 관련 relationship 생성
    # Rated relationship (User -[:RATED]-> Item relationship 생성) (User가 Item에 평점을 매긴 관계입니다)
    create_rated = gds.run_cypher('''
        UNWIND $data AS row
        MATCH (u:User{userID: row.userid}), (i:Item{itemID: row.itemid})
        MERGE (u)-[r:RATED]->(i)
        SET r.Rating = row.rating
        RETURN count(*) AS create_rated
        ''', params = {'data': ratings.to_dict('records')})
    print('RATED relationship 생성 완료')
    
    # Belongs_to relationship (Item -[:BELONGS_TO)-> Category relationship 생성) (Item이 어떤 Category에 속한다는 관계입니다)
    create_belongs_to = gds.run_cypher('''
        UNWIND $data AS row
        MATCH (i:Item{itemID: row.itemid}), (c:Category{categoryID: row.category})
        MERGE (i)-[b:BELONGS_TO]->(c)
        RETURN count(*) AS create_belongs_to
        ''', params = {'data': items.to_dict('records')})
    print('BELONGS_TO relationship 생성 완료')
    
    # supercategoryID = ['공통']인 것에 
    # (119562, 118920)->238482, (119564, 118922)->238486, (157054, 118926)->275980
    # 이렇게 새로운 categoryID를 부여하여 item을 넣어줍니다. (위에 묶여서 나온 categoryID는 detection 단계에서 하나로 detection을 진행하는 categoryID입니다)
    # 이는 영상에서 강아지, 고양이가 동수일 경우인 video_subject=-1를 대비하는 것입니다.
    create_new_cat = gds.run_cypher('''
        //category mapping을 해줍니다.
        WITH [
            {newCategoryID: 238482, oldCategoryIDs: [119562, 118920]},
            {newCategoryID: 238486, oldCategoryIDs: [119564, 118922]},
            {newCategoryID: 275980, oldCategoryIDs: [157054, 118926]}
        ] AS mappings
        
        UNWIND mappings AS mapping
    
        //newCategory node를 만듭니다.
        MERGE (newCategory:Category {categoryID: mapping.newCategoryID})
        //newCategory가 들어갈 supercategory node인 ['공통']을 newCategory와 relationship을 형성해줍니다.
        MERGE (superCategory:Supercategory {supercategoryID: "['공통']"})
        MERGE (newCategory)-[:CATEGORY_BELONGS_TO]->(superCategory)
    
        //oldCategory node에 연결되어 있던 item들을 newCategory node에도 연결을 해줍니다.
        WITH newCategory, mapping
        MATCH (i:Item)-[:BELONGS_TO]->(c:Category)
        WHERE c.categoryID IN mapping.oldCategoryIDs
        MERGE (i)-[:BELONGS_TO]->(newCategory)
    ''')
    print('newCategory 생성 완료')
    
    # User-User similarity 생성
    # User-User similarity를 생성하기 위해서는 GraphDataScience plugin을 통해서 'user_item_graph'를 생성해줘야 합니다.
    # 이미 해당 그래프가 존재하는 경우, 에러가 발생하기 때문에 존재 여부를 확인하고 없는 경우에 새로 만들어줍니다.
    user_item_graph_existence = gds.run_cypher('''
        CALL gds.graph.exists('user_item_graph')
        YIELD exists
        RETURN exists
        ''')
    
    if not user_item_graph_existence.iat[0,0]:
        create_projection = gds.run_cypher('''
            CALL gds.graph.project(
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
        CALL gds.nodeSimilarity.stream('user_item_graph')
        YIELD node1, node2, similarity
        RETURN gds.util.asNode(node1).userID AS userID1, gds.util.asNode(node2).userID AS userID2, similarity
        ORDER BY similarity DESC, userID1, userID2
    ''')
    # SIMILAR relationship 생성 (사용자 간의 유사도를 바탕으로 사용자 간의 SIMILAR relationship edge를 생성)
    # 위에서 구한 similarity를 기반으로 생성합니다.
    create_similarity = gds.run_cypher('''
        UNWIND $data AS row
        MATCH (u1: User{userID: row.userID1}), (u2: User{userID: row.userID2})
        MERGE (u1)-[s:SIMILAR]->(u2)
        SET s.Similarity = row.similarity
        RETURN count(*) AS create_similarity
        ''', params = {'data': users_similarity.to_dict('records')})
    print('SIMILAR relationship 생성 완료')
    
    # Category 선호도 PREFERENCE relationship 생성 (category 추천을 위해서 어떤 category를 user가 선호하는지 파악)
    create_preference = gds.run_cypher('''
            MATCH (u:User)-[:RATED]->(i:Item)-[:BELONGS_TO]->(c:Category)
            WITH u, count(c) AS total
            MATCH (u)-[:RATED]->(i:Item)-[:BELONGS_TO]->(c:Category)
            WITH u, total, c, count(i)*1.0 AS items
            MERGE (u)-[prefered:PREFERENCE]->(c)
            ON CREATE SET prefered.preference = items/total
            ON MATCH SET prefered.preference = items/total
            RETURN count(*) AS create_preference
        ''')
    print('PREFERENCE relationship 생성 완료')
    
    print('그래프 DB에 그래프 저장 완료')

          
# Main execution
if __name__ == "__main__":
   main()
