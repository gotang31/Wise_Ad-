크리에이터 ID, 최근 영상부터 저장할 영상 갯수, 저장할 경로 지정해주면 \
df로 영상 제목 및 url 저장한 후, \
pytube 이용해 영상을 Data 폴더 안에 {제목}.mp4 파일로 저장. \
OpenCV 이용해 {제목} 폴더 안에 1초 단위로 분할한 .jpg 이미지 생성.

Required Pkgs: \
selenium 4.9.0 # !pip install selenium==4.9.0 \
undetected_chromedriver \
BeautifulSoup4 \
pandas \
re \
pytube \
opencv-python

