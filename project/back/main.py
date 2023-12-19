
from flask import Flask, request, send_file
import psycopg2 as pg
from requests import get, post
import asyncio
import os

from lib.send_inferece import send_inference_request
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


@app.route("/api/inference", methods=['GET'])
def create_inference():
    youtube_link = request.args.get('vID', "None")

    # request to vision with snapshot
    print(youtube_link)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_inference_request(youtube_link))
    loop.close()

    print("Successfully transfered youtube link")

    return "Get YoutubeLink {0}".format(youtube_link)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5001)))

