from libs.getInput import *
from libs.makedir import *
from libs.getUrl_and_Title import *
from libs.getVideo import *


def main():
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
    channel, cnt, dir, userid, userpw = get_user_input()
    fdir = create_data_directory(channel, dir)
    driver = configure_and_login(channel, userid, userpw)
    scroll_down_page(driver, cnt)
    full_url, video_name = collect_video_urls(driver, cnt)
    df = create_dataframe(video_name, full_url)
    save_video(fdir, df)
    print(df)
if __name__ == "__main__":
    main()