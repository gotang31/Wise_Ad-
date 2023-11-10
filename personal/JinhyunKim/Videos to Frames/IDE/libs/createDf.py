import pandas as pd


# 데이터 프레임을 생성하는 함수
def create_dataframe(video_name, full_url):
    df = pd.DataFrame({'Title': video_name, 'URL': full_url})
    return df