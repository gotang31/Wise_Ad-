import psycopg2 as pg
from requests import post
from functools import cache

conn = pg.connect(host="127.0.0.1", dbname="youreco", user="postgres", password="postgres", port=5432)
cur = conn.cursor()


# get iteminfo list from itemid
def item_id_to_info(itemid):
    cur.execute("select * from iteminfo where itemid = {0};".format(itemid))
    res = cur.fetchone()
    item_name = res[1]
    item_price = res[3]
    image_filename = res[7]
    item_link = res[8]
    return [item_name, item_price, image_filename, item_link]


# create itemdata sheet
def create_section_object(start_time, end_time, category, video_subject):
    coverted_cate = convert_category(category, video_subject)
    rec_dict = {
        "start_time": start_time,
        "end_time": end_time,
        "category": [coverted_cate],
        "sim_item": [],
        "rel_item_01": [],
        "rel_item_02": [],
        "rel_item_03": []
    }

    return rec_dict


def create_new_section_list(section_list):
    new_section_list = []

    for section in section_list:
        rel_item_list = get_recommendation(section[4], 10, section[6]) #7 is dummy value section[4] is detection category

        new_section = create_section_object(section[2], section[3], section[4], section[6])
        rel_item_categories = rel_item_list[0]
        rel_item_01_code = rel_item_list[1]
        rel_item_02_code = rel_item_list[2]
        rel_item_03_code = rel_item_list[3]

        # sim_item
        for each_item in section[5]:
            item = item_id_to_info(each_item)
            new_section["sim_item"].append(item)

        for categories in rel_item_categories:
            new_section["category"].append(categories)

        # rel_item_01
        for each_item in rel_item_01_code:
            item = item_id_to_info(each_item)
            new_section["rel_item_01"].append(item)

        # rel_item_02
        for each_item in rel_item_02_code:
            item = item_id_to_info(each_item)
            new_section["rel_item_02"].append(item)

        # rel_item_03
        for each_item in rel_item_03_code:
            item = item_id_to_info(each_item)
            new_section["rel_item_03"].append(item)

        new_section_list.append(new_section)

    return new_section_list

cache = {}
def get_recommendation(category, userid, video_subject):
    # communicate with rec server
    # test에서 사용한 curl:
    # curl -X POST http://127.0.0.1:5012/recommend -H "Content-Type: application/json" -d '{"detection_category":7, "userID":10, "video_subject":0}'

    cache_key = "cate" + str(category) + "uid" + str(userid) + "vsub" + str(video_subject)
    if cache_key not in cache:
        resp_reco = post('http://127.0.0.1:5012/recommend', json={'detection_category': category, 'userID': userid, 'video_subject': video_subject})
        print("requested to recsys docker")
        cache[cache_key] = resp_reco.json()
    return cache[cache_key]


def convert_category(detection_category, video_subject):
    if video_subject == 1:
        # Mapping for video_subject = 1 (고양이)
        mapping = {2: 118920, 3: 118923, 4: 119567, 5: 119567, 6: 119558, 7: 119562, 8: 119564, 9: 157054}
    elif video_subject == 0:
        # Mapping for video_subject = 0 (강아지)
        mapping = {2: 118920, 3: 118923, 4: 119567, 5: 119567, 6: 119558, 7: 118920, 8: 118922, 9: 118926}
    else:
        # Mapping for video_subject = -1 (공통)
        mapping = {2: 118920, 3: 118923, 4: 119567, 5: 119567, 6: 119558, 7: 238482, 8: 238486, 9: 275980}

    return mapping.get(detection_category)

# print(convert_category(2,1))
# print(convert_category(7,1))
# print(convert_category(3,1))