import os
import time


# 데이터를 저장할 디렉토리를 생성하고 해당 디렉토리 경로를 반환하는 함수
def create_data_directory(url, dir):
    now = time.localtime()
    dir_name = f"{now.tm_year:04d}-{now.tm_mon:02d}-{now.tm_mday:02d}-{now.tm_hour:02d}-{now.tm_min:02d}-{now.tm_sec:02d}-{url[32:]}"
    fdir = f"{dir}/{dir_name}"
    os.makedirs(fdir)
    os.chdir(fdir)
    return fdir