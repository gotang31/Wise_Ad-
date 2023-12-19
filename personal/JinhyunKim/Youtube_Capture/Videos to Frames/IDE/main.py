from libs.getInput import *
from libs.makeDir import *
from libs.getUrl import *
from libs.createDf import *
from libs.getVideo import *
from libs.createFrames import *


def main(channel, cnt, dir):
    fdir = create_data_directory(channel, dir)
    driver = configure_uc(channel)
    scroll_down_page(driver, cnt)
    video_name, full_url = collect_video_urls(driver, cnt)
    df = create_dataframe(video_name, full_url)
    download_videos(fdir, df)
    create_imgframes(fdir,df)
