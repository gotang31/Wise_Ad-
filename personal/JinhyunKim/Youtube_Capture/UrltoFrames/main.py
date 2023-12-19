    from libs.makeDir import *
from libs.getUrl import *
from libs.getVideo import *
from libs.createFrames import *


def main(url, dir, frame_interval):
    fdir = create_data_directory(url, dir)
    driver = configure_uc(url)
    video_name = collect_video_urls(driver)
    download_videos(fdir, video_name, url)
    create_imgframes(fdir, video_name, frame_interval)
