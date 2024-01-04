# config.py
import networkx as nx
import warnings

# GraphML에서 data를 networkX로 바꾸는 과정에서 data type 관련해서 중요하지 않은 에러 (type 지정 안함)이 있습니다.
# 이는 크게 상관이 없으므로 무시합니다.
warnings.filterwarnings('ignore')

def create_graph():
    # Path to the GraphML file
    # GraphML은 neo4j에서 제작하였습니다.
    graphml_file_path = 'neo4jdata.graphml'
    return nx.read_graphml(graphml_file_path)

# config.py가 import되면 한번만 graph G를 생성하도록 합니다.
G = create_graph()

def get_graph():
    global G
    return G

def find_node_by_attribute(G, attr, value):
    # userID 또는 categoryID로 각 node를 찾는 함수입니다.
    # 이는 graphDB에서 networkX로 옮겨 오면서 발생하는 ID 차이로 인해 사용합니다.
    for node, data in G.nodes(data=True):
        if data.get(attr) == value:
            return node
    return None


