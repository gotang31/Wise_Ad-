# RecSys 구현

app.py는 Flask file입니다. <br>
app.py를 실행한 후, curl 명령어를 통해서 입력 (명령어 예시는 'curl 사용' 파일을 참고해주세요)을 넣어주면, 추천을 진행해 줍니다.

categories.xlsx는 상품DB에 있는 모든 카테고리를 기록하고 있는 엑셀 파일입니다. <br>
이를 통해 graphDB에 category node를 구축합니다.

config.py의 내용을 반드시 본인에게 맞도록 적절히 수정하여 사용해주세요. <br>
graphDB를 local/online을 사용할 것인지, 연결되는 RDB (postgresql)의 로그인 정보를 수정할 수 있습니다.


