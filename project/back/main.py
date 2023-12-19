from flask import Flask, request, send_file
import psycopg2 as pg
from requests import get, post
import os

from lib.fill_recommendation import create_new_section_list


app = Flask(__name__)

conn = pg.connect(host="127.0.0.1", dbname="youreco", user="postgres", password="postgres", port=5432)
cur = conn.cursor()

@app.route("/api/test", methods=['GET'])
def response():
    return "Hello, World"


@app.route("/api/image", methods=['GET'])
def returnImage():
    imageID = request.args.get('imgID', "None")
    cateID = request.args.get('category', "None")
    return send_file('data\\{0}\\{1}\\{2}.jpg'.format(cateID, imageID, imageID))

@app.route("/api/videoinfo", methods=['GET'])
def send_by_link():
    youtube_link = request.args.get('vID', "None")
    if youtube_link != "":
        cur.execute("SELECT * FROM inferenceinfo where url='{0}';".format(youtube_link))
        section_list = cur.fetchall()
        if len(section_list) == 0:
            return 'None'
        elif len(section_list) > 0:

            # append rel_items
            new_section_list = create_new_section_list(section_list)


            return new_section_list


@app.route("/api/videosecinfo", methods=['GET'])
def send_by_link_sec():
    youtube_link = request.args.get('vID', "None")
    youtube_second = request.args.get('second', "None")

    # request to vision with snapshot



    return "Get YoutubeLink {0} {1}".format(youtube_link, youtube_second)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5001)))


# url = 'frontend에서 받는 url'
# image_name = 'frontend에서 받는 image_name'
#
# similar_itemid_list = ''
# category_list = ''
# split_time_list = ''
#
# # json file response
# if url: #
#     resp_vision = post('http://172.29.50.29:5000/infer', url)
#     similar_itemid_list = resp_vision['similar_itemid_list']
#     category_list = resp_vision['category_list']
#     split_time_list = resp_vision['split_time_list']
#     video_subject = resp_vision['video_subject']
#
#     resp_reco = post('http://172.29.50.29:5000/infer', json = {'category_list' : category_list, 'video_subject': video_subject})
#
# else:
#     resp_vision = post('http://172.29.50.29:5000/infer', image_name)
#     similar_itemid_list = resp_vision['similar_itemid_list']
#     category_list = resp_vision['category_list']
#
#     resp_reco = post('http://172.29.50.29:5000/infer', json = {'category_list' : category_list, })

