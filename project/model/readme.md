# RecSys 구현

dataloader.py의 경우, graphDB 내에 있는 데이터를 업데이트하거나, 처음으로 데이터를 넣을 때 실행시켜주면 됩니다. <br>
반드시 동일한 경로 안에 categories.xlsx와 config.py가 있어야 합니다. <br>
또한 graphDB가 켜져 있는지 확인이 필요합니다.

app.py는 Flask file입니다. <br>
app.py를 실행한 후, curl 명령어를 통해서 입력 (명령어 예시는 'curl 사용' 파일을 참고해주세요)을 넣어주면, 추천을 진행해 줍니다.

categories.xlsx는 상품DB에 있는 모든 카테고리를 기록하고 있는 엑셀 파일입니다. <br>
이를 통해 graphDB에 category node를 구축합니다.

config.py의 내용을 반드시 본인에게 맞도록 적절히 수정하여 사용해주세요. <br>
graphDB를 local/online을 사용할 것인지, 연결되는 RDB (postgresql)의 로그인 정보를 수정할 수 있습니다. <br>
현재는 온라인에 생성되어 있는 neo4j sandbox에 연결이 되도록 설정이 되어 있습니다. <br>
다른 곳에서 작업을 할 경우, 그에 따라 적절히 수정하면 됩니다.

main.py의 경우, input을 받아서 recommendation을 수행하는 main file입니다.
